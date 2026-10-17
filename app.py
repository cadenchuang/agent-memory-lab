import pandas as pd
import streamlit as st

st.set_page_config(page_title='Agent Memory Lab',layout='centered')
st.title('Agent Memory Lab')
st.caption('Controlled synthetic cases · deterministic evidence policy · no LLM trained')
df=pd.read_csv('results/case_results.csv')
split=st.selectbox('Dataset split',['test','train'])
scenarios=st.multiselect('Scenarios',['recall','update','poison'],default=['recall','update','poison'])
filtered=df[(df.split==split)&(df.scenario.isin(scenarios))]
if len(filtered):
    chart=filtered.groupby('policy',as_index=False).agg(accuracy=('correct','mean'),abstention=('abstained','mean'))
    st.subheader('Performance (fraction of cases)')
    st.bar_chart(chart.set_index('policy'))
    st.dataframe(filtered[['case_id','scenario','policy','expected','prediction','correct','retained_ids']],hide_index=True,use_container_width=True)
    st.info('Salience is a hand-built heuristic. This is a benchmark infrastructure demo, not evidence of a trained future-value scorer or LLM robustness.')
