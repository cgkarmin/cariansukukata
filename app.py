import streamlit as st
import pandas as pd
from functions import cari_suku_kata

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Carian Suku Kata Pantun", layout="wide")

# Gaya CSS untuk gelapkan teks dalam jadual
st.markdown("""
    <style>
        .stDataFrame div {
            font-weight: bold;
            color: black;
        }
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            padding: 10px;
            font-size: 12px;
            color: gray;
        }
    </style>
    """, unsafe_allow_html=True)

# Tajuk utama
st.title("🔍 Carian Suku Kata dalam Pantun")

# Tukar nama dropdown supaya lebih mudah dibaca
pilihan_kategori = {
    "Rima Tengah 1": "RIMA_TENGAH_1",
    "Rima Tengah 2": "RIMA_TENGAH_2",
    "Rima Tengah 3": "RIMA_TENGAH_3",
    "Rima Tengah 4": "RIMA_TENGAH_4",
    "Rima Akhir 1": "RIMA_AKHIR_1",
    "Rima Akhir 2": "RIMA_AKHIR_2",
    "Rima Akhir 3": "RIMA_AKHIR_3",
    "Rima Akhir 4": "RIMA_AKHIR_4"
}

# Input pengguna
suku_kata = st.text_input("Masukkan Suku Kata", "")
kategori_pilihan = st.selectbox("Pilih Kategori", list(pilihan_kategori.keys()))

# Simpan pantun terpilih dalam sesi Streamlit
if "selected_pantun" not in st.session_state:
    st.session_state.selected_pantun = ""

# Butang cari
if st.button("Cari"):
    if suku_kata:
        kategori = pilihan_kategori[kategori_pilihan]  # Tukar kembali ke nama asal untuk carian
        hasil = cari_suku_kata(suku_kata, kategori)
        if hasil:
            df_hasil = pd.DataFrame(hasil)

            # Hadkan kepada maksimum 5 pantun
            df_hasil = df_hasil.head(5)

            # Paparkan hasil dalam jadual dengan Suku Kata, Perkataan, dan Pantun
            st.write(f"**Menampilkan maksimum 5 pantun yang mengandungi '{suku_kata}' dalam kategori {kategori_pilihan}:**")
            edited_df = st.data_editor(df_hasil, use_container_width=True, num_rows="dynamic", key="pantun_table")

            # Apabila klik dua kali pada baris, pantun dipaparkan dalam format serangkap 4 baris
            selected_rows = edited_df.loc[edited_df.index.intersection(st.session_state.get('pantun_table', {}).get('edited_rows', []))]

            if not selected_rows.empty:
                selected_pantun = selected_rows.iloc[0]["pantun"]

                # Tukarkan pantun kepada format 4 baris
                if isinstance(selected_pantun, str):
                    formatted_pantun = "\n".join(selected_pantun.replace(",", ";").split("; "))  # Tukar pemisah jika perlu
                    st.session_state.selected_pantun = formatted_pantun

        else:
            st.warning("Tiada hasil dijumpai.")
    else:
        st.warning("Sila masukkan suku kata untuk dicari.")

# Paparkan pantun dalam format serangkap 4 baris jika ada pilihan
if st.session_state.selected_pantun:
    st.subheader("📜 Pantun Terpilih:")
    st.text_area("Serangkap Pantun", st.session_state.selected_pantun, height=150, disabled=True)

# Footer
st.markdown('<div class="footer">© 2023-2025 Carian Suku Kata. v1. 2008-2025. Sebuah carian suku kata berguna untuk membantu pengguna mengarang pantun.</div>', unsafe_allow_html=True)
