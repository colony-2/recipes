"""Validate real producer reports against the authored schemas, without mock flags."""
from copy import deepcopy
from pathlib import Path
import unittest
import jsonschema
import yaml

SCHEMAS = yaml.safe_load((Path(__file__).resolve().parents[2]/'recipes/adaptive3/schemas.yaml').read_text())['outputs']

class DocumentSchemas(unittest.TestCase):
    def test_document_producer_reports(self):
        detail=dict(document_id='review/decision.md', title='Save drafts on this browser',
                    description='Review the saving behavior and its limits.', role='primary', order=0)
        reports={
            'execute':dict(status='ready',summary='Ready for review.',title='Save drafts',primary='review/decision.md',
                           work_kind='feature',consultation=None,packages=None,assignment=None,delivery_recipe=None),
            'backstop':dict(status='ask',summary='Choose a browser for validation.',stage='implementation',action='Rerun validation with the available browser.',
                            additional_attempts=None,title='Choose the validation browser',primary='review/decision.md'),
            'recovery':dict(status='ask',summary='Restore the saved work.',stage='implementation',action=None,approval=None,
                            publication=None,queue_recovery=None,additional_attempts=None,title='Restore the draft repair',primary='review/decision.md'),
        }
        for name,report in reports.items():
            schema=SCHEMAS[name]
            report['document_details']=[detail]
            jsonschema.Draft202012Validator.check_schema(schema)
            jsonschema.validate(report,schema)
            invalid=[]
            for key in ('document_details','primary','title'):
                invalid.append({k:v for k,v in report.items() if k!=key})
            invalid.extend([{**report,'unexpected':True},{**report,'document_details':None},
                            {**report,'document_details':{}},{**report,'document_details':[None]}])
            for key in detail:
                invalid.append({**report,'document_details':[{k:v for k,v in detail.items() if k!=key}]})
            for patch in ({'unexpected':True},{'document_id':1},{'title':123},{'title':'a'*121},
                          {'description':'a'*301},{'role':'neutral'},{'order':True},{'order':None},
                          {'order':1.5},{'order':-1},{'order':1000001}):
                invalid.append({**report,'document_details':[{**detail,**patch}]})
            for bad in invalid:
                with self.subTest(schema=name, report=bad):
                    self.assertFalse(jsonschema.Draft202012Validator(schema).is_valid(bad))
            empty={**report,'primary':None,'document_details':[]}
            if name in ('backstop','recovery'):
                empty.update(action=None,stage=None)
            jsonschema.validate(empty,schema)
            unicode=deepcopy(report)
            unicode['document_details'][0].update(title='🐈'*120,description='é'*300,order=1000000)
            jsonschema.validate(unicode,schema)

if __name__=='__main__': unittest.main()
