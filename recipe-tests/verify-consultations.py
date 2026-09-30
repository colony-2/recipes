# /// script
# dependencies = ["PyYAML>=6,<7"]
# ///
"""Mandate contracts and real same-job foreign workspaces on a disposable JobDB.

Only model replies are deterministic fixtures; checkout, artifacts, const
snapshots, node re-entry, child submission, waits and provenance are real c2j.
Broker/include and workspace/child-wait replay regressions execute independently.
Both must pass; compiled includes are exercised without the former inline workaround.
"""
import copy
import hashlib
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
spec = importlib.util.spec_from_file_location('dependencies', ROOT/'recipe-tests/verify-dependencies.py')
deps = importlib.util.module_from_spec(spec); spec.loader.exec_module(deps)
d = deps.defaults


def write(path, value): path.write_text(yaml.safe_dump(value, sort_keys=False))
def read(name): return yaml.safe_load((ROOT/'recipes/develop'/name).read_text())
def e(text): return '${{ '+text+' }}'


def seed(work, name):
    repo = d.repository(work, name)
    (repo/'.c2j/mandate.md').write_text((ROOT/'.c2j/mandate.md').read_text())
    d.git(repo, 'add', '.'); d.git(repo, 'commit', '-qm', 'Accepted mandate')
    return repo


def verify_mandates(work):
    repo = seed(work, 'mandate-cell'); out = work/'mandate-out'; out.mkdir()
    code = read('mandate.yaml')['sequence'][0]['inputs']['run']
    original = (repo/'.c2j/mandate.md').read_text(); baseline = d.git(repo,'rev-parse','HEAD')
    env = {'CELL_ROOT':str(repo),'CELL':'mandate-cell','OUTBOX':str(out),'COMMIT':''}
    for case in ['valid','missing','bad-schema','missing-section','duplicate-id','zero-id','missing-examples','symlink','pinned']:
        path=repo/'.c2j/mandate.md'
        if path.is_symlink(): path.unlink()
        path.write_text(original)
        if case=='missing': path.unlink()
        if case=='bad-schema': path.write_text(original.replace('c2.cell-mandate/v1','unknown'))
        if case=='missing-section': path.write_text(original.replace('## Purpose','## Unknown'))
        if case=='duplicate-id': path.write_text(original.replace('OWN-02:','OWN-01:'))
        if case=='zero-id': path.write_text(original.replace('OWN-01:','OWN-00:'))
        if case=='missing-examples': path.write_text(original.replace('`partial`','`mixed`'))
        if case=='pinned': path.write_text('Unaccepted broadening')
        if case=='symlink': path.unlink(); path.symlink_to(ROOT/'.c2j/mandate.md')
        d.git(repo,'add','.'); d.git(repo,'commit','--allow-empty','-qm',case)
        value=d.command_test(code,{**env,'COMMIT':baseline if case=='pinned' else ''})
        assert value['valid']==(case in ['valid','pinned']), (case,value)
        if case=='pinned': assert value['commit']==baseline and value['sha256']==hashlib.sha256(original.encode()).hexdigest()
    print('mandate: 9 provenance/format cases passed',flush=True)


def data():
    m={'cell':'test','valid':True,'path':'.c2j/mandate.md','commit':d.HASH,'sha256':'b'*64,'clauses':['OWN-01','EXCLUDE-01','Purpose','Owns']}
    r=copy.deepcopy(d.DESIGN)
    b={**d.BASE,'fit':'fits','design_markdown':'Agreed service change'}
    history={'service':{'cell':'service','ref':'main','commit':d.HASH,'session_id':'B-session','session':d.session_ref('B-session'),'mandate':{**m,'cell':'service'},'turns':[{'message':'Design?','response':b}],'response':b}}
    return m,r,history


