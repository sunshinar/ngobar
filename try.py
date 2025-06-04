import tkinter as tk
from tkinter import ttk, messagebox
import json
import matplotlib.pyplot as plt

# --- Data Global
data_suhu = {}
filename = "data_suhu.json"
daftar_kota = ["JKT", "SBY", "MKS", "DPS", "ACH", "MDN", "DPK", "TGR"]
nama_kota_map = {
    "JKT": "Jakarta",
    "SBY": "Surabaya",
    "MKS": "Makassar",
    "DPS": "Denpasar",
    "ACH": "Aceh",
    "MDN": "Medan",
    "DPK": "Depok",
    "TGR": "Tangerang"
}

# --- Fungsi File
def simpan_data():
    with open(filename, 'w') as f:
        json.dump(data_suhu, f)

def baca_data():
    global data_suhu
    try:
        with open(filename, 'r') as f:
            data_suhu = json.load(f)
    except FileNotFoundError:
        data_suhu = {}

# --- Fungsi Tambah Data
def tambah_data():
    id_kota = combo_id.get().upper()
    hari = combo_hari.get()
    suhu = entry_suhu.get()

    if id_kota == "Pilih ID Kota" or hari == "Pilih Hari" or not suhu:
        messagebox.showwarning("Peringatan", "Isi semua data dengan benar!")
        return

    try:
        suhu = int(suhu)
    except ValueError:
        messagebox.showerror("Error", "Suhu harus berupa angka.")
        return

    if id_kota not in data_suhu:
        data_suhu[id_kota] = {}
    data_suhu[id_kota][hari] = suhu
    simpan_data()
    tampilkan_data()
    messagebox.showinfo("Sukses", f"Data untuk {id_kota} - {hari} ditambahkan.") 

# --- Fungsi Tampilkan Tabel
def tampilkan_data():
    for row in tree.get_children():
        tree.delete(row)
    for id_kota, hari_data in data_suhu.items():
        nama_kota = nama_kota_map.get(id_kota, "Tidak diketahui")
        for hari, suhu in hari_data.items():
            tree.insert('', 'end', values=(id_kota, nama_kota, hari, suhu))

# --- Fungsi Cari Data
def cari_data():
    id_kota = combo_cari_id.get().upper()
    if id_kota == "PILIH ID KOTA":
        messagebox.showwarning("Peringatan", "Silakan pilih ID Kota terlebih dahulu.")
        return
    if id_kota in data_suhu:
        hasil = data_suhu[id_kota]
        pesan = f"Data Suhu untuk {id_kota}:\n" + "\n".join([f"{h}: {s}°C" for h, s in hasil.items()])
        messagebox.showinfo("Hasil Pencarian", pesan)
    else:
        messagebox.showwarning("Tidak Ditemukan", f"Tidak ada data untuk ID {id_kota}.")

# --- Fungsi Grafik Rata-rata
def tampilkan_grafik_rata_rata():
    kota = []
    rata_rata = []

    for id_kota, suhu in data_suhu.items():
        rata = sum(suhu.values()) / len(suhu)
        kota.append(id_kota)
        rata_rata.append(rata)

    plt.figure(figsize=(8, 5))
    plt.barh(kota, rata_rata, color="#4682B4")
    plt.xlabel("Rata-rata Suhu (°C)")
    plt.ylabel("Kota")
    plt.title("Rata-rata Suhu Mingguan per Kota", fontsize=14, fontweight="bold")
    plt.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

# --- Fungsi Grafik per Kota
def tampilkan_grafik_per_kota():
    id_kota = combo_cari_id.get().upper()
    if id_kota == "PILIH ID KOTA":
        messagebox.showwarning("Peringatan", "Silakan pilih ID Kota terlebih dahulu.")
        return

    hari = list(data_suhu[id_kota].keys())
    suhu = list(data_suhu[id_kota].values())

    plt.figure(figsize=(8, 5))
    plt.barh(hari, suhu, color="#FFA07A")
    plt.xlabel("Suhu (°C)")
    plt.ylabel("Hari")
    plt.title(f"Suhu Harian - {id_kota}", fontsize=14, fontweight="bold")
    plt.grid(axis="x", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

# --- Inisialisasi GUI
baca_data()
root = tk.Tk()
root.title("Sistem Pemantauan Suhu Kota")
root.geometry("620x550")

# --- Frame Input
frame_input = tk.LabelFrame(root, text="Input Data Suhu", padx=10, pady=10)
frame_input.pack(padx=10, pady=5, fill="x")

tk.Label(frame_input, text="ID Kota:").grid(row=0, column=0, sticky="w")
combo_id = ttk.Combobox(frame_input, state="readonly", values=daftar_kota)
combo_id.set("Pilih ID Kota")  # 👉 placeholder
combo_id.grid(row=0, column=1)

tk.Label(frame_input, text="Hari:").grid(row=1, column=0, sticky="w")
combo_hari = ttk.Combobox(frame_input, state="readonly", values=["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"])
combo_hari.set("Pilih Hari")  # 👉 placeholder
combo_hari.grid(row=1, column=1)

tk.Label(frame_input, text="Suhu:").grid(row=2, column=0, sticky="w")
entry_suhu = tk.Entry(frame_input)
entry_suhu.grid(row=2, column=1)

btn_tambah = tk.Button(frame_input, text="Tambah Data", command=tambah_data, bg="lightblue")
btn_tambah.grid(row=3, column=0, columnspan=2, pady=5)

# --- Tabel TreeView
tree = ttk.Treeview(root, columns=('ID Kota', 'Nama Kota', 'Hari', 'Suhu'), show='headings', height=8)
tree.heading('ID Kota', text='ID Kota')
tree.heading('Nama Kota', text='Nama Kota')
tree.heading('Hari', text='Hari')
tree.heading('Suhu', text='Suhu (°C)')
tree.pack(padx=10, pady=10, fill="x")

# --- Frame Pencarian & Grafik
frame_search = tk.LabelFrame(root, text="Pencarian & Grafik", padx=10, pady=10)
frame_search.pack(padx=10, pady=5, fill="x")

tk.Label(frame_search, text="Cari ID Kota:").grid(row=0, column=0, sticky="w")
combo_cari_id = ttk.Combobox(frame_search, state="readonly", values=daftar_kota)
combo_cari_id.set("Pilih ID Kota")  # 👉 placeholder
combo_cari_id.grid(row=0, column=1)

btn_cari = tk.Button(frame_search, text="Cari", command=cari_data)
btn_cari.grid(row=0, column=2, padx=5)

btn_grafik = tk.Button(frame_search, text="Grafik Rata-rata", command=tampilkan_grafik_rata_rata, bg="lightgreen")
btn_grafik.grid(row=0, column=3, padx=5)

btn_grafik_perkota = tk.Button(frame_search, text="Grafik per Kota", command=tampilkan_grafik_per_kota, bg="lightyellow")
btn_grafik_perkota.grid(row=0, column=4, padx=5)

# --- Load Data Awal
tampilkan_data()
root.mainloop()