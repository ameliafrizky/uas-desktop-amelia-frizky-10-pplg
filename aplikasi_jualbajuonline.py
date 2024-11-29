import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Membuat atau menghubungkan ke database SQLite
conn = sqlite3.connect('jual_baju_online.db')
cursor = conn.cursor()

# Membuat tabel produk jika belum ada
cursor.execute("""
CREATE TABLE IF NOT EXISTS produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    kategori TEXT NOT NULL,
    harga REAL NOT NULL,
    stok INTEGER NOT NULL

)
""")
conn.commit()

# Fungsi CRUD
def tambah_produk():
    nama = entry_nama.get()
    kategori = entry_kategori.get()
    harga = entry_harga.get()
    stok = entry_stok.get()
    
    if not (nama and kategori and harga and stok):
        messagebox.showerror("Error", "Semua bidang harus diisi!")
        return
    
    try:
        cursor.execute("INSERT INTO produk (nama, kategori, harga, stok) VALUES (?, ?, ?, ?)",
                       (nama, kategori, float(harga), int(stok)))
        conn.commit()
        messagebox.showinfo("Sukses", "Produk berhasil ditambahkan!")
        clear_form()
        tampilkan_produk()
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

def tampilkan_produk():
    for item in tree_produk.get_children():
        tree_produk.delete(item)

    cursor.execute("SELECT * FROM produk")
    rows = cursor.fetchall()
    for row in rows:
        tree_produk.insert("", tk.END, values=row)

def hapus_produk():
    selected_item = tree_produk.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih produk yang ingin dihapus!")
        return

    data_id = tree_produk.item(selected_item, "values")[0]
    cursor.execute("DELETE FROM produk WHERE id=?", (data_id,))
    conn.commit() 
    tree_produk.delete(selected_item)
    messagebox.showinfo("Sukses", "Produk berhasil dihapus!")

def edit_produk():
    selected_item = tree_produk.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih produk yang ingin diedit!")
        return

    data_id = tree_produk.item(selected_item, "values")[0]
    nama = entry_nama.get()
    kategori = entry_kategori.get()
    harga = entry_harga.get()
    stok = entry_stok.get()

    if not (nama and kategori and harga and stok):
        messagebox.showerror("Error", "Semua bidang harus diisi!")
        return

    cursor.execute("UPDATE produk SET nama=?, kategori=?, harga=?, stok=? WHERE id=?",
                   (nama, kategori, float(harga), int(stok), data_id))
    conn.commit()
    messagebox.showinfo("Sukses", "Data produk berhasil diperbarui!")
    clear_form()
    tampilkan_produk()

def beli_produk():
    selected_item = tree_produk.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih produk yang ingin dibeli!")
        return

    data_id = tree_produk.item(selected_item, "values")[0]
    cursor.execute("SELECT stok FROM produk WHERE id=?", (data_id,))
    stok = cursor.fetchone()[0]

    if stok > 0:
        cursor.execute("UPDATE produk SET stok=stok-1 WHERE id=?", (data_id,))
        conn.commit()
        messagebox.showinfo("Sukses", "Produk berhasil dibeli!")
        tampilkan_produk()
    else:
        messagebox.showerror("Error", "Stok produk habis!")

def clear_form():
    entry_nama.delete(0, tk.END)
    entry_kategori.delete(0, tk.END)
    entry_harga.delete(0, tk.END)
    entry_stok.delete(0, tk.END)

# Membuat GUI
root = tk.Tk()
root.title("Aplikasi Jual Beli Baju Online")

# Logo
try:
    logo_image = Image.open ("logo (2).png")
    logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(root, image=logo_photo)
    logo_label.pack(pady=10)
except Exception as e:
    print(f"Error memuat logo: {e}")

# Frame Form
frame_form = tk.Frame(root, padx=10, pady=10)
frame_form.pack(fill=tk.X)

tk.Label(frame_form, text="Nama Produk:").grid(row=0, column=0, sticky=tk.W, pady=5)
entry_nama = tk.Entry(frame_form)
entry_nama.grid(row=0, column=1, padx=10)

tk.Label(frame_form, text="Kategori:").grid(row=1, column=0, sticky=tk.W, pady=5)
entry_kategori = tk.Entry(frame_form)
entry_kategori.grid(row=1, column=1, padx=10)

tk.Label(frame_form, text="Harga:").grid(row=2, column=0, sticky=tk.W, pady=5)
entry_harga = tk.Entry(frame_form)
entry_harga.grid(row=2, column=1, padx=10)

tk.Label(frame_form, text="Stok:").grid(row=3, column=0, sticky=tk.W, pady=5)
entry_stok = tk.Entry(frame_form)
entry_stok.grid(row=3, column=1, padx=10)

