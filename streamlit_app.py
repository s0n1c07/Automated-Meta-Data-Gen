import streamlit as st
from generate import generate_metadata

st.set_page_config(page_title="Automated Metadata Generator")
st.title("📄 Automated Metadata Generator")

# Cache metadata generation so if someone re‑uploads the same file, it's instant
@st.cache_data(show_spinner=False)
def get_metadata(path: str):
    return generate_metadata(path)

uploaded_file = st.file_uploader(
    "Upload a document (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    tmp_path = uploaded_file.name
    # write the uploaded bytes to a temporary file
    with open(tmp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"{uploaded_file.name} uploaded!")

    # generate (or fetch cached) metadata
    with st.spinner("Generating metadata..."):
        metadata = get_metadata(tmp_path)

    # display results
    st.subheader("📦 Extracted Metadata")
    st.json(metadata)

    # offer a download of the JSON
    st.download_button(
        "Download Metadata JSON",
        data=st.experimental_get_query_params(),  # or json.dumps(metadata)
        file_name=f"{uploaded_file.name.split('.')[0]}_meta.json",
        mime="application/json",
    )
