import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def risk_score_row(row):
    # simple scoring: impact (1-5) * likelihood (1-5)
    return row.get('impact',1) * row.get('likelihood',1)

def app():
    st.header('OT Risk Scoring Workshop')
    st.write('Input device characteristics or upload CSV (name, age_years, exposure, protocol, impact, likelihood).')

    uploaded = st.file_uploader('Upload devices CSV', type=['csv'])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
    else:
        # sample table
        df = pd.DataFrame([
            {'name':'PLC-1','age_years':8,'exposure':3,'protocol':'Modbus','impact':5,'likelihood':4},
            {'name':'HMI-1','age_years':4,'exposure':2,'protocol':'OPC','impact':4,'likelihood':2},
            {'name':'Historian-1','age_years':6,'exposure':3,'protocol':'MQTT','impact':4,'likelihood':3},
        ])

    st.dataframe(df)

    st.markdown('**Calculate risk**')
    if st.button('Score devices'):
        df['risk'] = df.apply(lambda r: risk_score_row(r), axis=1)
        fig = px.scatter(df, x='likelihood', y='impact', size='risk', hover_name='name', title='Risk heatmap (bubble)')
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df[['name','impact','likelihood','risk']])

    st.markdown('**Apply mitigation**')
    mitigate = st.checkbox('Apply mitigation: reduce likelihood by 1 for selected devices')
    if mitigate:
        sel = st.multiselect('Select devices to mitigate', df['name'].tolist())
        if st.button('Recalculate after mitigation'):
            df2 = df.copy()
            df2.loc[df2['name'].isin(sel),'likelihood'] = (df2.loc[df2['name'].isin(sel),'likelihood'] - 1).clip(lower=1)
            df2['risk'] = df2.apply(risk_score_row, axis=1)
            fig2 = px.scatter(df2, x='likelihood', y='impact', size='risk', hover_name='name', title='Post-mitigation risk')
            st.plotly_chart(fig2, use_container_width=True)
            st.dataframe(df2[['name','impact','likelihood','risk']])