def verify_contract(work):
    code=d.script('design.yaml','contract'); cases=['fits','partial','outside','clarification','consult','repeat','limit','unknown-clause','wrong-owner','wrong-fit','unresolved-assessed','missing-mandate','duplicate-outcome','foreign-requirement','missing-handoff','changed-handoff','wrong-handoff-owner','unagreed-handoff','duplicate-handoff','retarget-cell','retarget-ref','missing-session','false-ready']
    positive={'fits','partial','outside','clarification','consult','repeat','limit'}
    for case in cases:
        m,r,h=data(); initial={}; session='A-session'
        if case in ['partial','missing-handoff','changed-handoff','wrong-handoff-owner','unagreed-handoff','duplicate-handoff']:
            r['assessment']['fit']='partial';r['assessment']['outcomes'].append({'id':'R2','statement':'Service behavior','ownership':'external','suggested_owner':'service','mandate_evidence':['EXCLUDE-01'],'reason':'Service owns this'})
            r['handoffs']=[{'thread_id':'service','cell':'service','mode':'build','outcome_ids':['R2'],'design_markdown':'Agreed service change'}]
        if case=='outside': r['assessment']['fit']='outside';r['assessment']['outcomes'][0].update(ownership='external',suggested_owner='service');r['requirements']=[]
        if case=='clarification': r['assessment'].update(assessment_status='needs_clarification',fit=None,questions=['Who owns this?']);r.update(status='needs_input',questions=['Who owns this?']);m['valid']=False
        if case in ['consult','repeat','limit','retarget-cell','retarget-ref','missing-session']:
            r['consultation']={'thread_id':'service','cell':'service','ref':'main','message':'Refine design'}
            if case=='consult': h={}
            if case=='limit': h['service']['turns']*=8
            if case=='retarget-cell': r['consultation']['cell']='other'
            if case=='retarget-ref': r['consultation']['ref']='other'
            if case=='missing-session':session=''
        if case=='unknown-clause':r['assessment']['outcomes'][0]['mandate_evidence']=['OWN-99']
        if case=='wrong-owner':r['assessment']['outcomes'][0]['suggested_owner']='other'
        if case=='wrong-fit':r['assessment']['fit']='partial'
        if case=='unresolved-assessed':r['assessment']['outcomes'][0]['ownership']='unresolved'
        if case=='missing-mandate':m['valid']=False
        if case=='duplicate-outcome':r['assessment']['outcomes']*=2
        if case=='foreign-requirement':r['requirements'].append({'id':'R2','statement':'Foreign behavior'})
        if case=='missing-handoff':r['handoffs']=[]
        if case=='changed-handoff':r['handoffs'][0]['design_markdown']='Unreviewed change'
        if case=='wrong-handoff-owner':r['handoffs'][0]['cell']='other'
        if case=='unagreed-handoff':h['service']['response']['fit']='partial'
        if case=='duplicate-handoff':r['handoffs']*=2
        if case=='false-ready':r['questions']=['Undecided']
        out=work/('contract-'+case);out.mkdir()
        result=d.command_test(code,{'RESULT_JSON':json.dumps(r),'MANDATE_JSON':json.dumps(m),'HISTORY_JSON':json.dumps(h),'INITIAL_HISTORY_JSON':json.dumps(initial),'PROMPT':'Improve behavior','FEEDBACK':'','SESSION':json.dumps(d.session_ref(session) if session else None),'OUTBOX':str(out)},ok=case in positive)
        if case=='repeat':assert result['selection']['workspace_ref']==d.HASH and result['selection']['session']==d.session_ref('B-session')
        if case=='limit':assert not result['selection'] and result['result']['status']=='needs_input'
        if case=='partial':assert result['result']['handoffs'][0]['provenance']['commit']==d.HASH
    print(f'design: {len(cases)} ownership/consultation contract cases passed',flush=True)


def verify_routing(work):
    cases=[]
    for mode in ['build','evolve']:
        outside=copy.deepcopy(d.DESIGN);outside['assessment']['fit']='outside';outside['requirements']=[]
        outside['assessment']['outcomes'][0].update(ownership='external',suggested_owner='service')
        case=d.case('outside',d.phase(outside)+[d.response('acknowledge')],False)
        case['inputs']['type']=mode;case['assertions'].append({'type':'output_equals','path':'disposition','value':'outside'})
        partial=copy.deepcopy(d.DESIGN);partial['assessment']['fit']='partial'
        partial['assessment']['outcomes'].append({'id':'R2','statement':'External behavior','ownership':'external','suggested_owner':'service','mandate_evidence':['EXCLUDE-01'],'reason':'External owner'})
        partial['handoffs']=[{'thread_id':'service','cell':'service','mode':'build','outcome_ids':['R2'],'design_markdown':'Agreed external design'}]
        partial_case=d.case('partial',d.phase(partial)+d.planning()[len(d.phase(d.DESIGN)):]+[d.response('approve')]+d.implementation()+d.verification()+d.finish())
        partial_case['inputs']['type']=mode
        partial_case['assertions'].append({'type':'output_equals','path':'design.assessment.fit','value':'partial'})
        d.run_suite(ROOT/(mode+'.yaml'),[case,partial_case],work/('ownership-'+mode))
    print('routing: 4 partial/outside cases passed across both entrypoints',flush=True)


