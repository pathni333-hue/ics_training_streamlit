import streamlit as st
from modules import segmentation, asset_lab, risk_workshop, threat_mapping, incident_response, hygiene_dashboard

st.set_page_config(page_title="OT/ICS Training Platform", layout="wide")

st.title("OT / ICS Interactive Training Platform")
st.markdown("A modular training platform containing six OT-focused labs. Select a module from the sidebar to begin.")

MODULES = {
    "1 - Network Segmentation Trainer": segmentation,
    "2 - Asset Discovery & Classification Lab": asset_lab,
    "3 - OT Risk Scoring Workshop": risk_workshop,
    "4 - Threat-to-Mitigation Mapping Challenge": threat_mapping,
    "5 - OT Incident Response Simulation": incident_response,
    "6 - OT Cyber Hygiene Assessment Dashboard": hygiene_dashboard
}

choice = st.sidebar.radio("Choose module", list(MODULES.keys()))
module = MODULES[choice]

st.sidebar.markdown("---")
st.sidebar.markdown("**Resources**")
st.sidebar.markdown("- Example datasets are in the `data/` folder.")
st.sidebar.markdown("- Expand modules in `modules/` to customise content.")

# Run selected module
module.app()
