# /// script
# dependencies = ["PyYAML>=6,<7"]
# ///
"""Real consultation schema gates and an independent child-broker include regression.

Workspace dialogues run in verify-implementation-consultations.py; full child
submission and restart run in verify-development-lifecycle.py.
"""
import importlib.util
import json
import os
from pathlib import Path
import select
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


def verify_foreign_gates(work):
    cases=[]
    for name in ['done','ask-user','missing-session','incomplete','error','malformed','missing-field','wrong-next']:
        response={'next':'ask_user' if name=='ask-user' else 'done','summary':'Answer from this cell.'}
        if name=='missing-field': del response['summary']
        if name=='wrong-next': response['next']='invented'
        raw='not json' if name=='malformed' else json.dumps(response)
        ops=[d.mock('recipe_within_resolution',{'resolved_selectors':{}}),d.mock('extension_execution',{'status':name if name in ['incomplete','error'] else 'completed','sessionId':'B-session',**({} if name=='missing-session' else {'session':d.session_ref('B-session')})},{'result.json':raw}),deps.passthrough('extension_execution')]
        if name not in ['malformed','missing-field','wrong-next']:ops.append(deps.passthrough('command_execution'))
        cases.append({'id':name,'type':'recipe_case','inputs':{'message':'Discuss ownership'},'mocks':{'ops':ops},'assertions':[{'type':'output_equals','path':'valid','value':name in ['done','ask-user']}]})
    d.run_suite(ROOT/'recipes/develop/consult.yaml',cases,work/'foreign-gates')
    print('consultation: 8 real routing/schema/session cases passed',flush=True)


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
        verify_foreign_gates(work)
        verify_broker_includes(work / "broker")

if __name__=='__main__':main()
