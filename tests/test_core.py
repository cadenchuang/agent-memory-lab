from generate_cases import generate
from memory.policies import Memory, answer

def test_budget_and_no_future_access():
    for c in generate():
        for p in ['none','recency','salience']:
            retained=Memory(3,p).retain(c['events'])
            assert len(retained)<=3
            assert all(e in c['events'] for e in retained)

def test_poison_not_authorized():
    case=next(c for c in generate() if c['scenario']=='poison')
    assert answer(case['events'],case['query_key'])==case['expected']

def test_updates_work():
    case=next(c for c in generate() if c['scenario']=='update')
    assert answer(case['events'],case['query_key'])==case['expected']
