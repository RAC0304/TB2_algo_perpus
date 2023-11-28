import streamlit as st
import pymysql
import pandas as pd
# import datetime
# from fpdf import FPDF
# import os

# Membuat koneksi ke database MySQL
db = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='perpustakaan'
)

# Membuat objek cursor
cursor = db.cursor()

# Fetch specific columns from the database (nama_pinjam, tanggal_pinjam, tanggal_kembali, status)
query = """
    SELECT users.nama,
           buku.judul, 
           pinjam_buku.nama_pinjam, pinjam_buku.tanggal_pinjam, pinjam_buku.tanggal_kembali, pinjam_buku.status
    FROM pinjam_buku
    INNER JOIN buku ON pinjam_buku.id_buku = buku.id_buku
    INNER JOIN users ON pinjam_buku.id_anggota = users.id_anggota
"""
cursor.execute(query)
result = cursor.fetchall()
columns = ['Pengurus', 'Judul', 'Nama Peminjam', 'Tanggal Pinjam', 'Tanggal Kembali', 'Status']
book_data = pd.DataFrame(result, columns=columns)

# Menetapkan nomor baris index dimulai dari 1
book_data.index = book_data.index + 1

# Menampilkan data pinjam_buku menggunakan Streamlit dengan pagination
st.write("### Data Peminjaman Buku")

# Menentukan jumlah baris per halaman (page)
rows_per_page = 10

# Menampilkan tabel dengan pagination
page_number = st.number_input("Masukkan Nomor Halaman", min_value=1, value=1)
start_index = (page_number - 1) * rows_per_page
end_index = start_index + rows_per_page
st.table(book_data[start_index:end_index])

# Menampilkan informasi jumlah halaman
total_pages = int(len(book_data) / rows_per_page) + (len(book_data) % rows_per_page > 0)
st.write(f"Total Halaman: {total_pages}")

# Menutup koneksi database
db.close()


# # Membuat laporan PDF
# class PDF(FPDF):
#     def header(self):
#         self.set_font('Arial', 'B', 12)
#         self.cell(0, 10, 'Laporan Data Peminjaman Buku', 0, 1, 'C')
#
#     def footer(self):
#         self.set_y(-15)
#         self.set_font('Arial', 'I', 8)
#         self.cell(0, 10, 'Halaman %s' % self.page_no(), 0, 0, 'C')


# # Membuat laporan PDF dengan orientasi Landscape
# pdf = PDF(orientation='L')
# pdf.add_page()
#
#
#
# # Menambahkan header tabel ke laporan
# pdf.set_font('Arial', 'B', 11)
# pdf.cell(15, 10, txt='No', ln=False)
# pdf.cell(30, 10, txt='Judul', ln=False)
# pdf.cell(30, 10, txt='Nama Pengurus', ln=False)
# pdf.cell(30, 10, txt='Nama Peminjam', ln=False)
# pdf.cell(30, 10, txt='Tanggal Pinjam', ln=False)
# pdf.cell(35, 10, txt='Tanggal Kembali', ln=False)
# pdf.cell(40, 10, txt='Status', ln=True)
#
# # Menambahkan data tabel ke laporan
# pdf.set_font('Arial', '', 11)
# for index, row in book_data.iterrows():
#     pdf.cell(15, 10, str(index), ln=False)
#     for col in columns:
#         pdf.cell(35, 10, str(row[col]), ln=False)
#     pdf.ln()
#
# # Simpan laporan PDF di folder 'laporan'
# pdf_output_folder = 'laporan'
# tgl_sekarang = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# pdf_output_path = os.path.join(pdf_output_folder, f'laporan_peminjaman_buku_{tgl_sekarang}.pdf')
#
# # Pastikan folder 'laporan' sudah ada
# os.makedirs(pdf_output_folder, exist_ok=True)
#
# # Simpan laporan PDF
# pdf.output(pdf_output_path)
#
# # Tampilkan link download laporan PDF dengan lokasi yang diarahkan
# st.markdown(f"**[Download Laporan PDF]({pdf_output_path})**")