# Frame Tombol
frame_buttons = tk.Frame(root, padx=10, pady=10)
frame_buttons.pack(fill=tk.X)

btn_tambah = tk.Button(frame_buttons, text="Tambah Produk", command=tambah_produk, bg="green", fg="white")
btn_tambah.grid(row=0, column=0, padx=5)

btn_edit = tk.Button(frame_buttons, text="Edit Produk", command=edit_produk, bg="blue", fg="white")
btn_edit.grid(row=0, column=1, padx=5)

btn_hapus = tk.Button(frame_buttons, text="Hapus Produk", command=hapus_produk, bg="red", fg="white")
btn_hapus.grid(row=0, column=2, padx=5)

btn_beli = tk.Button(frame_buttons, text="Beli Produk", command=beli_produk, bg="purple", fg="white")
btn_beli.grid(row=0, column=3, padx=5)

btn_clear = tk.Button(frame_buttons, text="Clear Form", command=clear_form, bg="gray", fg="white")
btn_clear.grid(row=0, column=4, padx=5)

# Frame Tabel
frame_table = tk.Frame(root, padx=10, pady=10)
frame_table.pack(fill=tk.BOTH, expand=True)

columns = ("id", "nama", "kategori", "harga", "stok")
tree_produk = ttk.Treeview(frame_table, columns=columns, show="headings", height=8)
tree_produk.pack(fill=tk.BOTH, expand=True)

tree_produk.heading("id", text="ID")
tree_produk.column("id", width=50, anchor=tk.CENTER)

tree_produk.heading("nama", text="Nama Produk")
tree_produk.column("nama", width=150, anchor=tk.W)

tree_produk.heading("kategori", text="Kategori")
tree_produk.column("kategori", width=100, anchor=tk.W)

tree_produk.heading("harga", text="Harga")
tree_produk.column("harga", width=100, anchor=tk.CENTER)

tree_produk.heading("stok", text="Stok")
tree_produk.column("stok", width=100, anchor=tk.CENTER)

tampilkan_produk()

def cari_produk():
    # Mengambil kata kunci dari input pencarian
    keyword = entry_cari.get().strip()
    if not keyword:
        messagebox.showerror("Error", "Masukkan kata kunci untuk pencarian!")
        return
    
    # Membersihkan tabel sebelum menampilkan hasil pencarian
    for item in tree_produk.get_children():
        tree_produk.delete(item)
    
    # Menjalankan query pencarian
    cursor.execute("SELECT * FROM produk WHERE nama LIKE ?", (f"%{keyword}%",))
    rows = cursor.fetchall()
    
    if rows:
        for row in rows:
            tree_produk.insert("", tk.END, values=row)
    else:
        messagebox.showinfo("Info", "Produk tidak ditemukan!")

def reset_tampilan():
    # Membersihkan kata kunci pencarian dan menampilkan semua produk
    entry_cari.delete(0, tk.END)
    tampilkan_produk()

# Menambahkan elemen pencarian
frame_search = tk.Frame(root, padx=10, pady=10)
frame_search.pack(fill=tk.X)

tk.Label(frame_search, text="Cari Produk:").pack(side=tk.LEFT, padx=5)
entry_cari = tk.Entry(frame_search, width=30)
entry_cari.pack(side=tk.LEFT, padx=5)

btn_cari = tk.Button(frame_search, text="Cari", command=cari_produk, bg="orange", fg="white")
btn_cari.pack(side=tk.LEFT, padx=5)

btn_reset = tk.Button(frame_search, text="Reset", command=reset_tampilan, bg="gray", fg="white")
btn_reset.pack(side=tk.LEFT, padx=5)

# Frame Tabel
frame_table = tk.Frame(root, padx=10, pady=10)
frame_table.pack(fill=tk.BOTH, expand=True)

columns = ("id", "nama", "kategori", "harga", "stok")
tree_produk = ttk.Treeview(frame_table, columns=columns, show="headings", height=8)
tree_produk.pack(fill=tk.BOTH, expand=True)

tree_produk.heading("id", text="ID")
tree_produk.column("id", width=50, anchor=tk.CENTER)

tree_produk.heading("nama", text="Nama Produk")
tree_produk.column("nama", width=150, anchor=tk.W)

tree_produk.heading("kategori", text="Kategori")
tree_produk.column("kategori", width=100, anchor=tk.W)

tree_produk.heading("harga", text="Harga")
tree_produk.column("harga", width=100, anchor=tk.CENTER)

tree_produk.heading("stok", text="Stok")
tree_produk.column("stok", width=100, anchor=tk.CENTER)

tampilkan_produk()

# Menjalankan aplikasi
root.mainloop()
