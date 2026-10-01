# /// script
# dependencies = ["PyYAML>=6,<7"]
# ///
"""Named defaults, late consultation, approved child work, restart and real merges.

Only model/human decisions are scripted. Verification commands run on the host
instead of Shai; schema gates, scope, includes, jobs, artifacts and Git are real.
Guards guides/BUG_REPORT_CHILD_SNAPSHOT_COLLISION_AFTER_CONSULTATION.md and
the public default recipe contract for exporting verification evidence.
"""
import copy
import importlib.util
import json
import os
from pathlib import Path
import select
import shutil
import subprocess
import sys
import tempfile

import yaml

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('late', ROOT/'recipe-tests/verify-implementation-consultations.py')
late = importlib.util.module_from_spec(spec); spec.loader.exec_module(late)
c, d, deps, e = late.c, late.d, late.deps, late.e


def install(repo, cell, mode, work, child):
    folder = repo/'.c2j/recipes'
    shutil.copytree(ROOT/'recipes/develop', folder/'develop')
    common = dict(CELL_KIND=cell, MODE=mode, B_CELL=str(child), TRACE=str(work/'trace.jsonl'),
                  DECISIONS=str(work/'decisions.jsonl'), INBOX='{{ context.environment.op.inbox }}',
                  OUTBOX='{{ context.environment.op.outbox }}', WORKTREE='{{ context.environment.op.worktree_path }}',
                  OWNER='{{ context.workflow.cell }}', WORKSPACE='{{ context.workspace.cell }}')
    agent = c.read('agent.yaml')
    code=(ROOT/'recipe-tests/fixtures/development-lifecycle-model.py').read_text()
    agent=d.objects.replace(agent,folder/'develop',{**common,'CONSULT':'false','INSTRUCTIONS':e('inputs.instructions'),'PROMPT':e('inputs.prompt')},code)
    c.write(folder/'develop/agent.yaml',agent)
    consult=d.objects.replace(c.read('consult.yaml'),folder/'develop',{**common,'CONSULT':'true'},code)
    c.write(folder/'develop/consult.yaml',consult)
    coordinator = c.read('develop.yaml')
    for name, node in list(coordinator['state']['states'].items()):
        if node.get('op') != 'input': continue
        coordinator['state']['states'][name] = dict(inputs=node['inputs'],transitions=node.get('transitions',[]),
            sequence=[dict(id='decision',op='command_execution',inputs=dict(env=dict(CELL=cell,STATE=name,DECISIONS=str(work/'decisions.jsonl'),FORM=e('json_stringify(inputs.form)')),
                run="""python3 - <<'HUMAN'
import json,os
state=os.environ['STATE'];form=json.loads(os.environ['FORM'])
assert state in ['approve_plan','plan_feedback','accept'], ('Unexpected feedback',state,form)
with open(os.environ['DECISIONS'],'a') as log:log.write(json.dumps({'cell':os.environ['CELL'],'state':state,'form':form})+'\\n')
print(json.dumps({'response':'approve' if state=='approve_plan' else 'satisfied' if state=='accept' else '', 'fields':{'decision':'approve' if state=='approve_plan' else 'satisfied' if state=='accept' else 'revise','feedback':'Incorporate the agreed external dependency into the design and test plan.'}}))
HUMAN
"""))], outputs=dict(response=e('json_parse(sequence.decision.outputs.stdout).response'),fields=e('json_parse(sequence.decision.outputs.stdout).fields'),receipt={},artifact_refs={}))
    c.write(folder/'develop/develop.yaml',coordinator)
    verify = c.read('verify.yaml'); del verify['sequence'][0]['inputs']['sandbox']
    c.write(folder/'develop/verify.yaml',verify)
    for entry in ['build','evolve']:
        recipe=yaml.safe_load((ROOT/(entry+'.yaml')).read_text())
        recipe['sequence'][0]['include']='./develop/develop.yaml'
        c.write(folder/(entry+'.yaml'),recipe)
    (repo/'AGENTS.md').write_text('Instructions for '+cell+'\n')
    d.git(repo,'add','.');d.git(repo,'commit','-qm','Install committed local default recipes')


