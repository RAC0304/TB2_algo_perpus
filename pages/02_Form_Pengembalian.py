import time
import sys
import os
import datetime
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

def balik_buku():
    # Dapatkan id_anggota dari session_state
    return st.session_state.id_anggota

st.set_page_config(page_title="Menu Pengembalian Buku", page_icon="📄", layout="centered")

arynama, aryjudul, arytglpinjam, arytglkembali = [], [], [], []
st.empty()
st.title("📄 Menu Pengembalian Buku")
st.write("Silahkan Masukkan Data Diri Anda")
form2 = st.form(key="annotation2", clear_on_submit=True)

# Fetch book data from the database
cursor.execute("SELECT * FROM buku")
result = cursor.fetchall()
columns = [col[0] for col in cursor.description]  # Get column names from the cursor
book_data = pd.DataFrame(result, columns=columns)

# Ambil kolom 'judul' dari DataFrame dan konversi ke list
judul_buku_list = book_data['judul'].tolist()

id_anggota = balik_buku()  # Tidak perlu memberikan parameter

with form2:
    nama = form2.text_input("Nama Lengkap :")
    judul = form2.selectbox('Pilih Judul Buku', ['', *judul_buku_list])

    # Dapatkan id_buku berdasarkan judul
    filtered_data = book_data.loc[book_data['judul'] == judul, 'id_buku'].values

    if len(filtered_data) > 0:
        id_buku = filtered_data[0]
 

    tanggal_kembali = form2.date_input("Tanggal Deadline Pengembalian :")
    submitted = form2.form_submit_button(label="Submit")
    tglskg = datetime.datetime.now()
    tglkembali = tanggal_kembali
    tglkembali = str(tglkembali)
    tglWajib = tglkembali.split('-')

    tglWajib[0] = int(tglWajib[0])
    tglWajib[1] = int(tglWajib[1])
    tglWajib[2] = int(tglWajib[2])

    selisihTahun = tglskg.year - tglWajib[0]
    selisihBulan = tglskg.month - tglWajib[1]
    selisihTanggal = tglskg.day - tglWajib[2]

    totalHari = (selisihTahun * 365 + selisihBulan * 30 + selisihTanggal)

    denda = 0

    if totalHari > 0:
        denda = 5000 * totalHari

    if submitted:
        if denda == 0:
            # Proses pengembalian buku
            cursor.execute("UPDATE pinjam_buku SET status = 'sudah dikembalikan' WHERE id_anggota = %s AND id_buku = %s AND tanggal_kembali = %s",(id_anggota, id_buku, tanggal_kembali),)
            db.commit()
            st.success("Terimakasih sudah mengembalikan buku tepat pada waktunya!")
            st.balloons()
        else:
            st.success("Anda terlambat mengembalikan buku sebanyak " + str(totalHari) + " hari, maka harap membayar denda sebesar " + str(denda) + " rupiah")

