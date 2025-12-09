import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
from collections import defaultdict

# ! Словарь студентов
students = {}

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Учёт студентов")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        # ? Верхнее меню 
        menu_frame = tk.Frame(root)
        menu_frame.pack(pady=10)

        tk.Button(menu_frame, text="Добавить студента", command=self.add_student, width=20).grid(row=0, column=0, padx=5)
        tk.Button(menu_frame, text="Показать всех", command=self.show_all, width=20).grid(row=0, column=1, padx=5)
        tk.Button(menu_frame, text="Найти по ФИО", command=self.find_by_fio, width=20).grid(row=0, column=2, padx=5)
        tk.Button(menu_frame, text="Удалить по ФИО", command=self.delete_by_fio, width=20).grid(row=0, column=3, padx=5)

        # ? Кнопки поиска
        search_frame = tk.Frame(root)
        search_frame.pack(pady=5)
        tk.Button(search_frame, text="Средний балл > 4.0", command=self.search_avg_above_4, width=25).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Одинаковые группы", command=self.search_same_group, width=25).pack(side=tk.LEFT, padx=5)

        # ? Поле вывода
        tk.Label(root, text="Результаты:").pack(anchor=tk.W, padx=10, pady=(10, 0))
        self.output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=25, font=("Consolas", 10))
        self.output.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # ? Статусная строка
        self.status = tk.Label(root, text="Готово", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(self, msg):
        self.status.config(text=msg)

    def clear_output(self):
        self.output.delete(1.0, tk.END)

    def add_student(self):
        popup = tk.Toplevel(self.root)
        popup.title("Добавить студента")
        popup.geometry("400x250")
        popup.grab_set()  # ! Модальное окно

        tk.Label(popup, text="ФИО:").pack(pady=(10, 0))
        fio_entry = tk.Entry(popup, width=50)
        fio_entry.pack()

        tk.Label(popup, text="Номер группы:").pack()
        group_entry = tk.Entry(popup, width=50)
        group_entry.pack()

        tk.Label(popup, text="Оценки (5 чисел через пробел, например: 4 5 3.5 4 5):").pack()
        grades_entry = tk.Entry(popup, width=50)
        grades_entry.pack()

        def save():
            fio = fio_entry.get().strip()
            group = group_entry.get().strip()
            grades_str = grades_entry.get().strip()

            if not fio or not group or not grades_str:
                messagebox.showwarning("Ошибка", "Все поля обязательны!")
                return

            if fio in students:
                messagebox.showinfo("Инфо", "Студент с таким ФИО уже существует.")
                return

            try:
                grades = list(map(float, grades_str.split()))
                if len(grades) != 5:
                    raise ValueError("Должно быть ровно 5 оценок.")
                if not all(2 <= g <= 5 for g in grades):
                    raise ValueError("Оценки должны быть от 2 до 5.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Некорректные оценки:\n{e}")
                return

            students[fio] = {
                "ФИО": fio,
                "номер группы": group,
                "успеваемость": grades
            }
            self.update_status(f"Добавлен студент: {fio}")
            popup.destroy()

        tk.Button(popup, text="Сохранить", command=save, bg="#4CAF50", fg="white").pack(pady=15)

    def show_all(self):
        self.clear_output()
        if not students:
            self.output.insert(tk.END, "Список студентов пуст.\n")
            return

        for data in students.values():
            avg = sum(data["успеваемость"]) / len(data["успеваемость"])
            self.output.insert(tk.END, f"ФИО: {data['ФИО']}\n")
            self.output.insert(tk.END, f"Группа: {data['номер группы']}\n")
            self.output.insert(tk.END, f"Оценки: {data['успеваемость']}\n")
            self.output.insert(tk.END, f"Средний балл: {avg:.2f}\n")
            self.output.insert(tk.END, "-" * 50 + "\n")

    def find_by_fio(self):
        fio = simpledialog.askstring("Поиск", "Введите ФИО студента:")
        if not fio:
            return
        fio = fio.strip()
        self.clear_output()
        if fio in students:
            data = students[fio]
            avg = sum(data["успеваемость"]) / len(data["успеваемость"])
            self.output.insert(tk.END, f"Найден студент:\n")
            self.output.insert(tk.END, f"ФИО: {data['ФИО']}\n")
            self.output.insert(tk.END, f"Группа: {data['номер группы']}\n")
            self.output.insert(tk.END, f"Оценки: {data['успеваемость']}\n")
            self.output.insert(tk.END, f"Средний балл: {avg:.2f}\n")
        else:
            self.output.insert(tk.END, "Студент с таким ФИО не найден.\n")

    def delete_by_fio(self):
        fio = simpledialog.askstring("Удаление", "Введите ФИО для удаления:")
        if not fio:
            return
        fio = fio.strip()
        if fio in students:
            del students[fio]
            self.update_status(f"Удалён студент: {fio}")
            self.output.insert(tk.END, f"Студент {fio} удалён.\n")
        else:
            messagebox.showinfo("Не найден", "Студент не найден.")

    def search_avg_above_4(self):
        self.clear_output()
        found = False
        for data in students.values():
            avg = sum(data["успеваемость"]) / len(data["успеваемость"])
            if avg > 4.0:
                self.output.insert(tk.END, f"{data['ФИО']} ({data['номер группы']}) — ср. балл: {avg:.2f}\n")
                found = True
        if not found:
            self.output.insert(tk.END, "Нет студентов со средним баллом выше 4.0.\n")

    def search_same_group(self):
        self.clear_output()
        groups = defaultdict(list)
        for fio, data in students.items():
            groups[data["номер группы"]].append((fio, sum(data["успеваемость"]) / len(data["успеваемость"])))

        found = False
        for group, members in groups.items():
            if len(members) > 1:
                self.output.insert(tk.END, f"\nГруппа {group}:\n")
                for name, avg in members:
                    self.output.insert(tk.END, f"  - {name} (ср. балл: {avg:.2f})\n")
                found = True
        if not found:
            self.output.insert(tk.END, "Нет студентов с одинаковыми номерами групп.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()