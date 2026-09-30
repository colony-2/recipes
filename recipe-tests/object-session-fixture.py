"""Replace model calls while preserving real c2j object publication/hydration."""
import copy
import subprocess
import tempfile
from pathlib import Path
import yaml

RUNNER = '''import json, os, pathlib, shutil, subprocess, sys
request=json.load(sys.stdin)
home=pathlib.Path(os.environ['C2J_OBJECT_OUTBOX'])/'home'
prior=request.get('session')
if prior:
    assert prior['ref']['type']=='c2ops.codex.session/v1'
    shutil.copytree(prior['files']['home'],home)
else: home.mkdir()
env={**os.environ,**request['env'],'SESSION_HOME':str(home),'SESSION':prior['metadata']['session_id'] if prior else ''}
assert not (pathlib.Path(env['INBOX'])/'codex-home-state').exists(), 'Legacy session artifacts leaked into inbox'
p=subprocess.run([sys.executable,'-c',request['code']],env=env,text=True,capture_output=True)
sys.stderr.write(p.stderr)
if p.returncode:
    sys.stderr.write(p.stdout)
    raise SystemExit(p.returncode)
output=json.loads(p.stdout.strip().splitlines()[-1])
if output.pop('_omit_session',False) or not output.get('sessionId'):
    print(json.dumps({'output':output}));raise SystemExit()
output['session']={'$object':'next'}
print(json.dumps({'output':output,'objects':{'next':{'type':'c2ops.codex.session/v1','metadata':{'session_id':output['sessionId']},'files':{'home':str(home)}}}}))
'''


_temporary = None
_selector = None

def install(folder):
    global _temporary, _selector
    if _selector: return _selector
    _temporary=tempfile.TemporaryDirectory(prefix='recipe-object-model-')
    repo=Path(_temporary.name)
    op=repo/"session-op";op.mkdir()
    (op/'op.yaml').write_text(yaml.safe_dump(dict(name='model-session',command=['python3','run.py'],input_schema={
        'type':'object','additionalProperties':False,'required':['env','code'],'properties':{
            'session':{'type':'object','x-c2j-object-type':'c2ops.codex.session/v1'},
            'env':{'type':'object'},'code':{'type':'string'}}},output_schema={
        'type':'object','properties':{'session':{'type':'object','x-c2j-object-type':'c2ops.codex.session/v1'},'sessionId':{'type':'string'},'status':{'type':'string'}}}),sort_keys=False))
    (op/'run.py').write_text(RUNNER)
    def git(*args): return subprocess.check_output(['git','-C',str(repo),*args],text=True).strip()
    git('init','-q','-b','main');git('add','.')
    git('-c','user.name=Recipe Test','-c','user.email=recipe-test@example.com','commit','-qm','Object fixture')
    _selector='git+'+repo.as_uri()+'//session-op@'+git('rev-parse','HEAD')
    return _selector


def replace(doc, folder, env, code):
    selector=install(folder)
    def visit(node):
        if isinstance(node,list):
            return [visit(n) for n in node]
        if not isinstance(node,dict):return node
        if '//codex@' in node.get('op',''):
            original=copy.deepcopy(node['inputs'])
            node['op']=selector
            node['inputs']={'env':{k:v for k,v in env.items() if k!='SESSION'},'code':code,'sandbox':{'type':'none'}}
            if 'session' in original:node['inputs']['session']=original['session']
            return node
        return {k:visit(v) for k,v in node.items()}
    return visit(doc)
