import csv
import json
from pathlib import Path
from memory.policies import Memory, answer

def main():
    cases=[json.loads(x) for x in Path('data/cases.jsonl').read_text().splitlines()]
    rows=[]
    for case in cases:
        for policy in ['none','recency','salience']:
            retained=Memory(capacity=3,strategy=policy).retain(case['events'])
            prediction=answer(retained,case['query_key'])
            rows.append(dict(case_id=case['id'],split=case['split'],scenario=case['scenario'],policy=policy,expected=case['expected'],prediction=prediction,correct=int(prediction==case['expected']),abstained=int(prediction=='ABSTAIN'),poison_adopted=int(case['scenario']=='poison' and prediction!=case['expected'] and prediction!='ABSTAIN'),retained_ids=json.dumps([e['id'] for e in retained])))
    Path('results').mkdir(exist_ok=True)
    with open('results/case_results.csv','w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    try:
        import duckdb
        con=duckdb.connect('results/experiments.duckdb')
        con.execute('CREATE OR REPLACE TABLE case_results AS SELECT * FROM read_csv_auto(\'results/case_results.csv\')')
        print(con.execute('SELECT split, scenario, policy, COUNT(*) n, ROUND(AVG(correct),2) accuracy, SUM(poison_adopted) poisoned FROM case_results GROUP BY ALL ORDER BY split,scenario,policy').fetchdf().to_string(index=False))
        con.close()
    except ImportError:
        print('duckdb not installed; CSV saved successfully')
    print(f'Wrote {len(rows)} evaluated policy/case combinations')

if __name__=='__main__': main()
