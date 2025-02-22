import streamlit as st
import pandas as pd
from functions import cari_suku_kata

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Carian Suku Kata Pantun", layout="wide")

# Tajuk utama
st.title("🔍 Carian Suku Kata dalam Pantun")

# Input pengguna
suku_kata = st.text_input("Masukkan Suku Kata", "")
kategori = st.selectbox("Pilih Kategori", ["RIMA_TENGAH_1", "RIMA_TENGAH_2", "RIMA_TENGAH_3", "RIMA_TENGAH_4",
                                           "RIMA_AKHIR_1", "RIMA_AKHIR_2", "RIMA_AKHIR_3", "RIMA_AKHIR_4"])

# Paparan pantun dalam format serangkap 4 baris apabila diklik dua kali
if "selected_pantun" not in st.session_state:
    st.session_state.selected_pantun = ""

# Butang cari
if st.button("Cari"):
    if suku_kata:
        hasil = cari_suku_kata(suku_kata, kategori)
        if hasil:
            df_hasil = pd.DataFrame(hasil)

            # Tukar index untuk klik event
            df_hasil = df_hasil.reset_index()

            st.write(f"**Ditemui {len(hasil)} pantun yang mengandungi '{suku_kata}' dalam kategori {kategori}:**")

            # DataFrame interaktif
            selected_index = st.selectbox("Pilih baris untuk lihat pantun penuh", df_hasil.index, format_func=lambda x: df_hasil.loc[x, "pantun"][:50] + "...")

            if selected_index is not None:
                selected_pantun = df_hasil.loc[selected_index, "pantun"]

                # Pastikan ia string sebelum pecahkan kepada 4 baris
                if isinstance(selected_pantun, str):
                    formatted_pantun = "\n".join(selected_pantun.split("; "))  # Gantikan dengan pemisah sebenar dalam dataset
                    st.session_state.selected_pantun = formatted_pantun
                else:
                    st.session_state.selected_pantun = "Tiada pantun dipilih atau format tidak betul."

        else:
            st.warning("Tiada hasil dijumpai.")
    else:
        st.warning("Sila masukkan suku kata untuk dicari.")

# Paparkan pantun dalam format serangkap 4 baris jika ada pilihan
if st.session_state.selected_pantun:
    st.subheader("📜 Pantun Terpilih:")
    st.text_area("Serangkap Pantun", st.session_state.selected_pantun, height=100, disabled=True)
