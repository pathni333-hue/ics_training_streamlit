# ICS Training Streamlit App

This is a ready-to-run Streamlit project with six OT/ICS training modules:
1. ICS Network Segmentation Trainer
2. Asset Discovery & Classification Lab
3. OT Risk Scoring Workshop
4. Threat-to-Mitigation Mapping Challenge
5. OT Incident Response Simulation
6. OT Cyber Hygiene Assessment Dashboard

## Run locally

1. Create a Python virtual environment and activate it (recommended).
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   streamlit run app.py
   ```

## Structure

- `app.py` - main Streamlit app / navigation
- `modules/` - individual module implementations (modular; expand as needed)
- `data/` - example CSVs and sample data
- `utils.py` - shared helper functions
- `requirements.txt` - minimal dependencies

This project is intentionally modular and contains example data and scoring logic you can extend for training.
