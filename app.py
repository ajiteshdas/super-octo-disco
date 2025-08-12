
import streamlit as st
import pandas as pd
import pdfplumber
import re
from io import BytesIO

st.set_page_config(page_title="Oil & Gas RFP/Contract Analyzer - Ajitesh Das", page_icon="📄", layout="wide")
st.title("📄 Oil & Gas RFP/Contract Analyzer by Ajitesh Das")
st.write("Upload an Oil & Gas RFP (PDF/TXT) to extract key dates, compliance requirements, and deliverables.")

# Sample file loader
@st.cache_data
def load_sample():
    return "sample_rfp_oilgas.pdf"

def show_sample_download():
    with open("sample_data.csv", "rb") as f:
        st.download_button(
            "📥 Download sample CSV",
            data=f,
            file_name="sample_data.csv",
            mime="text/csv",
            help="Grab a copy of the sample and tweak it if you like."
        )

show_sample_download = st.button("Download Sample RFP")

uploaded_file = st.file_uploader("Upload RFP", type=["pdf", "txt"])
use_sample = st.button("Use Sample Oil & Gas RFP")
if uploaded_file:
    file_bytes = uploaded_file.read()
elif use_sample:
    with open(load_sample(), "rb") as f:
        file_bytes = f.read()
else:
    st.stop()

# Extract text
text = ""
if uploaded_file or use_sample:
    try:
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
    except Exception as e:
        try:
            text = file_bytes.decode("utf-8", errors="ignore")
        except:
            st.error("Unable to extract text from file.")
            st.stop()

# Compliance checklist (Oil & Gas specific)
compliance_items = [
    "Health, Safety, and Environment",
    "Quality Assurance",
    "offshore oil and gas maintenance",
    "API certification",
    "ISO 9001",
    "ISO 14001",
    "Local Content",
    "Bid Bond",
    "insurance",
    "technical specifications",
    "project schedule",
]

deliverables = [
    "bid form",
    "Safety management plan",
    "Technical proposal",
    "equipment list",
    "Pricing schedule",
    "References",
]

# Date extraction
patterns = {
    "Pre-Bid Meeting": r"Pre-Bid Meeting:\s*(.+)",
    "Deadline for Questions": r"Deadline for Questions:\s*(.+)",
    "Proposal Submission Deadline": r"Proposal Submission Deadline:\s*(.+)",
    "Expected Award Date": r"Expected Award Date:\s*(.+)",
    "Anticipated Project Start": r"Anticipated Project Start:\s*(.+)",
}
dates_found = []
for label, pat in patterns.items():
    m = re.search(pat, text, re.IGNORECASE)
    if m:
        dates_found.append((label, m.group(1).strip()))

# Compliance matrix
comp_rows = []
found_count = 0
for item in compliance_items:
    found = re.search(item, text, re.IGNORECASE) is not None
    comp_rows.append({"Requirement": item, "Found": "✓" if found else "✗"})
    if found:
        found_count += 1

# Deliverables check
deliverable_rows = []
for item in deliverables:
    found = re.search(item, text, re.IGNORECASE) is not None
    deliverable_rows.append({"Deliverable": item, "Found": "✓" if found else "✗"})

# KPI Dashboard
total_items = len(compliance_items)
compliance_pct = (found_count / total_items * 100) if total_items else 0.0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Items Checked", total_items)
col2.metric("Items Found", found_count)
col3.metric("Items Missing", total_items - found_count)
col4.metric("Compliance %", f"{compliance_pct:.0f}%")
col5.metric("Key Dates Found", len(dates_found))

# Tabs
tab1, tab2, tab3 = st.tabs(["📅 Summary", "✅ Compliance", "❓ Questions to Clarify"])

with tab1:
    st.subheader("Key Dates")
    if dates_found:
        st.table(pd.DataFrame(dates_found, columns=["Event", "Date"]))
    else:
        st.write("No dates detected.")
    st.subheader("Deliverables")
    st.table(pd.DataFrame(deliverable_rows))

with tab2:
    st.subheader("Compliance Matrix")
    df_comp = pd.DataFrame(comp_rows)
    st.dataframe(df_comp, use_container_width=True)
    csv = df_comp.to_csv(index=False).encode("utf-8")
    st.download_button("Download Compliance CSV", csv, "compliance_matrix.csv", "text/csv")

with tab3:
    st.write("Potential questions to clarify (rule-based):")
    # Simple heuristic: if an item exists but no numbers/dates nearby, ask for details
    for item in compliance_items:
        if re.search(item, text, re.IGNORECASE):
            snippet_match = re.search(item + r".{0,120}", text, re.IGNORECASE)
            snippet = snippet_match.group(0) if snippet_match else ""
            has_numeric = re.search(r"\b\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}\b|\b\d{4}\b|%|\d+", snippet)
            if not has_numeric:
                st.write(f"- Please provide more details regarding '{item}' (specific standards, dates, or percentages).")
