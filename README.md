
# Oil & Gas RFP/Contract Analyzer (Streamlit)

Analyzes Oil & Gas RFP documents for key dates, compliance requirements, and deliverables.

## Features
- Upload PDF or TXT RFPs (sample Oil & Gas RFP included)
- Extract key dates (submission deadline, pre-bid, etc.)
- Check compliance items (HSE, QA/QC, certifications, local content, etc.)
- Deliverable detection
- KPI dashboard (compliance %, items found/missing, key dates found)
- Download compliance matrix as CSV

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy
- Streamlit Community Cloud: deploy from this folder
