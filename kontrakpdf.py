import streamlit as st
import openai
import PyPDF2
import io

# Fungsi untuk mengekstrak teks dari PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

# Fungsi untuk menganalisis teks menggunakan OpenAI GPT
def analyze_contract_with_gpt(contract_text, openai_api_key):
    openai.api_key = openai_api_key
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",  # Atau model lain yang Anda inginkan, misalnya "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "Anda adalah asisten yang membantu menganalisis dokumen kontrak. Berikan ringkasan poin-poin penting, potensi risiko, dan klausul utama."},
                {"role": "user", "content": f"Analisis dokumen kontrak berikut ini:\n\n{contract_text}\n\nBerikan ringkasan, potensi risiko, dan klausul utama dalam bahasa Indonesia."},
            ],
            max_tokens=1500,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Terjadi kesalahan saat memanggil OpenAI API: {e}"

# Tampilan aplikasi Streamlit
st.set_page_config(page_title="Penganalisis Kontrak PDF dengan OpenAI", layout="wide")

st.title("📄 Penganalisis Kontrak PDF")
st.markdown("Unggah dokumen kontrak PDF Anda dan dapatkan analisis otomatis menggunakan OpenAI.")

# Sidebar untuk API Key
with st.sidebar:
    st.header("Konfigurasi OpenAI")
    openai_api_key = st.text_input("Masukkan OpenAI API Key Anda", type="password")
    st.info("API Key Anda tidak akan disimpan.")
    st.markdown("[Dapatkan API Key di sini](https://platform.openai.com/account/api-keys)")

# Area utama untuk unggah file
st.header("Unggah Dokumen Kontrak PDF")
uploaded_file = st.file_uploader("Pilih file PDF", type=["pdf"])

analysis_result = None

if uploaded_file is not None:
    if not openai_api_key:
        st.warning("Mohon masukkan OpenAI API Key Anda di sidebar untuk melanjutkan.")
    else:
        st.success("File PDF berhasil diunggah!")
        
        # Baca teks dari PDF
        st.subheader("Mengekstrak Teks dari PDF...")
        try:
            pdf_file_obj = io.BytesIO(uploaded_file.read())
            contract_text = extract_text_from_pdf(pdf_file_obj)
            st.text_area("Pratinjau Teks yang Diekstrak", contract_text[:1000] + "..." if len(contract_text) > 1000 else contract_text, height=300)
            
            if st.button("Mulai Analisis Kontrak"):
                with st.spinner("Menganalisis dokumen kontrak menggunakan OpenAI... Ini mungkin memakan waktu beberapa saat."):
                    analysis_result = analyze_contract_with_gpt(contract_text, openai_api_key)
                    
                st.subheader("Hasil Analisis Kontrak")
                st.write(analysis_result)
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses file PDF atau mengekstrak teks: {e}")

st.markdown("---")
st.markdown("Dibuat dengan ❤️ oleh AI Asisten")
