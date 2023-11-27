import time
import os
from fpdf import FPDF
import pymysql
import pandas as pd
import streamlit as st

# Membuat koneksi ke database MySQL
db = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='perpustakaan'
)

# Membuat objek cursor
cursor = db.cursor()

def pinjam_buku():
    # Dapatkan id_anggota dari session_state
    return st.session_state.id_anggota

st.set_page_config(page_title="Menu Peminjaman Buku", page_icon="📖", layout="centered")

arynama, aryjudul, arytglpinjam, arytglkembali = [], [], [], []
st.empty()
st.title("📖 Menu Peminjaman Buku")
st.write("Silahkan Masukkan Data Diri Anda")
form1 = st.form(key="annotation1", clear_on_submit=True)

# Fetch book data from the database
cursor.execute("SELECT * FROM buku")
result = cursor.fetchall()
columns = [col[0] for col in cursor.description]  # Get column names from the cursor
book_data = pd.DataFrame(result, columns=columns)

# Ambil kolom 'judul' dari DataFrame dan konversi ke list
judul_buku_list = book_data['judul'].tolist()

id_anggota = pinjam_buku()  # Tidak perlu memberikan parameter
with form1:
    cols = st.columns((1, 1))
    nama = cols[0].text_input("Nama Lengkap :")
    judul = cols[1].selectbox('Pilih Judul Buku', ['', *judul_buku_list])

    # Dapatkan id_buku berdasarkan judul
    filtered_data = book_data.loc[book_data['judul'] == judul, 'id_buku'].values

    if len(filtered_data) > 0:
        id_buku = filtered_data[0]
    
        # st.error('Buku tidak ditemukan.')
        # Keluar dari fungsi jika buku tidak ditemukan
      

    cols = st.columns(2)
    tglpinjam = cols[0].date_input("Tanggal Peminjaman :")
    tglkembali = cols[1].date_input("Tanggal Kembali :")
    submitted = st.form_submit_button(label="Submit")

    if submitted:
        cursor.execute("INSERT INTO pinjam_buku(id_anggota, id_buku, nama_pinjam, tanggal_pinjam, tanggal_kembali, status) VALUES (%s,%s,%s,%s,%s,%s)", (id_anggota, id_buku,nama, tglpinjam, tglkembali, 'belum dikembalikan'))
        db.commit()
        st.success(
            "Terimakasih sudah meminjam buku di perpustakaan Minimalism! Jangan lupa simpan struk peminjaman ya")
        st.balloons()
        for i in range(1):
            arynama.append(nama)
            aryjudul.append(judul)
            arytglpinjam.append(tglpinjam)
            arytglkembali.append(tglkembali)

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt="************************  PERPUS MINIMALISM  ************************", ln=True,
                     align='C')
            pdf.cell(200, 10, txt="************ Sistem Peminjaman Buku Perpustakaan Digital ************", ln=True,
                     align='C')
            pdf.cell(200, 10, txt="************************ Struk Bukti Pinjam *************************", ln=True,
                     align='C')
            pdf.ln(10)

            pdf.cell(200, 10, txt=f'Tanggal : {tglpinjam}', ln=True)
            pdf.cell(200, 10, txt=f'Nama Peminjam Buku : {nama}', ln=True)
            pdf.cell(200, 10, txt=f'Judul Buku : {judul}', ln=True)
            pdf.cell(200, 10, txt=f'Tanggal Peminjaman : {tglpinjam}', ln=True)
            pdf.cell(200, 10, txt=f'Tanggal Kembali : {tglkembali}', ln=True)
            pdf.ln(10)

            pdf.cell(200, 10, txt='---Terima Kasih Telah Meminjam Buku Ditempat Kami---', ln=True)
            pdf.cell(200, 10, txt='---Struk Harap Dibawa pada saat pengembalian Buku---', ln=True)

            pdf_file_path = f"struk-{nama}-{str(tglpinjam)}.pdf"
            pdf.output(pdf_file_path)

            os.system(pdf_file_path)

if __name__ == "__main__":
    pinjam_buku()
