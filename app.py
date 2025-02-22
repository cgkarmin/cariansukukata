import streamlit as st
import pandas as pd
from functions import cari_suku_kata  # Pastikan fungsi ini tersedia

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Carian Suku Kata Pantun", layout="wide")

# Tambahkan CSS untuk mengunci ukuran input dan dropdown
st.markdown(
    """
    <style>
    /* Kunci lebar input */
    div[data-baseweb="input"] {
        width: 320px !important;  /* Ukuran tetap */
        max-width: 320px !important;
        margin: auto;
    }

    /* Kunci lebar dropdown */
    div[data-baseweb="select"] {
        width: 220px !important;  /* Ukuran tetap */
        max-width: 220px !important;
        margin: auto;
    }

    /* Pusatkan tombol "Cari" */
    div.stButton > button {
        display: block;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Judul aplikasi
st.markdown("<h1 style='text-align: center;'>🔍 Carian Suku Kata dalam Pantun</h1>", unsafe_allow_html=True)

# Layout input dan dropdown agar ukurannya tidak melebar
col1, col2, col3 = st.columns([1, 3, 1])  # Kolom tengah lebih besar agar input tidak melebar

with col2:  # Input di tengah
    col_input, col_dropdown = st.columns([3, 2])  # Input lebih lebar dari dropdown

    with col_input:
        suku_kata = st.text_input("Masukkan Suku Kata", "", max_chars=10, help="Masukkan suku kata yang ingin dicari")

    with col_dropdown:
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

# Tombol pencarian di tengah
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if st.button("Cari"):
    if suku_kata:
        kategori = pilihan_kategori[kategori_pilihan]
        hasil = cari_suku_kata(suku_kata, kategori)

        if hasil:
            df_hasil = pd.DataFrame(hasil)
            df_hasil = df_hasil.head(5)  # Menampilkan hanya 5 pantun pertama

            # Tampilkan hasil
            st.write(f"Menampilkan maksimum 5 pantun yang mengandungi '{suku_kata}' dalam kategori {kategori_pilihan}:")
            selected_rows = st.data_editor(df_hasil, use_container_width=True, key="pantun_table", selection_mode="single")

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
            st.warning("⚠️ Tiada hasil dijumpai.")
    else:
        st.warning("⚠️ Sila masukkan suku kata untuk dicari.")
st.markdown("</div>", unsafe_allow_html=True)

# Tampilan pantun yang dipilih
if "selected_pantun" in st.session_state and st.session_state.selected_pantun:
    st.subheader("📜 Pantun Terpilih:")
    st.write(st.session_state.selected_pantun)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 12px;'>© 2023-2025 Carian Suku Kata. Sebuah carian suku kata untuk membantu pengguna mengarang pantun.</p>",
    unsafe_allow_html=True
)