def verify_foreign_gates(work):
    cases=[]
    for name in ['ready','needs-input','partial','outside','missing-session','incomplete','error','malformed','missing-field']:
        response={**d.BASE,'fit':'fits','design_markdown':'Agreed design'}
        if name=='needs-input':response.update(status='needs_input',fit=None,questions=['Clarify ownership'])
        if name in ['partial','outside']:response['fit']=name
        if name=='missing-field':del response['fit']
        raw='not-json' if name=='malformed' else json.dumps(response)
        ops=[d.mock('recipe_within_resolution',{'resolved_selectors':{}}),d.command({'valid':True}),d.mock('extension_execution',{'status':name if name in ['incomplete','error'] else 'completed','sessionId':'B-session',**({} if name=='missing-session' else {'session':d.session_ref('B-session')})},{'result.json':raw}),deps.passthrough('extension_execution')]
        if name not in ['malformed','missing-field']:ops.append(deps.passthrough('command_execution'))
        cases.append({'id':name,'type':'recipe_case','inputs':{'message':'Assess this request'},'mocks':{'ops':ops},'assertions':[{'type':'output_equals','path':'valid','value':name in ['ready','needs-input','partial','outside']}]})
    d.run_suite(ROOT/'recipes/develop/consult.yaml',cases,work/'foreign-gates',parallelism=4)
    code=d.script('consult.yaml','read')
    for name in ['invalid-mandate','false-ready','illegal-children']:
        path=work/(name+'.json');path.write_text(json.dumps({**d.BASE,'fit':'fits','design_markdown':'Design','questions':['Undecided'] if name=='false-ready' else []}))
        d.command_test(code,{'RESULT':str(path),'MANDATE_JSON':json.dumps({'valid':name!='invalid-mandate'}),'JOBS_JSON':json.dumps(['unexpected'] if name=='illegal-children' else [])},ok=False)
    print('consultation: 12 real schema/status/submission gate cases passed',flush=True)


