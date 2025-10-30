import streamlit as st
import networkx as nx
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils import sample_network, score_segmentation

def draw_network_plotly(G):
    # create positions
    pos = nx.spring_layout(G, seed=42)
    edge_x = []
    edge_y = []
    for u,v in G.edges():
        x0,y0 = pos[u]
        x1,y1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    node_x = []
    node_y = []
    text = []
    sizes = []
    for n in G.nodes(data=True):
        x,y = pos[n[0]]
        node_x.append(x)
        node_y.append(y)
        text.append(f"{n[0]}<br>{n[1].get('role','')}")
        sizes.append(20 if n[1].get('level',1)==1 else 30)

    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=1), hoverinfo='none')
    node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text', textposition='top center',
                            marker=dict(size=sizes), text=[n for n in list(G.nodes())],
                            hovertext=text, hoverinfo='text')
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(showlegend=False, margin=dict(l=0,r=0,t=20,b=0))
    return fig

def app():
    st.header('ICS Network Segmentation Trainer')
    st.write('Upload a small network CSV or generate a sample. Identify segmentation violations and get scored.')

    st.markdown('**Sample network**')
    if st.button('Generate sample network'):
        G = sample_network()
        st.session_state['seg_graph'] = G
    uploaded = st.file_uploader('Upload network CSV (optional)', type=['csv'])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        # Expect columns: source,target,source_level,target_level,source_role,target_role
        G = nx.from_pandas_edgelist(df, 'source', 'target', edge_attr=True, create_using=nx.DiGraph())
        for n in df['source'].unique():
            if n not in G.nodes():
                G.add_node(n)
        # attach node attrs if present
        for _,r in df.iterrows():
            if 'source_level' in r and not pd.isna(r['source_level']):
                G.nodes[r['source']]['level'] = int(r['source_level'])
            if 'target_level' in r and not pd.isna(r['target_level']):
                G.nodes[r['target']]['level'] = int(r['target_level'])
        st.session_state['seg_graph'] = G

    if 'seg_graph' not in st.session_state:
        st.info('No network loaded. Click "Generate sample network" or upload a CSV.')
        return

    G = st.session_state['seg_graph']
    st.plotly_chart(draw_network_plotly(G), use_container_width=True)

    st.markdown('**Identify violations**')
    st.write('Select an edge and state whether it is a segmentation violation relative to Purdue levels (L0-L4).')
    edges = list(G.edges())
    edge_strs = [f"{u} -> {v}" for u,v in edges]
    picked = st.selectbox('Pick edge', ['']+edge_strs)
    verdict = st.radio('Is this a segmentation violation?', ['Unknown','Yes','No'])
    comment = st.text_input('Comment / remediation suggestion')
    if st.button('Submit identification'):
        if picked=='':
            st.warning('Pick an edge first.')
        else:
            idx = edge_strs.index(picked)
            u,v = edges[idx]
            # store annotations
            anns = st.session_state.get('seg_annotations', [])
            anns.append({'edge':picked, 'verdict':verdict, 'comment':comment})
            st.session_state['seg_annotations'] = anns
            st.success('Recorded.')

    st.markdown('**Scoring**')
    anns = st.session_state.get('seg_annotations', [])
    df_ann = pd.DataFrame(anns) if anns else pd.DataFrame(columns=['edge','verdict','comment'])
    st.dataframe(df_ann)
    if st.button('Calculate compliance score'):
        score, details = score_segmentation(G, anns)
        st.metric('Segmentation compliance', f"{score:.1f}%")
        st.write('Details:')
        st.json(details)
