import streamlit as st
import pandas as pd
from utils import sample_asset_csv

ASSET_CLASSES = ['PLC','HMI','Historian','Sensor','Actuator','Switch','Firewall','Unknown']

def app():
    st.header('Asset Discovery & Classification Lab')
    st.write('Upload a CSV with fake OT devices or use the sample. Then assign each device to a class.')

    if st.button('Generate sample CSV'):
        sample_asset_csv()
        st.success('Sample CSV written to data/sample_assets.csv')

    uploaded = st.file_uploader('Upload devices CSV', type=['csv'])
    if uploaded is None:
        try:
            df = pd.read_csv('data/sample_assets.csv')
        except Exception as e:
            st.info('No sample CSV yet — click "Generate sample CSV" or upload your own.')
            return
    else:
        df = pd.read_csv(uploaded)

    st.write('Devices:')
    st.dataframe(df)

    st.markdown('**Classify devices**')
    results = []
    for idx,row in df.iterrows():
        cols = st.columns([3,2,2])
        cols[0].write(f"**{row['name']}** — {row['ip']} — {row['vendor']}")
        pick = cols[1].selectbox('Class', ASSET_CLASSES, key=f'class_{idx}')
        if cols[2].button('Submit', key=f'submit_{idx}'):
            results.append({'name':row['name'],'assigned':pick, 'correct': pick==row.get('expected','Unknown')})
            st.write('Recorded.')

    if st.button('Show scoring'):
        if len(results)==0:
            st.info('No classifications recorded yet — use the Submit buttons.')
        else:
            dfr = pd.DataFrame(results)
            acc = dfr['correct'].mean()*100
            st.metric('Classification accuracy', f"{acc:.1f}%")
            st.dataframe(dfr)
