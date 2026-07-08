import sys
import tkinter as tk
from tkinter import messagebox
import ipn_gen
import edrpo_gen


class IpnEdrpouGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор ІПН та ЄДРПОУ")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Центруємо головне вікно (600x400)
        self._center_element(self.root, 400, 300)

        # Змінні для чекбоксів
        self.var_ipn = tk.BooleanVar(value=True)
        self.var_edrpou = tk.BooleanVar()
        self.var_vat = tk.BooleanVar()

        # top empty space
        top_spacer = tk.Frame(self.root)
        top_spacer.pack(expand=True)

        # frame for checkboxes
        checkbox_frame = tk.Frame(self.root)
        checkbox_frame.pack(pady=10)

        # Елементи інтерфейсу
        tk.Checkbutton(checkbox_frame, text="ІПН (Фіз. особа)", variable=self.var_ipn).pack(anchor="w")
        tk.Checkbutton(checkbox_frame, text="ЄДРПОУ (Юр. особа)", variable=self.var_edrpou).pack(anchor="w")
        tk.Checkbutton(checkbox_frame, text="Платник ПДВ", variable=self.var_vat).pack(anchor="w")

        # middle empty space
        middle_spacer = tk.Frame(self.root)
        middle_spacer.pack(expand=True)

        # Поле введення
        tk.Label(root, text="Введіть дату для ІПН (ДД.ММ.РРРР) або префікс для ЄДРПОУ (2 цифри):", wraplength=270, justify="center").pack(padx=20, pady=10)
        self.entry_input = tk.Entry(root, justify="center",width=25)
        self.entry_input.pack(padx=20, pady=1)
        self.entry_input.insert(0, "01.01.1990")  # Дефолтне значення для зручності

        # Кнопка генерації
        tk.Button(root, text="GENERATE", command=self.handle_generation , bg="#4CAF50", fg="white",
                  font=("Arial", 10, "bold")).pack(pady=20)
        root.bind("<Return>", lambda e: self.handle_generation())

        # bottom empty space
        bottom_spacer = tk.Frame(self.root)
        bottom_spacer.pack(expand=True)

    def _center_element(self, win, width, height, parent=None):
        """Універсальний метод для центрування вікон та модалок."""
        if parent:
            # Центрування відносно батьківського вікна
            p_x = parent.winfo_x()
            p_y = parent.winfo_y()
            p_w = parent.winfo_width()
            p_h = parent.winfo_height()
            x = p_x + (p_w // 2) - (width // 2)
            y = p_y + (p_h // 2) - (height // 2)
        else:
            # Центрування відносно екрана
            screen_width = win.winfo_screenwidth()
            screen_height = win.winfo_screenheight()
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

    def handle_generation(self, event=None):
        """Основний обробник бізнес-логіки інтерфейсу."""
        user_input = self.entry_input.get().strip()
        # user_input validation
        if not user_input:
            messagebox.showwarning("Помилка вводу", "Поле не може бути порожнім!")
            return
        if any(char.isalpha() for char in user_input):
            messagebox.showwarning("Помилка вводу", "Не вводь літери! \nВведіть дату (для ІПН) або префікс (для ЄДРПОУ)")
            return
        allowed_list = set("0123456789.-,/ ")
        if not (char in allowed_list for char in user_input):
            messagebox.showwarning("Помилка вводу", "Введення містить недопустимі символи. \n Достно до введення цифри та роздільники .-,/!")
            return
        results = []
        return_res = []

        try:
            if self.var_ipn.get():
                # generate single ipn
                ipn = ipn_gen.generate_ipn(user_input)
                results.append(f"ІПН: {ipn}")
                # generate ipn list
                ipn_gen.generate_ipn_list(user_input)
                return_res.append(ipn)

            if self.var_edrpou.get():
                # Якщо введено дату замість префіксу, візьмемо дефолт "35" або перші дві цифри
                prefix = user_input if (user_input.isdigit() and len(user_input) == 2) else "35"
                # generate single edrpou
                edrpou = edrpo_gen.generate_edrpou(prefix)
                results.append(f"ЄДРПОУ: {edrpou}")
                # generate edrpo list
                edrpo_gen.generate_edrpou_list(prefix)
                return_res.append(edrpou)

            if self.var_vat.get() and self.var_edrpou.get():
                # Приклад логіки ПДВ для юр-особи (звичайне розширення коду для тестів)
                results.append(f"Код ПДВ (ЮО): 1{edrpou}011")
                return_res.append(f"1{edrpou}011")

            if not results:
                messagebox.showwarning("Увага", "Виберіть хоча б один тип коду для генерації!")
                return
            copy_res = "\n".join(return_res)
            self.show_result_modal("\n".join(results),copy_res)

        except ValueError as e:
            messagebox.showerror("Помилка валідації", str(e))

    def show_result_modal(self, result_text, copy_res):
        """Створення модального вікна для копіювання результату."""
        top = tk.Toplevel(self.root)
        top.title("Результат")
        self._center_element(top, 250, 150, parent=self.root)

        top.transient(self.root)
        top.grab_set()

        # frame for centering
        content = tk.Frame(top)
        content.pack(expand=True)

        tk.Label(content, text=result_text, justify="center", font=("Consolas", 11)).pack(pady=20)

        def copy_and_close(copy_res):
            self.root.clipboard_clear()
            self.root.clipboard_append(copy_res)
            top.destroy()

        tk.Button(content, text="КОПІЮВАТИ", command=lambda: copy_and_close(copy_res), bg="#2196F3", fg="white").pack(pady=10)
        top.bind("<Control-c>", lambda e: copy_and_close(copy_res))

    def on_close(self):
        self.root.destroy()

def main():
    # Захист від подвійного запуску
    if len(sys.argv) > 1 and sys.argv[1] == "--running":
        print("Програма вже запущена!")

        sys.exit(0)

    root = tk.Tk()
    IpnEdrpouGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()