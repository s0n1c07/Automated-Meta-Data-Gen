import streamlit as st
from generate import generate_metadata

# Page config
st.set_page_config(
    page_title="📄 Automated Metadata Generator",
    page_icon="🧠",
    layout="centered"
)

# Sidebar with info
with st.sidebar:
    st.markdown("## ℹ️ About")
    st.markdown(
        """
        This tool helps you automatically extract metadata from documents  
        (PDF, DOCX, or TXT). Upload your file and receive a clean report.

        **Built with ❤️ using Streamlit**
        """
    )
    st.markdown("---")
    st.markdown("### 🔗 Useful Tips")
    st.markdown(
        """
        - Ensure the document is not encrypted.  
        - Best results with well-formatted text.  
        - TXT files must use UTF-8 encoding.
        """
    )

# Title
st.markdown("<h1 style='text-align: center;'>📄 Automated Metadata Generator</h1>", unsafe_allow_html=True)
st.markdown("#### Upload a document below to generate its metadata report.")

# File uploader
uploaded_file = st.file_uploader(
    "Choose a document (PDF, DOCX, or TXT)",
    type=["pdf", "docx", "txt"],
    label_visibility="visible"
)

if uploaded_file:
    # Save temporarily
    tmp_path = uploaded_file.name
    with open(tmp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ {uploaded_file.name} uploaded successfully!")

    with st.spinner("🔍 Generating metadata..."):
        report_text = generate_metadata(tmp_path)

    # Display metadata report
    st.markdown("---")
    st.subheader("📋 Extracted Metadata Report")
    st.text_area("Metadata Report", report_text, height=350, disabled=True)

    # Download option
    st.download_button(
        label="⬇️ Download Report as TXT",
        data=report_text,
        file_name=f"{uploaded_file.name.rsplit('.',1)[0]}_metadata.txt",
        mime="text/plain"
    )

else:
    st.info("📤 Please upload a document to begin.")
