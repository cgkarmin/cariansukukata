import streamlit as st
import pandas as pd
from functions import cari_suku_kata  # Pastikan modul ini ada

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Carian Suku Kata Pantun", layout="wide")

# Judul aplikasi
st.markdown("<h1 style='text-align: center;'>🔍 Carian Suku Kata dalam Pantun</h1>", unsafe_allow_html=True)

# Susun layout dalam 2 kolom (satu untuk input pencarian dan kategori, satu untuk hasil)
col1, col2 = st.columns([1, 2])  # Col1 lebih kecil, Col2 lebih lebar

with col1:
    # Buat layout pencarian lebih ringkas
    c1, c2 = st.columns([2, 1])  # Pembagian layout untuk pencarian dan kategori

    with c1:
        suku_kata = st.text_input("Masukkan Suku Kata", "", max_chars=10, help="Masukkan suku kata yang ingin dicari")

    with c2:
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
        kategori_pilihan = st.selectbox("Pilih Kategori", list(pilihan_kategori.keys()), help="Pilih jenis rima yang ingin dicari")

    # Simpan pantun terpilih dalam sesi Streamlit
    if "selected_pantun" not in st.session_state:
        st.session_state.selected_pantun = ""

    # Tombol pencarian
    if st.button("Cari"):
        if suku_kata:
            kategori = pilihan_kategori[kategori_pilihan]  # Konversi kembali ke nama asli untuk pencarian
            hasil = cari_suku_kata(suku_kata, kategori)

            if hasil:
                df_hasil = pd.DataFrame(hasil)

                # Tampilkan hanya 5 hasil teratas
                df_hasil = df_hasil.head(5)

                # Menampilkan tabel hasil
                st.write(f"Menampilkan maksimum 5 pantun yang mengandungi '{suku_kata}' dalam kategori {kategori_pilihan}:")
                selected_rows = st.data_editor(df_hasil, use_container_width=True, key="pantun_table", selection_mode="single")

                # Jika pengguna memilih satu pantun, tampilkan dalam format serangkap (4 baris)
                selected_rows = st.session_state.get("pantun_table", {}).get("selected_rows", [])
                if selected_rows and len(selected_rows) > 0:
                    selected_pantun = df_hasil.iloc[selected_rows[0]]["pantun"]

                    # Format pantun agar tampil per baris
                    if isinstance(selected_pantun, str):
                        possible_separators = ["\n", ";", ","]
                        for sep in possible_separators:
                            if sep in selected_pantun:
                                formatted_pantun = "\n".join(selected_pantun.split(sep))
                                break
                        else:
                            formatted_pantun = selected_pantun

                        st.session_state.selected_pantun = formatted_pantun
            else:
                st.warning("❌ Tiada hasil dijumpai.")
        else:
            st.warning("⚠️ Sila masukkan suku kata untuk dicari.")

# **Tampilan pantun di sebelah kanan (col2)**
with col2:
    if st.session_state.selected_pantun:
        st.subheader("📜 Pantun Terpilih:")
        st.write(st.session_state.selected_pantun)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 12px;'>© 2023-2025 Carian Suku Kata. Sebuah carian suku kata untuk membantu pengguna mengarang pantun.</p>",
    unsafe_allow_html=True
)
