import streamlit as st
import pandas as pd
from functions import cari_suku_kata

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Carian Suku Kata Pantun", layout="wide")

# Susun layout dalam 2 kolum (kiri = input, kanan = hasil pantun yang dipilih)
col1, col2 = st.columns([1, 2])

with col1:
    # **Pendekkan input carian**
    suku_kata = st.text_input("🔍 Cari Suku Kata", "", max_chars=10, help="Masukkan suku kata yang ingin dicari")

    # **Pendekkan dropdown kategori**
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
    kategori_pilihan = st.selectbox("📂 Pilih Kategori", list(pilihan_kategori.keys()), help="Pilih jenis rima yang ingin dicari")

    # Simpan pantun terpilih dalam sesi Streamlit
    if "selected_pantun" not in st.session_state:
        st.session_state.selected_pantun = ""

    # Butang cari
    if st.button("🔍 Cari Pantun"):
        if suku_kata:
            kategori = pilihan_kategori[kategori_pilihan]  # Tukar kembali ke nama asal untuk carian
            hasil = cari_suku_kata(suku_kata, kategori)
            if hasil:
                df_hasil = pd.DataFrame(hasil)

                # Hadkan kepada maksimum 5 pantun
                df_hasil = df_hasil.head(5)

                # Paparkan hasil dalam jadual
                st.write(f"**📜 Menampilkan maksimum 5 pantun yang mengandungi '{suku_kata}' dalam kategori {kategori_pilihan}:**")
                selected_index = st.data_editor(df_hasil, use_container_width=True, num_rows="dynamic", key="pantun_table", selection_mode="single")

                # Apabila pengguna klik satu pantun, paparkan keseluruhan rangkap
                if selected_index:
                    selected_pantun = df_hasil.iloc[selected_index[0]]["pantun"]

                    # Tukarkan pantun kepada format serangkap (4 baris)
                    if isinstance(selected_pantun, str):
                        possible_separators = ["\n", ";", ","]  # Pemisah yang mungkin digunakan
                        for sep in possible_separators:
                            if sep in selected_pantun:
                                formatted_pantun = "\n".join(selected_pantun.split(sep))
                                break
                        else:
                            formatted_pantun = selected_pantun  # Jika tiada pemisah, paparkan asal

                        st.session_state.selected_pantun = formatted_pantun
            else:
                st.warning("❌ Tiada hasil dijumpai.")
        else:
            st.warning("⚠️ Sila masukkan suku kata untuk dicari.")

# **Paparan pantun di sebelah kanan (col2)**
with col2:
    if st.session_state.selected_pantun:
        st.subheader("📜 Pantun Terpilih:")
        st.write(st.session_state.selected_pantun)  # Gunakan st.write() untuk format automatik

# Footer
st.markdown('<div class="footer">© 2023-2025 Carian Suku Kata. v1. 2008-2025. Sebuah carian suku kata berguna untuk membantu pengguna mengarang pantun.</div>', unsafe_allow_html=True)
