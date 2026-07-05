import customtkinter as ctk
from tkinter import messagebox, filedialog
import subprocess
import os
import ctypes 
import _ctypes

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Metoda Newtona - Arytmetyka Przedziałowa")
        self.geometry("950x700") 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(16, weight=1) 

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Rozwiązywania równania nieliniowego\nmetodą Newtona", font=ctk.CTkFont(size=18, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 30))

        self.label_func = ctk.CTkLabel(self.sidebar_frame, text="1. Plik funkcji (.dll):", font=ctk.CTkFont(weight="bold"))
        self.label_func.grid(row=1, column=0, padx=20, pady=(0, 5), sticky="w")
        
        self.entry_dll = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Ścieżka do .dll")
        self.entry_dll.grid(row=2, column=0, padx=20, pady=(0, 5), sticky="ew")
        
        self.btn_file = ctk.CTkButton(self.sidebar_frame, text="Wybierz plik", command=self.wybierz_plik)
        self.btn_file.grid(row=3, column=0, padx=20, pady=(0, 5), sticky="ew")

        # NOWA ETYKIETA: Pokazuje jaka to funkcja!
        self.label_loaded_func = ctk.CTkLabel(self.sidebar_frame, text="Wzór: (nie wczytano)", font=ctk.CTkFont(slant="italic", size=12), text_color="gray")
        self.label_loaded_func.grid(row=4, column=0, padx=20, pady=(0, 15), sticky="w")

        self.label_mode = ctk.CTkLabel(self.sidebar_frame, text="2. Wybierz tryb obliczeń:", font=ctk.CTkFont(weight="bold"))
        self.label_mode.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="w")

        self.var_tryb = ctk.StringVar(value="1")
        self.rb1 = ctk.CTkRadioButton(self.sidebar_frame, text="Zwykłe (mpreal)", variable=self.var_tryb, value="1")
        self.rb1.grid(row=6, column=0, padx=30, pady=5, sticky="w")
        self.rb2 = ctk.CTkRadioButton(self.sidebar_frame, text="Przedziałowe (dane Rzeczywiste)", variable=self.var_tryb, value="2")
        self.rb2.grid(row=7, column=0, padx=30, pady=5, sticky="w")
        self.rb3 = ctk.CTkRadioButton(self.sidebar_frame, text="Przedziałowe (dane Przedziałowe)", variable=self.var_tryb, value="3")
        self.rb3.grid(row=8, column=0, padx=30, pady=(5, 20), sticky="w")

        self.label_data = ctk.CTkLabel(self.sidebar_frame, text="3. Punkt startowy (x0 lub a;b):", font=ctk.CTkFont(weight="bold"))
        self.label_data.grid(row=9, column=0, padx=20, pady=(0, 5), sticky="w")
        
        self.entry_data = ctk.CTkEntry(self.sidebar_frame, placeholder_text="np. 1.5 lub 1.4;1.6")
        self.entry_data.insert(0, "")
        self.entry_data.grid(row=10, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.label_iter = ctk.CTkLabel(self.sidebar_frame, text="4. Liczba iteracji:", font=ctk.CTkFont(weight="bold"))
        self.label_iter.grid(row=11, column=0, padx=20, pady=(0, 5), sticky="w")

        self.entry_iter = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Iteracje")
        self.entry_iter.insert(0, "100")
        self.entry_iter.grid(row=12, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.label_eps = ctk.CTkLabel(self.sidebar_frame, text="5. Epsilon (dokładność):", font=ctk.CTkFont(weight="bold"))
        self.label_eps.grid(row=13, column=0, padx=20, pady=(0, 5), sticky="w")

        self.entry_eps = ctk.CTkEntry(self.sidebar_frame, placeholder_text="np. 1e-10")
        self.entry_eps.insert(0, "1e-10")
        self.entry_eps.grid(row=14, column=0, padx=20, pady=(0, 15), sticky="ew")

        self.btn_run = ctk.CTkButton(self.sidebar_frame, text="OBLICZ WYNIKI", command=self.oblicz, 
                                     fg_color="#28a745", hover_color="#218838", height=40, font=ctk.CTkFont(weight="bold"))
        self.btn_run.grid(row=15, column=0, padx=20, pady=20, sticky="sew")

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.label_results = ctk.CTkLabel(self.main_frame, text="Wyniki oraz iteracje:", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_results.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.txt_output = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont(family="Consolas", size=13))
        self.txt_output.grid(row=1, column=0, sticky="nsew")

    def wybierz_plik(self):
        filepath = filedialog.askopenfilename(title="Wybierz bibliotekę DLL", filetypes=[("Pliki DLL", "*.dll")])
        if filepath:
            self.entry_dll.delete(0, ctk.END)
            self.entry_dll.insert(0, filepath)
            
            try:
                dll = ctypes.CDLL(filepath)
                dll.get_info.restype = ctypes.c_char_p 
                nazwa = dll.get_info().decode('utf-8')
                self.label_loaded_func.configure(text=f"Wzór: {nazwa}", text_color="#28a745") 
                
                _ctypes.FreeLibrary(dll._handle)
            except Exception:
                self.label_loaded_func.configure(text="Wzór: (brak opisu w dll)", text_color="gray")

    def oblicz(self):
        try:
            folder = os.path.dirname(os.path.abspath(__file__))
            exe = os.path.join(folder, "backend.exe")

            dll_path = os.path.normpath(self.entry_dll.get())
            if not dll_path or not os.path.exists(dll_path):
                messagebox.showwarning("Brak pliku", "Wybierz poprawny plik .dll z funkcją!")
                return

            tryb = self.var_tryb.get()
            dane = self.entry_data.get().replace("[", "").replace("]", "").replace(",", ";").replace(" ", "")
            iters = self.entry_iter.get()
            epsilon = self.entry_eps.get().replace(" ", "")

            process = subprocess.Popen([exe, dll_path, tryb, dane, iters, epsilon], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, text=True, encoding='utf-8')
            stdout, stderr = process.communicate()

            self.txt_output.delete("1.0", ctk.END)
            if process.returncode == 0:
                self.txt_output.insert(ctk.END, stdout)
            else:
                self.txt_output.insert(ctk.END, f"BŁĄD BACKENDU (kod {process.returncode}):\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")

        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się połączyć z C++: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()