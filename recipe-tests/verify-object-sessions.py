# /// script
# dependencies = ["PyYAML>=6,<7"]
# ///
"""Real pinned Codex adapters, object store and workers; only Codex CLI is scripted."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import select
import shutil
import subprocess
import sys
sys.dont_write_bytecode = True
import tempfile

import yaml

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('deps',ROOT/'recipe-tests/verify-dependencies.py')
deps=importlib.util.module_from_spec(spec);spec.loader.exec_module(deps)
d=deps.defaults
CODEX=d.CODEX
SKILL=CODEX.replace('//codex@','//codex/run_skill@')


def e(value):return '${{ '+value+' }}'
def write(path,value):path.write_text(yaml.safe_dump(value,sort_keys=False))


def main():
    with tempfile.TemporaryDirectory(prefix='object-session-adapters-') as temporary:
        work=Path(temporary);binary=work/'jobdb-service'
        d.run(['go','build','-o',str(binary),'.'],cwd=ROOT/'recipe-tests/jobdb-service')
        server=subprocess.Popen([str(binary)],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
        try:
            assert select.select([server.stdout],[],[],20)[0]
            url=server.stdout.readline().strip();assert url.startswith('http://127.0.0.1:')
            env={k:v for k,v in os.environ.items() if not k.startswith(('C2J_CURRENT_','C2J_CHILD_JOB_')) and k!='C2J_TENANT_ID'}
            fake=work/'bin';fake.mkdir();shutil.copy(ROOT/'recipe-tests/fixtures/object-session-codex.py',fake/'codex');(fake/'codex').chmod(0o755)
            credential_home=work/'credential-home';credential_home.mkdir()
            env.update(C2J_JOBDB=url+'/test',TMPDIR=str(work),PATH=str(fake)+os.pathsep+env['PATH'],CODEX_HOME=str(credential_home))
            repo=d.repository(work,'object-cell');skill=repo/'.agents/skills/checkpoint-test';skill.mkdir(parents=True)
            (skill/'SKILL.md').write_text('---\nname: checkpoint-test\ndescription: Validate the session checkpoint fixture.\n---\n\nProduce the requested evidence.\n')
            d.git(repo,'add','.');d.git(repo,'commit','-qm','Session fixture skill')
            trace=work/'trace.jsonl'
            def node(name,previous,expected,value,*,skill=False,fail=False):
                inputs={'prompt':'Check the fixture session and produce evidence.','sandbox':{'type':'none'},'env':{
                    'RECIPE_EXPECT':expected,'RECIPE_WRITE':value,'RECIPE_TRACE':str(trace),
                    'RECIPE_OUTBOX':'{{ context.environment.op.outbox }}','RECIPE_FAIL':str(fail).lower()}}
                if previous is not None:inputs['session']=previous
                if skill:inputs.update(skill='checkpoint-test',output={'path':'evidence.json','schema':{'type':'object','required':['value'],'properties':{'value':{'type':'string'}}}})
                return {'id':name,'op':SKILL if skill else CODEX,'inputs':inputs}
            def execute(name,recipe,inputs=None,expected_error=None):
                recipe.setdefault('input_schema',{})['prompt']={'type':'string','required':True}
                path=work/(name+'.yaml');write(path,recipe)
                submit=subprocess.run(['c2j','submit','Object session regression','--cell',str(repo),'--recipe-file',str(path),'--inputs-json',json.dumps(inputs or {}),'--json'],env=env,text=True,capture_output=True,timeout=45)
                if submit.returncode:
                    assert expected_error and expected_error.lower() in (submit.stdout+submit.stderr).lower(),submit.stderr
                    return None
                job=json.loads(submit.stdout)['job_id']
                run=subprocess.run(['c2j','run','one','--job-id',job,'--wait-timeout','120s'],env=env,text=True,capture_output=True,timeout=180)
                (work/(name+'.log')).write_text(run.stdout+run.stderr)
                if expected_error:
                    assert run.returncode and expected_error.lower() in (run.stdout+run.stderr).lower(),(name,run.returncode,run.stderr[-6000:])
                    return None
                assert run.returncode==0,(name,run.stderr[-9000:])
                result=deps.request(url+'/test/job?id='+job)['Attempts'][-1]['Output']['Data']
                print('object adapters: '+name+' passed',flush=True)
                return result
            branches={'id':'session-branches','sequence':[
                node('a',None,'','alpha'),node('b',e('sequence.a.outputs.session'),'alpha','beta'),
                node('c',e('sequence.a.outputs.session'),'alpha','gamma'),
                node('d',e('sequence.b.outputs.session'),'beta','delta',skill=True),
                node('e',e('sequence.d.outputs.session'),'delta','epsilon')],
                'outputs':{**{n:e('sequence.'+n+'.outputs.session') for n in 'abcde'},
                    'ids':e('[sequence.a.outputs.sessionId,sequence.b.outputs.sessionId,sequence.c.outputs.sessionId,sequence.d.outputs.sessionId,sequence.e.outputs.sessionId]'),
                    'artifact_refs':e('sequence.e.artifacts')}}
            result=execute('branches-and-skill-interoperability',branches)
            assert result['ids']==['fixture-thread']*5
            assert len({json.dumps(result[n],sort_keys=True) for n in 'abcde'})==5
            assert all(result[n]['type']=='c2ops.codex.session/v1' for n in 'abcde')
            assert result['artifact_refs'] and not any('codex-home-state' in name or '__c2j_objects__' in name for name in result['artifact_refs'])
            def continuation(value,fail=False):
                return {'id':'continue-object','input_schema':{'session':{'type':'object','object_type':'c2ops.codex.session/v1','required':True}},
                    'inputs':{'session':e('inputs.session')},'sequence':[node('resume',e('inputs.session'),'gamma',value,fail=fail)],
                    'outputs':{'session':e('sequence.resume.outputs.session'),'summary':e('sequence.resume.outputs.assistantSummary')}}
            resumed=execute('new-job-new-worker',continuation('omega'),{'session':result['c']})
            assert resumed['summary']=='omega' and resumed['session']!=result['c']
            execute('failed-private-branch',continuation('discarded',True),{'session':result['c']},'failed')
            execute('retry-original-checkpoint',continuation('retry'),{'session':result['c']})
            for name,field,value,error in [
                ('wrong-type','type','other.session/v1','type'),
                ('foreign-tenant','tenant_id','other-tenant','tenant'),
                ('corrupted-reference','sha256','f'*64,'digest'),
            ]:
                bad=copy.deepcopy(result['c']);bad[field]=value
                execute(name,continuation('forbidden'),{'session':bad},error)
            bad=copy.deepcopy(result['c']);bad['artifact']['jobId']='missing-job'
            execute('missing-checkpoint',continuation('forbidden'),{'session':bad},'failed')
            for skill in [False,True]:
                for field,value in [('sessionId',''),('resume_context',{}),('session',None)]:
                    item=node('invalid',None,'','forbidden',skill=skill);item['inputs'][field]=value
                    execute(('skill-' if skill else 'codex-')+'reject-'+field,{'id':'invalid-input','sequence':[item]},expected_error=field)
            entries=[json.loads(line) for line in trace.read_text().splitlines()]
            assert [v['prior'] for v in entries[:6]]==['','alpha','alpha','beta','delta','gamma'],entries
            assert entries[-1]['value']=='retry' and entries[-1]['prior']=='gamma'
            assert entries[6:-1] and all(v['prior']=='gamma' and v['value']=='discarded' for v in entries[6:-1]),entries
            assert len({v['home'] for v in entries})==len(entries),'Private homes were reused'
            print('object adapters: 14 real interoperability, branch, retry and rejection cases passed',flush=True)
        finally:
            server.terminate();server.wait(timeout=10)


if __name__=='__main__':main()
