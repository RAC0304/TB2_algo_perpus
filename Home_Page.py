import streamlit as st
import pymysql
import pandas as pd
from PIL import Image

db = pymysql.connect(
    host='localhost',
    user='root',  # Replace with your MySQL username
    password='',  # Replace with your MySQL password
    database='perpustakaan'  # Replace with your MySQL database name
)
cursor = db.cursor()

# Function to create a SQLite connection and fetch book data
def read_data():
    cursor.execute("SELECT * FROM buku")
    result = cursor.fetchall()
    columns = [col[0] for col in cursor.description]  # Get column names from the cursor
    df = pd.DataFrame(result, columns=columns)
    return df

st.set_page_config(page_title="Home Page", page_icon="📚", layout="centered")

st.title(body="📚Selamat Datang Di Perpustakaan")
st.title("📚Minimalism")
st.write("Berikut ini adalah daftar buku yang tersedia di perpustakaan kami")

# Fetch book data from the database
book_data = read_data()

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
