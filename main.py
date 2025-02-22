import tkinter as tk
from tkinter import ttk, messagebox
from functions import cari_suku_kata

# Fungsi carian yang dipanggil apabila butang ditekan
def buat_carian():
    suku_kata = entry_carian.get().strip()
    kategori = combo_kategori.get()
    if not suku_kata or not kategori:
        messagebox.showwarning("Amaran", "Sila masukkan suku kata dan pilih kategori!")
        return

    hasil = cari_suku_kata(suku_kata, kategori)
    text_output.delete(1.0, tk.END)
    if hasil:
        for item in hasil:
            text_output.insert(tk.END, f"{item['kategori']}: {item['perkataan']}\nPantun: {item['pantun']}\n\n")
    else:
        text_output.insert(tk.END, "Tiada hasil dijumpai.")

# Bina GUI
root = tk.Tk()
root.title("Carian Suku Kata Pantun")
root.geometry("600x400")

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Masukkan Suku Kata:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_carian = ttk.Entry(frame, width=20)
entry_carian.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame, text="Pilih Kategori:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
combo_kategori = ttk.Combobox(frame, values=["RIMA_TENGAH_1", "RIMA_TENGAH_2", "RIMA_TENGAH_3", "RIMA_TENGAH_4",
                                             "RIMA_AKHIR_1", "RIMA_AKHIR_2", "RIMA_AKHIR_3", "RIMA_AKHIR_4"], state="readonly")
combo_kategori.grid(row=1, column=1, padx=5, pady=5)

btn_cari = ttk.Button(frame, text="Cari", command=buat_carian)
btn_cari.grid(row=2, column=0, columnspan=2, pady=10)

text_output = tk.Text(frame, height=15, width=70)
text_output.grid(row=3, column=0, columnspan=2, pady=5)

root.mainloop()
