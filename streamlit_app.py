import streamlit as st
from generate import generate_metadata

st.set_page_config(page_title="Automated Metadata Generator")
st.set_page_config(page_title="Automated Metadata Generator")
st.title("📄 Automated Metadata Generator")

uploaded_file = st.file_uploader(
    "Upload a document (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    tmp_path = uploaded_file.name
    with open(tmp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"{uploaded_file.name} uploaded!")

    with st.spinner("Generating report..."):
        report_text = generate_metadata(tmp_path)

    st.subheader("📋 Metadata Report")
    # read-only text area:
    st.text_area("Report", report_text, height=400, disabled=True)

    # download as plain .txt
    st.download_button(
        label="Download Report as TXT",
        data=report_text,
        file_name=f"{uploaded_file.name.rsplit('.',1)[0]}_metadata.txt",
        mime="text/plain"
    )
