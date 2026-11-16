"""Producer declarations and the actual generated draft-2020-12 schemas."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('review_v2', Path(__file__).resolve().parents[2] / 'recipes/review-v2.py')
v2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v2)


def request():
    return dict(review_id='test-review', title='Review saved drafts', question='Approve?', documents={},
                directions=[dict(id='accept', label='Approve', feedback_mode='forbidden', allow_attachments=False, continues_review=False),
                            dict(id='question', label='Ask', feedback_mode='required', allow_attachments=True, continues_review=True)],
                feedback={'label': 'Question'}, conversation=[])


def setting(control='text', **values):
    return dict(id='unfamiliar', label='Example preference', effect='Changes fixture output.', control=control,
                applies_to=['question'], **values)


class Contract(unittest.TestCase):
    def test_valid_original_coordinates_and_snapshot(self):
        r=request();ref={'kind':'stored','name':'design.md','stored':{'key':{'jobId':'another-job','taskOrdinal':3,'name':'design.md','sizeBytes':10}}}
        r['documents']={'original':ref};r['overview_document_id']='original'
        form=v2.build_form(r)
        self.assertEqual(form['request']['documents']['original'],ref)
        self.assertNotIn('fields',form);self.assertNotIn('kind',form)
        form['request']['documents']['original']['name']='different'
        self.assertEqual(r['documents']['original']['name'],'design.md')

    def test_invalid_declarations(self):
        for field,value in [('allow_attachments',None),('continues_review',None),('feedback_mode','maybe'),('feedback_required',False)]:
            r=request();r['directions'][0][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):v2.build_form(r)
        r=request();r['directions'][0]['allow_attachments']=True
        with self.assertRaises(ValueError):v2.build_form(r)
        r=request();r['directions'].append(copy.deepcopy(r['directions'][0]))
        with self.assertRaises(ValueError):v2.build_form(r)
        r=request();r['document_metadata']={'missing':{'title':'Unattached'}}
        with self.assertRaises(ValueError):v2.build_form(r)
        r=request();r['feedback']['allow_attachments']=False
        with self.assertRaises(ValueError):v2.build_form(r)

    def test_controls_and_reset(self):
        for s in [setting(value='日本🙂',schema={'type':['string','null'],'minLength':3,'maxLength':3},default=None,reset_label='Reset'),
                  setting('boolean',value=False,schema={'type':'boolean'}),
                  setting('number',value=0,schema={'type':'integer','minimum':0,'maximum':10}),
                  setting('choice',value=None,default=None,reset_label='Reset',choices=[{'value':'x','label':'X'}],schema={'type':['string','null']})]:
            r=request();r['settings']=[s];v2.build_form(r)
        for s in [setting(value='x',schema={'type':'string','minLength':3,'maxLength':2}),
                  setting(value='x',schema={'type':'string','default':'x'}),
                  setting(value='x',schema={'type':'boolean'}),
                  setting(value='x',schema={'type':'string'},default=None),
                  setting('number',value=0,schema={'type':'integer','exclusiveMinimum':0,'exclusiveMaximum':1}),
                  setting('choice',value=1,choices=[{'value':1,'label':'1'},{'value':1.0,'label':'Same'}],schema={'type':'number'})]:
            r=request();r['settings']=[s]
            with self.subTest(s=s),self.assertRaises(ValueError):v2.build_form(r)
        self.assertTrue(v2.unique([False,0,None,'0']))
        self.assertFalse(v2.unique([1,1.0]))

    def test_shared_vectors(self):
        vectors=json.loads(Path(__file__).with_name('contract-vectors.json').read_text())
        for v in vectors['patterns']:
            with self.subTest(v=v):
                try: pattern=v2.portable_pattern(v['pattern'])
                except ValueError:self.assertFalse(v['valid'])
                else:
                    self.assertTrue(v['valid'])
                    for value,expected in v.get('matches',[]):self.assertEqual(bool(pattern.search(value)),expected)
        for v in vectors['feedback']:
            self.assertEqual(v2.text(v['text']),v['meaningful'])
        for v in vectors['scalars']:
            with self.subTest(v=v):
                try: v2.validate_scalar(v['value'], v['schema'])
                except ValueError: self.assertFalse(v['valid'])
                else: self.assertTrue(v['valid'])
        for v in vectors['declarations']:
            r = request()
            r.update(v.get('patch', {}))
            if 'setting' in v: r['settings'] = [v['setting']]
            with self.subTest(v=v):
                try: v2.build_form(r)
                except ValueError: self.assertFalse(v['valid'])
                else: self.assertTrue(v['valid'])

    def test_generated_response_schema(self):
        # Optional installed dependency: native.test.yaml independently submits these
        # through c2j; this provides quick parity while iterating on the generator.
        from jsonschema import Draft202012Validator
        r=request();r['settings']=[setting('number',value=0,schema={'type':'integer','minimum':0})]
        form=v2.build_form(r);schema=form['response_schema']
        Draft202012Validator.check_schema(schema)
        validate=Draft202012Validator(schema).is_valid
        self.assertTrue(validate(dict(direction='accept',feedback='',attachments=[],settings={})))
        for value in ['',*v2.WHITE_SPACE,v2.WHITE_SPACE*2]:
            self.assertFalse(validate(dict(direction='question',feedback=value,attachments=[],settings={})))
        for value in [' ', '\ufeff', 'meaningful']:
            self.assertFalse(validate(dict(direction='accept',feedback=value,attachments=[],settings={})))
        self.assertTrue(validate(dict(direction='question',feedback='  日本語\n',attachments=[],settings={'unfamiliar':0})))
        for values in [{'unfamiliar':False},{'model':'x'},{'unfamiliar':None}]:
            self.assertFalse(validate(dict(direction='question',feedback='Why?',attachments=[],settings=values)))
        self.assertFalse(validate(dict(direction='accept',feedback='',attachments=[],settings={'unfamiliar':0})))
        self.assertFalse(validate(dict(direction='question',feedback='',attachments=[],settings={'unfamiliar':0})))
        ref={'kind':'stored','stored':{'key':{'jobId':'upload','taskOrdinal':0,'name':'notes.md','sizeBytes':0}}}
        self.assertTrue(validate(dict(direction='question',feedback='',attachments=[ref],settings={})))
        self.assertFalse(validate(dict(direction='accept',feedback='',attachments=[ref],settings={})))
        self.assertFalse(validate(dict(direction='question',feedback='Why?',attachments=[],settings={},actor='forged')))
        self.assertFalse(validate(dict(direction='question',feedback='Why?',settings={})))

if __name__=='__main__':unittest.main()
