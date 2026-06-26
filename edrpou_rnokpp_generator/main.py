import tkinter as tk
#from logging import exception
from tkinter import messagebox
from ipn_gen import generate_ipn, generate_ipn_list
from edrpo_gen_plus import generato_self_validator, generate_edrpou

# Перевірка чи вже запущена програма
import sys

if len(sys.argv) > 1 and sys.argv[1] == "--running":
    print("Програма вже запущена!")
    sys.exit(0)

class IpnEdrpouGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор ІПН та ЄДРПОУ")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


        # Чекбокси
        self.var_ipn = tk.BooleanVar(value=True)   # за замовчуванням ІПН
        self.var_edrpou = tk.BooleanVar()
        self.var_vat = tk.BooleanVar()

        tk.Checkbutton(root, text="ІПН", variable=self.var_ipn).pack(anchor="w")
        tk.Checkbutton(root, text="ЄДРПОУ", variable=self.var_edrpou).pack(anchor="w")
        tk.Checkbutton(root, text="Платник ПДВ", variable=self.var_vat).pack(anchor="w")

        # Поле для введення дати
        tk.Label(root, text="Введіть дату (ДД.ММ.РРРР):").pack(anchor="w")
        self.entry_date = tk.Entry(root)
        self.entry_date.pack(fill="x", padx=5, pady=5)

        # Кнопка GEN
        tk.Button(root, text="GEN", command=self.generate).pack(pady=10)
        self.root.bind("<Return>", self.generate)


    def generate(self, event=None):

        date_str = self.entry_date.get().strip()



        # Якщо не обрано жодного чекбокса → помилка
        if not (self.var_ipn.get() or self.var_edrpou.get()):
            messagebox.showerror("Помилка", "Оберіть хоча б один тип (ІПН або ЄДРПОУ)")
            return

        result = ""

        if self.var_ipn.get():
            try:
                ipn = generate_ipn(date_str)
                result += f"{ipn}\n"

                generate_ipn_list(date_str)
            except Exception as e:
                messagebox.showerror("Помилка", str(e))
                return

        if self.var_edrpou.get():
            try:
                edrpou = generate_edrpou() 
                result += f"{edrpou}\n"

                generato_self_validator()
            except ValueError as e:
                messagebox.showerror("Помилка", str(e))
                return

        if self.var_vat.get():
            result += "Статус: платник ПДВ\n"

        # Модальне вікно з кнопкою "Копіювати"
        top = tk.Toplevel(self.root)
        center_modal(top, self.root, 400, 200)
        top.title("Результат")
        top.transient(self.root) #Прив'язка до головного вікна
        top.grab_set()  # робимо модальним

        lbl = tk.Label(top, text=result, justify="left")
        lbl.pack(padx=20, pady=20)

        def copy_and_close():
            self.root.clipboard_clear()
            self.root.clipboard_append(result.strip())
            top.destroy()

        tk.Button(top, text="КОПІЮВАТИ", command=copy_and_close).pack(pady=10)

        def on_enter_modal(event):
            copy_and_close()
            return "break"

        top.bind("<Return>", on_enter_modal)

        #return "break"

    def on_close(self):
        self.root.destroy()

def center_window(win, width=600, height=400):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def center_modal(win, parent, width=300, height=200):
    parent.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
    y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")




if __name__ == "__main__":
    root = tk.Tk()
    root.title("Головне вікно")
    center_window(root, 600, 400)
    app = IpnEdrpouGeneratorApp(root)
    root.mainloop()