def verify_lifecycle(work, binary, mode):
    work.mkdir(); workers=[]; logs=[]
    server=subprocess.Popen([str(binary)],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
    try:
        assert select.select([server.stdout],[],[],20)[0]
        url=server.stdout.readline().strip();assert url.startswith('http://127.0.0.1:')
        env={k:v for k,v in os.environ.items() if not k.startswith(('C2J_CURRENT_','C2J_CHILD_JOB_')) and k!='C2J_TENANT_ID'}
        env.update(C2J_JOBDB=url+'/test',TMPDIR=str(work),
                   GIT_AUTHOR_NAME='Recipe Test',GIT_AUTHOR_EMAIL='recipe-test@example.com',
                   GIT_COMMITTER_NAME='Recipe Test',GIT_COMMITTER_EMAIL='recipe-test@example.com')
        repos={cell:c.seed(work,'seed-'+cell) for cell in ['A','B']}
        upstreams={cell:work/('cell-'+cell.lower()+'.git') for cell in repos}
        heads={}
        for cell,repo in repos.items():
            install(repo,cell,mode,work,upstreams['B'])
            d.run(['git','init','--bare','-q','-b','main',str(upstreams[cell])])
            d.git(repo,'remote','add','origin',str(upstreams[cell]));d.git(repo,'push','-q','origin','main')
            heads[cell]=d.git(repo,'rev-parse','HEAD')
        parent=json.loads(d.run(['c2j','submit','Implement token validation','--'+mode,'--cell',str(upstreams['A']),'--json'],env=env))['job_id']
        def start(job,label):
            log=(work/(label+'.log')).open('w');logs.append(log)
            worker=subprocess.Popen(['c2j','run','one','--job-id',job,'--await-threshold','2s','--poll-interval','100ms','--wait-timeout','180s'],env=env,stdout=log,stderr=log)
            workers.append(worker);return worker
        def inspect(job):return deps.request(url+'/test/job?id='+job)
        def children():return json.loads(d.run(['c2j','list','children','--parent-tenant-id','test','--parent-job-id',parent,'--all-ops','--all','--status','READY,ACTIVE,PENDING_JOBS,COMPLETED,CANCELLED','--json'],env=env))['jobs']
        first=start(parent,'parent')
        def pending():
            status=inspect(parent)['Job']['Status']
            assert first.poll() is None and status!='COMPLETED', (work/'parent.log').read_text()[-8000:]
            return status=='PENDING_JOBS'
        deps.eventually(pending,timeout=180)
        submitted=children();assert len(submitted)==1,submitted
        child=submitted[0]['job_id']
        decisions=[json.loads(line) for line in (work/'decisions.jsonl').read_text().splitlines()]
        assert [x['state'] for x in decisions]==['approve_plan','plan_feedback','approve_plan'],decisions
        assert 'Provide token validation: valid tokens succeed and invalid tokens return an error.' in decisions[-1]['form']['fields'][0]['question']
        for cell in ['A','B']:assert d.run(['git','--git-dir',str(upstreams[cell]),'rev-parse','main']).strip()==heads[cell]
        first.terminate();first.wait(timeout=10)
        assert start(child,'child').wait(timeout=180)==0,(work/'child.log').read_text()[-8000:]
        child_result=inspect(child)['Attempts'][-1]['Output']['Data']
        assert child_result['merged'] and child_result['verification']['ok'] and child_result['design']['assessment']['fit']=='fits'
        evidence=child_result['artifact_refs']
        for name in ['verification.json', 'check-1.log']:
            assert name in evidence, ('Child did not export verification evidence',name,evidence)
            assert evidence[name]['stored']['key']['jobId']==child, 'Evidence lost child provenance'
        assert d.run(['git','--git-dir',str(upstreams['B']),'rev-parse','main']).strip()==child_result['merged_hash']
        assert d.run(['git','--git-dir',str(upstreams['B']),'rev-list','--count',heads['B']+'..main']).strip()=='1'
        assert d.run(['git','--git-dir',str(upstreams['A']),'rev-parse','main']).strip()==heads['A']
        assert start(parent,'resumed').wait(timeout=180)==0,(work/'resumed.log').read_text()[-8000:]
        result=inspect(parent)['Attempts'][-1]['Output']['Data']
        assert result['merged'] and result['verification']['ok'] and result['disposition']=='implemented',result
        assert result['session_id']=='A-implement'
        assert list(result['dependencies']['implementation'])==[child]
        assert result['dependencies']['implementation'][child]['outputs']['merged_hash']==child_result['merged_hash']
        for name in ['verification.json', 'check-1.log']:
            assert result['dependencies']['implementation'][child]['artifacts'][name]==evidence[name], 'Await changed evidence provenance'
        thread=result['consultations']['service']
        assert thread['session']['type']=='c2ops.codex.session/v1' and thread['commit']==heads['B'] and thread['turn_count']==1
        assert 'turns' not in thread and 'session_id' not in thread
        assert result['design']['handoffs'][0]['provenance']['commit']==heads['B']
        assert len(children())==1,'Replay duplicated child submission'
        rows=[json.loads(line) for line in (work/'trace.jsonl').read_text().splitlines()]
        assert len([x for x in rows if x['role']=='consult'])==1,'Replay reran consultation'
        implementation=[x for x in rows if x['cell']=='A' and x['role']=='implement']
        assert [x['session'] for x in implementation]==['','A-implement','A-implement','A-implement']
        decisions=[json.loads(line) for line in (work/'decisions.jsonl').read_text().splitlines()]
        assert [(x['cell'],x['state']) for x in decisions]==[('A','approve_plan'),('A','plan_feedback'),('A','approve_plan'),('B','approve_plan'),('B','accept'),('A','accept')]
        relative='.c2j/' if mode=='evolve' else ''
        for cell,output in [('A',result),('B',child_result)]:
            def git(*args):return d.run(['git','--git-dir',str(upstreams[cell]),*args]).strip()
            assert git('rev-parse','main')==output['merged_hash']
            assert git('rev-list','--count',heads[cell]+'..main')=='1','Expected one squash commit per cell'
            assert git('show','main:'+relative+'feature.txt')=='valid:ok\ninvalid:error'
            assert git('show','main:app.txt')=='application'
            files=git('diff','--name-only',heads[cell],'main').splitlines()
            assert set(files)=={relative+f for f in (['feature.txt','test_feature.py','candidate.txt'] if cell=='A' else ['feature.txt','test_feature.py'])},files
        assert not (work/'trace.jsonl.errors').exists() or not (work/'trace.jsonl.errors').read_text()
        print('lifecycle: '+mode+' late consultation, named child, restart, verification and both squash merges passed',flush=True)
    except Exception:
        for log in logs:log.flush()
        # Preserve the first runtime failure, before automatic job retries obscure it.
        for path in work.glob('*.log'):
            errors=[line for line in path.read_text().splitlines() if 'ERROR' in line]
            if errors:print(path.name+': '+errors[0],file=sys.stderr)
        if (work/'trace.jsonl.errors').exists():print((work/'trace.jsonl.errors').read_text(),file=sys.stderr)
        if os.environ.get('C2J_TEST_LOG_DIR'):
            destination=Path(os.environ['C2J_TEST_LOG_DIR'])/('lifecycle-'+mode);destination.mkdir(parents=True,exist_ok=True)
            for path in list(work.glob('*.log'))+list(work.glob('*.jsonl')):shutil.copy(path,destination/path.name)
            for name in ['parent','child']:
                if name in locals():
                    (destination/(name+'-job.json')).write_text(json.dumps(inspect(locals()[name]),indent=2))
        raise
    finally:
        for worker in workers:
            if worker.poll() is None:worker.terminate();worker.wait(timeout=10)
        for log in logs:log.close()
        server.terminate();server.wait(timeout=10)


def main():
    with tempfile.TemporaryDirectory(prefix='development-lifecycle-') as temp:
        work=Path(temp);binary=work/'jobdb-service'
        d.run(['go','build','-o',str(binary),'.'],cwd=ROOT/'recipe-tests/jobdb-service')
        failures=[]
        for mode in sys.argv[1:] or ['build','evolve']:
            try:verify_lifecycle(work/mode,binary,mode)
            except Exception as error:print(f'FAILED lifecycle {mode}: {error}',flush=True);failures.append(mode)
        assert not failures,'Failed lifecycle cases: '+', '.join(failures)

if __name__=='__main__':main()
