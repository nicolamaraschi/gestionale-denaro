import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt

# URL del backend Flask
BASE_URL = "http://localhost:5000"

# Funzione per inviare una nuova spesa al server
def aggiungi_spesa():
    categoria = entry_categoria.get()
    importo = entry_importo.get()
    if categoria and importo:
        try:
            importo = float(importo)
            response = requests.post(f'{BASE_URL}/add_spesa', json={'categoria': categoria, 'importo': importo})
            if response.status_code == 200:
                messagebox.showinfo("Successo", "Spesa aggiunta con successo")
                entry_categoria.delete(0, tk.END)
                entry_importo.delete(0, tk.END)
            else:
                messagebox.showerror("Errore", "Errore durante l'aggiunta della spesa")
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un importo valido")
    else:
        messagebox.showerror("Errore", "Tutti i campi sono obbligatori")

# Funzione per inviare lo stipendio al server
def aggiungi_stipendio():
    importo = entry_stipendio.get()
    if importo:
        try:
            importo = float(importo)
            response = requests.post(f'{BASE_URL}/add_stipendio', json={'importo': importo})
            if response.status_code == 200:
                messagebox.showinfo("Successo", "Stipendio aggiunto con successo")
                entry_stipendio.delete(0, tk.END)
            else:
                messagebox.showerror("Errore", "Errore durante l'aggiunta dello stipendio")
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un importo valido")
    else:
        messagebox.showerror("Errore", "L'importo è obbligatorio")

# Funzione per visualizzare le spese per categoria
def visualizza_spese_categorie():
    response = requests.get(f'{BASE_URL}/get_spese_categorie')
    if response.status_code == 200:
        spese_categorie = response.json()
        categorie = list(spese_categorie.keys())
        importi = list(spese_categorie.values())
        plt.figure(figsize=(10, 5))
        plt.bar(categorie, importi, color='blue')
        plt.xlabel('Categoria')
        plt.ylabel('Importo (€)')
        plt.title('Spese per Categoria')
        plt.show()
    else:
        messagebox.showerror("Errore", "Errore durante il recupero delle spese per categoria")

# Funzione per visualizzare lo storico mensile delle spese
def visualizza_storico_mensile():
    response = requests.get(f'{BASE_URL}/get_storico_mensile')
    if response.status_code == 200:
        storico_mensile = response.json()
        mesi = list(storico_mensile.keys())
        importi = list(storico_mensile.values())
        plt.figure(figsize=(10, 5))
        plt.plot(mesi, importi, marker='o', linestyle='-', color='green')
        plt.xlabel('Mese')
        plt.ylabel('Importo (€)')
        plt.title('Storico Mensile delle Spese')
        plt.show()
    else:
        messagebox.showerror("Errore", "Errore durante il recupero dello storico mensile")

# Creazione dell'interfaccia grafica
root = tk.Tk()
root.title("Gestione Finanze")

# Sezione Aggiungi Spesa
frame_spesa = tk.Frame(root)
frame_spesa.pack(pady=10)
tk.Label(frame_spesa, text="Categoria Spesa").grid(row=0, column=0, padx=5)
entry_categoria = tk.Entry(frame_spesa)
entry_categoria.grid(row=0, column=1, padx=5)
tk.Label(frame_spesa, text="Importo (€)").grid(row=1, column=0, padx=5)
entry_importo = tk.Entry(frame_spesa)
entry_importo.grid(row=1, column=1, padx=5)
btn_spesa = tk.Button(frame_spesa, text="Aggiungi Spesa", command=aggiungi_spesa)
btn_spesa.grid(row=2, columnspan=2, pady=5)

# Sezione Aggiungi Stipendio
frame_stipendio = tk.Frame(root)
frame_stipendio.pack(pady=10)
tk.Label(frame_stipendio, text="Stipendio (€)").grid(row=0, column=0, padx=5)
entry_stipendio = tk.Entry(frame_stipendio)
entry_stipendio.grid(row=0, column=1, padx=5)
btn_stipendio = tk.Button(frame_stipendio, text="Aggiungi Stipendio", command=aggiungi_stipendio)
btn_stipendio.grid(row=1, columnspan=2, pady=5)

# Sezione Visualizza Grafici
frame_grafici = tk.Frame(root)
frame_grafici.pack(pady=10)
btn_spese_categorie = tk.Button(frame_grafici, text="Visualizza Spese per Categoria", command=visualizza_spese_categorie)
btn_spese_categorie.pack(pady=5)
btn_storico_mensile = tk.Button(frame_grafici, text="Visualizza Storico Mensile", command=visualizza_storico_mensile)
btn_storico_mensile.pack(pady=5)

root.mainloop()