def verify_service(work, handoff=True):
    work.mkdir(); binary=work/'jobdb-service'
    d.run(['go','build','-o',str(binary),'.'],cwd=ROOT/'recipe-tests/jobdb-service')
    logs=[]; processes=[]
    server=subprocess.Popen([str(binary)],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
    try:
        assert select.select([server.stdout],[],[],20)[0]
        url=server.stdout.readline().strip();uri=url+'/test'
        env={k:v for k,v in os.environ.items() if not k.startswith(('C2J_CURRENT_','C2J_CHILD_JOB_')) and k!='C2J_TENANT_ID'}
        env.update(C2J_JOBDB=uri,TMPDIR=str(work))
        a=seed(work,'cell-a');b=seed(work,'cell-b');a_head=d.git(a,'rev-parse','HEAD');b_head=d.git(b,'rev-parse','HEAD')
        fixture=work/'fixture';shutil.copytree(ROOT/'recipes/develop',fixture)
        trace=work/'trace.jsonl'
        child_path=work/'child.yaml'
        write(child_path, {'id':'refined-child','input_schema':{'prompt':{'type':'string','required':True}},'inputs':{'prompt':e('inputs.prompt')},'sequence':[{'id':'mandate','include':'./fixture/mandate.yaml','inputs':{'commit':'','require_workspace':False}},{'id':'accept','op':'command_execution','inputs':{'env':{'PROMPT':e('inputs.prompt'),'MANDATE':e('json_stringify(sequence.mandate.outputs.mandate)'),'OUTBOX':'{{ context.environment.op.outbox }}'},'run':'''python3 - <<'CHILD'
import json,os,pathlib
h=json.loads(os.environ['PROMPT']);m=json.loads(os.environ['MANDATE'])
assert m['valid'] and h['provenance']['cell']==m['cell']
assert h['design_markdown']=='Service uses stable tokens; invalid tokens are rejected.' and h['outcome_ids']==['R2']
pathlib.Path(os.environ['OUTBOX'],'handoff.json').write_text(json.dumps(h))
CHILD
'''}}],'outputs':{'accepted':True}})
        model_inputs={'env':{'INBOX':'{{ context.environment.op.inbox }}','OUTBOX':'{{ context.environment.op.outbox }}','WORKTREE':'{{ context.environment.op.worktree_path }}','TRACE':str(trace),'B_CELL':str(b),'WORKSPACE':'{{ context.workspace.cell }}','OWNER':'{{ context.workflow.cell }}','INSTRUCTIONS':e('inputs.instructions'),'CHILD_RECIPE':str(child_path)},'run':'''python3 - 2>>"${TRACE}.error" <<'CODE'
import json,os,pathlib,subprocess
inbox=pathlib.Path(os.environ['INBOX']);out=pathlib.Path(os.environ['OUTBOX']);root=pathlib.Path(os.environ['WORKTREE'])
c=json.loads((inbox/'phase/context.json').read_text())
if os.environ['INSTRUCTIONS'].startswith('Implement'):
 context=c.get('phase',c);h=context['design']['handoffs'][0];dependencies=c.get('dependencies',{})
 assert h['provenance']['commit'] and h['design_markdown']=='Service uses stable tokens; invalid tokens are rejected.'
 if not os.environ['SESSION']:
  assert not dependencies
  subprocess.run(['c2j','submit',json.dumps(h),'--cell',h['cell'],'--recipe-file',os.environ['CHILD_RECIPE'],'--json'],check=True,stdout=subprocess.DEVNULL)
 else:
  assert os.environ['SESSION']=='I-session' and (pathlib.Path(os.environ['SESSION_HOME'])/'session.txt').read_text()=='I'
  assert len(dependencies)==1 and all(v['status']=='completed' and v['outputs']['accepted'] for v in dependencies.values())
  assert json.loads(next((inbox/'dependencies').rglob('handoff.json')).read_text())==h
 r={'status':'ready' if dependencies else 'needs_input','summary':'Integrated agreed service work','blocking_issues':[],'questions':[] if dependencies else ['Await service'],'changes':['Client behavior'],'consultation':None,'proposed_handoffs':[],'statement_tests':[{'statement_id':'T1','files':['test.sh']}]}
 (out/'result.json').write_text(json.dumps(r));(pathlib.Path(os.environ['SESSION_HOME'])/'session.txt').write_text('I')
 with open(os.environ['TRACE'],'a') as f:f.write(json.dumps({'actor':'I','session':os.environ['SESSION'],'workspace':os.environ['WORKSPACE'],'owner':os.environ['OWNER']})+'\\n')
 print(json.dumps({'status':'completed','sessionId':'I-session'}))
 raise SystemExit(0)
h=c['consultations'];m=c['mandate']
assert (root/'app.txt').read_text()=='application\\n' and not (root/'experiment.txt').exists()
if h: assert os.environ['SESSION']=='A-session' and (pathlib.Path(os.environ['SESSION_HOME'])/'session.txt').read_text()=='A', {'session':os.environ['SESSION'],'inbox':str(inbox),'context':c}
else: assert not os.environ['SESSION']
with open(os.environ['TRACE'],'a') as f:f.write(json.dumps({'actor':'A','session':os.environ['SESSION'],'workspace':os.environ['WORKSPACE'],'owner':os.environ['OWNER'],'turns':len(h.get('service',{}).get('turns',[]))})+'\\n')
r={'status':'ready','summary':'Reviewed mixed request','blocking_issues':[],'questions':[],'design_markdown':'Local client plus external service','requirements':[{'id':'R1','statement':'Client behavior'}], 'assessment':{'assessment_status':'assessed','fit':'partial','rationale':'Split ownership','questions':[],'outcomes':[{'id':'R1','statement':'Client behavior','ownership':'local','suggested_owner':m['cell'],'mandate_evidence':['OWN-01'],'reason':'Client owns this'},{'id':'R2','statement':'Service behavior','ownership':'external','suggested_owner':h['service']['mandate']['cell'] if h else 'cell-b','mandate_evidence':['EXCLUDE-01'],'reason':'Service owns this'}]},'consultation':None,'handoffs':[]}
if len(h.get('service',{}).get('turns',[]))<2:
 r.update(status='needs_input',questions=['Refine service design'],consultation={'thread_id':'service','cell':os.environ['B_CELL'],'ref':'main','message':'Use stable tokens and cover invalid tokens' if h else 'Discuss pagination design'})
else:
 r['handoffs']=[{'thread_id':'service','cell':os.environ['B_CELL'],'mode':'build','outcome_ids':['R2'],'design_markdown':h['service']['response']['design_markdown']}]
(out/'result.json').write_text(json.dumps(r));(pathlib.Path(os.environ['SESSION_HOME'])/'session.txt').write_text('A')
print(json.dumps({'status':'completed','sessionId':'A-session'}))
CODE
'''}
        code=model_inputs['run'].split("<<'CODE'\n",1)[1].rsplit('\nCODE',1)[0]
        agent=d.objects.replace(read('agent.yaml'),fixture,model_inputs['env'],code)
        write(fixture/'agent.yaml',agent)
        model_inputs={'env':{'INBOX':'{{ context.environment.op.inbox }}','OUTBOX':'{{ context.environment.op.outbox }}','WORKTREE':'{{ context.environment.op.worktree_path }}','TRACE':str(trace),'B_REPO':str(b),'B_HEAD':b_head,'WORKSPACE':'{{ context.workspace.cell }}','OWNER':'{{ context.workflow.cell }}'},'run':'''python3 - 2>>"${TRACE}.error" <<'CODE'
import json,os,pathlib,subprocess
root=pathlib.Path(os.environ['WORKTREE']);inbox=pathlib.Path(os.environ['INBOX']);out=pathlib.Path(os.environ['OUTBOX']);resumed=bool(os.environ['SESSION'])
assert (root/'app.txt').read_text()=='application\\n' and not (root/'experiment.txt').exists()
assert subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()==os.environ['B_HEAD'], {'actual':subprocess.check_output(['git','-C',str(root),'log','-3','--oneline'],text=True),'expected':os.environ['B_HEAD'],'session':os.environ['SESSION']}
assert os.environ['WORKSPACE']!=os.environ['OWNER']
if resumed: assert os.environ['SESSION']=='B-session' and (pathlib.Path(os.environ['SESSION_HOME'])/'session.txt').read_text()=='B'
else:
 assert not (pathlib.Path(os.environ['SESSION_HOME'])/'session.txt').exists()
 # Advance the source branch between turns. The recipe must use the original pin.
 source=pathlib.Path(os.environ['B_REPO']);(source/'unrelated.txt').write_text('new upstream commit')
 subprocess.run(['git','-C',str(source),'add','.'],check=True);subprocess.run(['git','-C',str(source),'commit','-qm','Unrelated advancement'],check=True)
(root/'experiment.txt').write_text('discard me');(root/'app.txt').write_text('experimental service')
r={'status':'ready' if resumed else 'needs_input','summary':'Agreed' if resumed else 'Clarify interface','fit':'fits','blocking_issues':[],'questions':[] if resumed else ['What token format?'],'design_markdown':'Service uses stable tokens; invalid tokens are rejected.'}
(out/'result.json').write_text(json.dumps(r));(pathlib.Path(os.environ['SESSION_HOME'])/'session.txt').write_text('B')
with open(os.environ['TRACE'],'a') as f:f.write(json.dumps({'actor':'B','session':os.environ['SESSION'],'workspace':os.environ['WORKSPACE'],'owner':os.environ['OWNER']})+'\\n')
print(json.dumps({'status':'completed','sessionId':'B-session'}))
CODE
'''}
        # Keep the production graph and let c2j handle the fixture session objects.
        code=model_inputs['run'].split("<<'CODE'\n",1)[1].rsplit('\nCODE',1)[0]
        consult=d.objects.replace(read('consult.yaml'),fixture,model_inputs['env'],code)
        write(fixture/'consult.yaml',consult)
        wrapper=work/'workflow.yaml'
        write(wrapper,{'id':'dialogue-and-handoff','input_schema':{'prompt':{'type':'string','required':True}},'inputs':{'prompt':e('inputs.prompt')},'sequence':[{'id':'design','include':str(fixture/'design.yaml'),'inputs':{'prompt':e('inputs.prompt')}},{'id':'implementation','include':str(fixture/'implement.yaml'),'inputs':{'prompt':e('inputs.prompt'),'context_json':e("'{\"design\":' + json_stringify(sequence.design.outputs.result) + '}'")}}],'outputs':{'design':e('sequence.design.outputs'),'implementation':e('sequence.implementation.outputs')}})
        if not handoff:
            recipe=yaml.safe_load(wrapper.read_text());recipe['sequence']=recipe['sequence'][:1];del recipe['outputs']['implementation'];write(wrapper,recipe)
        submitted=json.loads(d.run(['c2j','submit','Improve client and service','--recipe-file',str(wrapper),'--cell',str(a),'--json'],env=env));parent=submitted['job_id']
        log=(work/'parent.log').open('w');logs.append(log)
        process=subprocess.Popen(['c2j','run','one','--job-id',parent,'--poll-interval','100ms','--await-threshold','2s'],env=env,stdout=log,stderr=log);processes.append(process)
        inspect=lambda:deps.request(url+'/test/job?id='+parent)
        def child_jobs(): return json.loads(d.run(['c2j','list','children','--parent-tenant-id','test','--parent-job-id',parent,'--all-ops','--all','--status','READY,ACTIVE,PENDING_JOBS,COMPLETED,CANCELLED','--json'],env=env))['jobs']
        def submitted_or_failed():
            children=child_jobs()
            if inspect()['Job']['Status']=='COMPLETED' and not children:
                raise AssertionError((work/'parent.log').read_text()[-5000:]+((work/'trace.jsonl.error').read_text() if (work/'trace.jsonl.error').exists() else ''))
            return children
        if handoff:
            children=deps.eventually(submitted_or_failed,timeout=150)
            assert len(children)==1
            deps.eventually(lambda:inspect()['Job']['Status']=='PENDING_JOBS')
            process.terminate();process.wait(timeout=10)
            d.run(['c2j','run','one','--job-id',children[0]['job_id']],env=env,timeout=60)
            resumed_log=(work/'resumed.log').open('w');logs.append(resumed_log)
            process=subprocess.Popen(['c2j','run','one','--job-id',parent,'--poll-interval','100ms','--wait-timeout','60s'],env=env,stdout=resumed_log,stderr=resumed_log);processes.append(process)
        assert process.wait(timeout=180)==0, ((work/('resumed.log' if handoff else 'parent.log')).read_text()[-4000:] + ((work/'trace.jsonl.error').read_text() if (work/'trace.jsonl.error').exists() else ''))
        final=deps.request(url+'/test/job?id='+parent);outputs=final['Attempts'][-1]['Output']['Data'];result=outputs['design']
        if handoff: assert outputs['implementation']['valid'] and outputs['implementation']['completed'] and len(outputs['implementation']['dependencies'])==1
        assert result['valid'] and result['completed'] and result['result']['assessment']['fit']=='partial',result
        rows=[json.loads(line) for line in trace.read_text().splitlines()]
        assert [r['actor'] for r in rows]==(['A','B','A','B','A','I','I'] if handoff else ['A','B','A','B','A']),rows
        assert rows[0]['workspace']==rows[0]['owner'] and all(r['owner']==rows[0]['owner'] for r in rows)
        assert rows[3]['session']=='B-session' and rows[4]['session']=='A-session'
        assert result['consultations']['service']['commit']==b_head
        assert result['result']['handoffs'][0]['provenance']['commit']==b_head
        assert result['consultations']['service']['session']['type']=='c2ops.codex.session/v1'
        children=json.loads(d.run(['c2j','list','children','--parent-tenant-id','test','--parent-job-id',parent,'--all-ops','--all','--status','READY,ACTIVE,PENDING_JOBS,COMPLETED,CANCELLED','--json'],env=env))
        assert len(children['jobs'])==(1 if handoff else 0),'Expected only approved implementation dependencies'
        assert d.git(a,'rev-parse','HEAD')==a_head and d.git(a,'status','--porcelain')==''
        assert d.git(b,'status','--porcelain')=='' and (b/'app.txt').read_text()=='application\n' and not (b/'experiment.txt').exists()
        print('service: '+('approved child handoff and worker replacement passed' if handoff else 'A/B/A/B/A dialog, pinned commits, separate sessions, discarded experiments and no child jobs passed'),flush=True)
    finally:
        for process in processes:
            if process.poll() is None:process.terminate();process.wait(timeout=10)
        server.terminate();server.wait(timeout=10)
        for log in logs:log.close()


def verify_broker_includes(work):
    """Independent regression: submission of compiled includes, without workspaces or waits."""
    work.mkdir(); binary=work/'jobdb-service'
    d.run(['go','build','-o',str(binary),'.'],cwd=ROOT/'recipe-tests/jobdb-service')
    server=subprocess.Popen([str(binary)],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
    try:
        assert select.select([server.stdout],[],[],20)[0]
        url=server.stdout.readline().strip()
        env={k:v for k,v in os.environ.items() if not k.startswith(('C2J_CURRENT_','C2J_CHILD_JOB_')) and k!='C2J_TENANT_ID'}
        env.update(C2J_JOBDB=url+'/test',TMPDIR=str(work))
        a=seed(work,'cell-a');b=seed(work,'cell-b')
        write(work/'phase.yaml',{'id':'included-phase','sequence':[{'id':'answer','op':'command_execution','inputs':{'run':'printf included-child'}}],'outputs':{'answer':e('sequence.answer.outputs.stdout')}})
        write(work/'child.yaml',{'id':'included-child','input_schema':{'prompt':{'type':'string'}},'sequence':[{'id':'phase','include':'./phase.yaml'}],'outputs':{'answer':e('sequence.phase.outputs.answer')}})
        write(work/'parent.yaml',{'id':'broker-regression','input_schema':{'prompt':{'type':'string'}},'sequence':[{'id':'submit','op':'command_execution','inputs':{'env':{'CHILD':str(work/'child.yaml'),'CELL':str(b),'ERROR_LOG':str(work/'submit-error.log')},'run':"""python3 - <<'SUBMIT'
import os,pathlib,subprocess
result=subprocess.run(['c2j','submit','Approved external work','--cell',os.environ['CELL'],'--recipe-file',os.environ['CHILD'],'--json'],text=True,capture_output=True)
pathlib.Path(os.environ['ERROR_LOG']).write_text(result.stderr)
print(result.stdout)
result.check_returncode()
SUBMIT
"""}}],'outputs':{'jobs':e('sequence.submit.jobs.job_ids')}})
        job=json.loads(d.run(['c2j','submit','Broker regression','--cell',str(a),'--recipe-file',str(work/'parent.yaml'),'--json'],env=env))['job_id']
        worker=subprocess.run(['c2j','run','one','--job-id',job],env=env,text=True,capture_output=True,timeout=90)
        assert worker.returncode==0,(work/'submit-error.log').read_text()+worker.stderr[-1500:]
        parent=deps.request(url+'/test/job?id='+job)['Attempts'][-1]['Output']['Data']
        assert len(parent['jobs'])==1
        child=parent['jobs'][0]
        d.run(['c2j','run','one','--job-id',child],env=env,timeout=60)
        assert deps.request(url+'/test/job?id='+child)['Attempts'][-1]['Output']['Data']['answer']=='included-child'
        print('service: compiled-include child broker regression passed',flush=True)
    finally:
        server.terminate();server.wait(timeout=10)


def main():
    with tempfile.TemporaryDirectory(prefix='consultation-tests-') as temp:
        work=Path(temp)
        verify_mandates(work);verify_contract(work);verify_routing(work);verify_foreign_gates(work)
        failures=[]
        for name,check in [('dialogue',lambda:verify_service(work/'dialogue',handoff=False)),
                           ('handoff-replay',lambda:verify_service(work/'handoff',handoff=True)),
                           ('broker-includes',lambda:verify_broker_includes(work/'broker'))]:
            try: check()
            except Exception as error:
                print(f'FAILED {name}: {error}',flush=True);failures.append(name)
        assert not failures, 'Failed runtime regressions: '+', '.join(failures)

if __name__=='__main__':main()
