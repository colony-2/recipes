#!/usr/bin/env python3
"""Deterministic Codex CLI boundary; the real pinned c2ops adapters surround it."""
import json
import os
from pathlib import Path
import sqlite3
import sys

if sys.argv[1:] == ['--version']:
    print('codex-cli 0.157.1')
    raise SystemExit()
home = Path(os.environ['CODEX_HOME'])
assert 'sqlite_home='+json.dumps(str(home)) in sys.argv, sys.argv
rollout = home/'sessions/fixture-thread.jsonl'
prior = rollout.read_text() if rollout.exists() else ''
assert prior == os.environ['RECIPE_EXPECT'], (prior, os.environ['RECIPE_EXPECT'])
assert ('resume' in sys.argv) == bool(prior), sys.argv
home.mkdir(exist_ok=True)
rollout.parent.mkdir(exist_ok=True)
rollout.write_text(os.environ['RECIPE_WRITE'])
for name in ['state_5.sqlite','thread_history_1.sqlite','goals_1.sqlite','queue_1.sqlite','memories_1.sqlite']:
    with sqlite3.connect(home/name) as db:
        db.execute('CREATE TABLE IF NOT EXISTS threads (id TEXT PRIMARY KEY, rollout_path TEXT, cwd TEXT)')
        db.execute('INSERT OR REPLACE INTO threads VALUES (?, ?, ?)', ('fixture-thread',str(rollout),os.getcwd()))
with open(os.environ['RECIPE_TRACE'],'a') as trace:
    trace.write(json.dumps(dict(prior=prior,value=os.environ['RECIPE_WRITE'],home=str(home),cwd=os.getcwd()))+'\n')
if os.environ.get('RECIPE_FAIL') == 'true':
    raise SystemExit(3)
(Path(os.environ['RECIPE_OUTBOX'])/'evidence.json').write_text(json.dumps({'value':os.environ['RECIPE_WRITE']}))
print(json.dumps({'type':'session.created','session_id':'fixture-thread'}))
print(json.dumps({'type':'item.completed','item':{'item_type':'assistant_message','text':json.dumps({
    'status':'completed','assistantSummary':os.environ['RECIPE_WRITE'],'incompleteReason':'',
    'incompleteCategory':'','pendingDependencies':[],'errorMessage':''})}}))
