import streamlit as st
import pymysql
import pandas as pd
from PIL import Image

# Membuat koneksi ke database MySQL
db = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='perpustakaan'
)

# Membuat objek cursor
cursor = db.cursor()

# Fungsi untuk menambahkan user ke tabel login
def add_user(username, password):
    cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
    db.commit()

# Fungsi untuk melakukan login
def login(username, password):
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()

    if user and password == user[2]:
        # Perhatikan bahwa tidak perlu memanggil login(username) di sini
        id_anggota = user[0]  # Ambil id_anggota dari hasil query
        st.session_state.id_anggota = id_anggota
        return id_anggota
    else:
        return False

# Streamlit UI
st.set_page_config(page_title="Home Page", page_icon="📚", layout="centered")

# Form untuk login
st.title("Login")

username = st.text_input('Username:')
password = st.text_input('Password:', type='password')

login_button = st.button('Login')

# Deklarasi variabel app_mode
app_mode = ""

if login_button:
    id_anggota = login(username, password)  # Perbaiki pemanggilan fungsi login
    if id_anggota:
        st.success('Login berhasil!')
        app_mode = "daftar_buku"
    else:
        st.error('Login gagal. Silakan cek kembali username dan password Anda.')
        app_mode = "login"

# Hanya menampilkan bagian ini jika login berhasil
if app_mode == "daftar_buku":
    st.title(body="📚Selamat Datang Di Perpustakaan")
    st.title("📚Minimalism")
    st.write("Berikut ini adalah daftar buku yang tersedia di perpustakaan kami")

    # Fetch book data from the database
    cursor.execute("SELECT * FROM buku")
    result = cursor.fetchall()
    columns = [col[0] for col in cursor.description]  # Get column names from the cursor
    book_data = pd.DataFrame(result, columns=columns)

    # Loop through the book data and display information
    for index, row in book_data.iterrows():
        cols = st.columns((1, 1, 1))

        # Check if the image file exists
        if row["image"]:
            cols[0].image(f'assets/images/{row["image"]}', use_column_width=True, caption="Book Cover")
        else:
            cols[0].write("Tidak ada gambar tersedia")

        cols[1].write(f"Judul: {row['judul']}")
        cols[1].write(f"Pengarang: {row['pengarang']}")
        cols[1].write(f"Penerbit: {row['penerbit']}")
        cols[1].write(f"Tahun Terbit: {row['tahun_terbit']}")
        cols[1].write(f"Tersedia: {row['stok']} Buku")
        cols[1].write(f"**Kategori:** {row['kategori']} Buku")

        # Add more details as needed

        # Add a separator between books
        st.markdown("---")
