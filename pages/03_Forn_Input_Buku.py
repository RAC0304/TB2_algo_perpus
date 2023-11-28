import streamlit as st
import pymysql
from PIL import Image

st.set_page_config(page_title="Library Book Input Form",
                   page_icon="📚", layout="centered")

st.title("Library Book Input Form")

# Connect to MySQL
db = pymysql.connect(
    host='localhost',
    user='root',  # Replace with your MySQL username
    password='',  # Replace with your MySQL password
    database='perpustakaan'  # Replace with your MySQL database name
)
cursor = db.cursor()

# Function to create data in the database


def create_data(judul, pengarang, image, penerbit, tahun_terbit, kategori, stok):
    # Save the uploaded image to the ./assets/images/ directory
    if image is not None:
        image_content = image.read()  # Read the content of the image file
        image_name = image.name
        with open(f"./assets/images/{image_name}", "wb") as img_file:
            img_file.write(image_content)
    else:
        image_name = 'Belum ada gambar'

    # Insert the data into the MySQL database
    sql = "INSERT INTO buku (judul, pengarang, image, penerbit, tahun_terbit, kategori, stok) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (judul, pengarang, image_name,
           penerbit, tahun_terbit, kategori, stok)
    cursor.execute(sql, val)
    db.commit()


# Create a form for book information
form = st.form(key='book_input_form')

# Add input fields to the form
judul = form.text_input(label='Judul Buku', max_chars=255)
pengarang = form.text_input(label='Pengarang', max_chars=255)
image = form.file_uploader("Upload Book Cover Image",
                           type=["jpg", "jpeg", "png"])
penerbit = form.text_input(label='Penerbit', max_chars=255)
tahun_terbit = form.date_input(label='Tahun Terbit')
kategori = form.selectbox(
    label="Kategori",
    options=("Sejarah", "Dongeng", "Fiksi")
)
stok = form.number_input(label='Stok Buku', min_value=1)

# Add a submit button to the form
submitted = form.form_submit_button(label='Tambah')

# Process form submission
if submitted:
    create_data(judul, pengarang, image, penerbit,
                tahun_terbit, kategori, stok)
    st.snow()
    st.success("Data telah ditambahkan!")
