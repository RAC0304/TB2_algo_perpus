import time
import sys
import os
import datetime
from fpdf import FPDF
import streamlit as st

st.set_page_config(page_title="Menu Peminjaman Buku", page_icon="📖", layout="centered")

arynama, aryjudul, arytglpinjam, arytglkembali = [], [], [], []
st.empty()
st.title("📖 Menu Peminjaman Buku")
st.write("Silahkan Masukkan Data Diri Anda")
form1 = st.form(key="annotation1", clear_on_submit=True)

with form1:
    cols = st.columns((1, 1))
    nama = cols[0].text_input("Nama Lengkap :")
    judul = cols[1].selectbox('Pilih Judul Buku',
                              ('', 'The Great Gatsby by F. Scott Fitzgerald', 'To Kill a Mockingbird by Harper Lee',
                               '1984 by George Orwell', 'Pride and Prejudice by Jane Austen',
                               'The Catcher in the Rye by J.D. Salinger', 'Little Women by Lousia May Alcott',
                               'Poor Dad Rich Dad by Robert T. Kiyosaki', 'Atomic Habits by James Clear',
                               'Moby Dick by Herman Melvile', 'Sapiens by Yuval Noah Harari'))
    cols = st.columns(2)
    tglpinjam = cols[0].date_input("Tanggal Peminjaman :")
    tglkembali = cols[1].date_input("Tanggal Kembali :")
    submitted = st.form_submit_button(label="Submit")

    if submitted:
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
