import streamlit as st
import requests
import biotite.structure.io as bsio
from stmol import showmol
import py3Dmol
import string
# stmol
def render_mol(pdb, style='stick'):
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb,'pdb')
    pdbview.setStyle({style:{'color':'spectrum'}})
    ##pdbview.setBackgroundColor('black')#('0xeeeeee')
    pdbview.zoomTo()
    pdbview.zoom(1.5, 400)
    pdbview.spin(False)
    showmol(pdbview, height = 500,width=800)


st.header("Crop Protein Prediction using ESMFold")

"""ESMFold (Developed by Facebook Meta AI) uses the representations from a large language model (ESM2) to generate an accurate structure prediction from the sequence of a protein."""
st.caption("[Check the publication here](https://www.nature.com/articles/d41586-022-03539-1)")
default_seq = "MASKSNYNLLFTALLVFIFAAVAAVGNEDCTPWTSTLITPLPSCRNYVEEQACRIEMPGPPYLAKQECCEQLANIPQQCRCQALRYFMGPKSRPDQSGLMELPGCPREVQMNFVPILVTPGYCNLTTVHNTPYCLGMEESQWS"
st.subheader("")

input_seq = st.text_area("Enter Your Protein Sequence", default_seq, height=200)
st.caption("""Example Sequence: CM 17 protein (Wheat)""")
transformed_seq = input_seq.translate({ord(c): None for c in string.whitespace})
if st.button("Predict"):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=input_seq)
    pdb_string = response.content.decode('utf-8')
    with open('predicted.pdb', 'w') as f:
        f.write(pdb_string)
    
    struct = bsio.load_structure('predicted.pdb', extra_fields=["b_factor"])
    b_value = round(struct.b_factor.mean(), 4)
    st.subheader('Predicted Protein Structure')
    render_mol(pdb_string)
    st.info(f"Confidence Score (pLDDT): {b_value*100}")
    st.caption("PLDDT range : 0 to 100")
    
