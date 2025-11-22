import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import time

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей")
        self.root.geometry("600x600")

        # Переменные для хранения состояния
        self.password_length = tk.IntVar(value=13)
        self.use_lower_latin = tk.BooleanVar(value=True)
        self.use_lower_russian = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.special_chars = tk.StringVar(value="!@#$%^&*()_+-=[]{}|;:,.<>?")
        self.delete_chars = tk.StringVar(value="")

        self.create_widgets()
        self.update_alphabet()
        
    def create_widgets(self):
        # Заголовок
        style = ttk.Style()
        title_label = ttk.Label(self.root, text="Генератор паролей", font=("Montserrat", 14))
        title_label.pack(pady=5)
        
        # Фрейм для основных параметров
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=5, padx=5, fill="x")
        
        # Длина пароля
        length_frame = ttk.Frame(main_frame)
        length_frame.pack(fill="x", pady=5)
        ttk.Label(length_frame, text="Длина пароля (1-64):", font=("Montserrat", 10)).pack(side="left")
        length_entry = ttk.Entry(length_frame, textvariable=self.password_length, width=10)
        length_entry.pack(side="left", padx=5)
        
        # Чекбоксы для типов символов
        checkboxes_frame = ttk.Frame(main_frame)
        checkboxes_frame.pack(fill="x", pady=5)
        style.configure('TCheckbutton', font=("Montserrat", 10))
        
        ttk.Checkbutton(checkboxes_frame, text="Строчные латинские буквы",
                       variable=self.use_lower_latin, command=self.update_alphabet).grid(row=1, column=1, sticky="w", padx=2)
        ttk.Checkbutton(checkboxes_frame, text="Строчные русские буквы",
                       variable=self.use_lower_russian, command=self.update_alphabet).grid(row=1, column=2, sticky="w", padx=2)
        ttk.Checkbutton(checkboxes_frame, text="Цифры",
                       variable=self.use_digits, command=self.update_alphabet).grid(row=2, column=1, sticky="w", padx=2)
        ttk.Checkbutton(checkboxes_frame, text="Учитывать регистр (заглавные буквы)",
                       variable=self.use_uppercase, command=self.update_alphabet).grid(row=2, column=2, sticky="w", padx=2)
         
        # Спецсимволы
        special_frame = ttk.Frame(main_frame)
        special_frame.pack(fill="x", pady=5)
        ttk.Label(special_frame, text="Спецсимволы:", font=("Montserrat", 10)).pack(anchor="w")
        special_entry = ttk.Entry(special_frame, textvariable=self.special_chars, width=50)
        special_entry.pack(fill="x", pady=5)

        #Исключение символов
        delete_frame = ttk.Frame(main_frame)
        delete_frame.pack(fill="x", pady=5)
        ttk.Label(delete_frame, text="Исключить символы:", font=("Montserrat", 10)).pack(anchor="w")
        delete_entry = ttk.Entry(delete_frame, textvariable=self.delete_chars, width=50)
        delete_entry.pack(fill="x", pady=5)
        
        # Итоговый алфавит
        alphabet_frame = ttk.Frame(main_frame)
        alphabet_frame.pack(fill="x", pady=5)
        ttk.Label(alphabet_frame, text="Итоговый алфавит:", font=("Montserrat", 10)).pack(anchor="w")
        self.alphabet_label = ttk.Label(alphabet_frame, text="", wraplength=500, font=("Montserrat", 10))
        self.alphabet_label.pack(fill="x", pady=5)
        
        # Количество паролей
        count_frame = ttk.Frame(main_frame)
        count_frame.pack(fill="x", pady=5)
        ttk.Label(count_frame, text="Число возможных паролей:", font=("Montserrat", 10)).pack(side="left")
        self.count_label = ttk.Label(count_frame, text="0", font=("Montserrat", 10))
        self.count_label.pack(side="left", padx=5)
        
        # Сгенерированный пароль
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill="x", pady=5)
        ttk.Label(password_frame, text="Сгенерированный пароль:", font=("Montserrat", 10)).pack(side="left")
        self.password_label = ttk.Label(password_frame, text="", font=("Montserrat", 10))
        self.password_label.pack(side="left", padx=5)
        
        # Кнопки
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x", pady=5)
        style.configure("TButton", font=("Montserrat", 10),)

        ttk.Button(buttons_frame, text="Сгенерировать новый пароль", 
                  command=self.generate_password).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Проверить пароль", 
                  command=self.check_password).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Очистить", 
                  command=self.clear_all).pack(side="left", padx=5)
        
        # Поле для проверки пароля
        check_frame = ttk.Frame(main_frame)
        check_frame.pack(fill="x", pady=5)
        ttk.Label(check_frame, text="Проверить свой пароль:", font=("Montserrat", 10)).pack(anchor="w")
        self.check_entry = ttk.Entry(check_frame, width=50)
        self.check_entry.pack(fill="x", pady=5)
        self.check_result = ttk.Label(check_frame, text="")
        self.check_result.pack(anchor="w")
        
        # Привязываем события для автоматического обновления
        length_entry.bind("<KeyRelease>", lambda e: self.update_alphabet())
        special_entry.bind("<KeyRelease>", lambda e: self.update_alphabet())
        delete_entry.bind("<KeyRelease>", lambda e: self.update_alphabet())
        # Генерируем первый пароль
        self.generate_password()
    
    def get_alphabet(self):
        #Создает алфавит на основе выбранных параметров
        alphabet = ""
        
        if self.use_lower_latin.get():
            alphabet += string.ascii_lowercase
            if self.use_uppercase.get():
                alphabet += string.ascii_uppercase
        
        if self.use_lower_russian.get():
            russian_lower = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
            alphabet += russian_lower
            if self.use_uppercase.get():
                alphabet += russian_lower.upper()
        
        if self.use_digits.get():
            alphabet += string.digits
        
        # Добавляем спецсимволы, исключая дубликаты
        special = self.special_chars.get()
        for char in special:
            if char not in alphabet:
                alphabet += char
        
        delete = self.delete_chars.get()
        for char in delete:
            if char in alphabet:
                alphabet = alphabet.replace(char, "")

        return alphabet
    
    def update_alphabet(self):
        #Обновляет отображение алфавита и количества паролей
        try:
            length = self.password_length.get()
            if length < 1 or length > 64:
                self.alphabet_label.config(text="Ошибка: длина пароля должна быть от 1 до 64", font=("Montserrat", 10), foreground="red")
                self.count_label.config(text="0")
                return
        except:
            self.alphabet_label.config(text="Ошибка: некорректная длина пароля", font=("Montserrat", 10), foreground="red")
            self.count_label.config(text="0")
            return
        
        alphabet = self.get_alphabet()
        
        if not alphabet:
            self.alphabet_label.config(text="Ошибка: алфавит не может быть пустым",  font=("Montserrat", 10), foreground="red")
            self.count_label.config(text="0")
            return
        
        # Показываем первые 100 символов алфавита
        display_alphabet = alphabet
        if len(alphabet) > 100:
            display_alphabet = alphabet[:100] + "..."
        
        self.alphabet_label.config(text=f"{display_alphabet} (Включает {len(alphabet)} символов)")
        
        # Вычисляем количество возможных паролей
        total_passwords = len(alphabet) ** length
        self.count_label.config(text=f"{total_passwords:,}")
    
    def generate_password(self):
        #Генерирует случайный пароль
        try:
            length = self.password_length.get()
            if length < 1 or length > 64:
                messagebox.showerror("Ошибка", "Длина пароля должна быть от 1 до 64")
                return
        except:
            messagebox.showerror("Ошибка", "Некорректная длина пароля")
            return
        
        alphabet = self.get_alphabet()
        
        if not alphabet:
            messagebox.showerror("Ошибка", "Алфавит не может быть пустым")
            return
        
        # Измеряем время генерации
        start_time = time.time()
        
        # Генерируем пароль
        password = ''.join(random.choice(alphabet) for _ in range(length))
        
        end_time = time.time()
        generation_time = end_time - start_time
        
        self.password_label.config(text=password)
        
        # Показываем время генерации, если оно больше 0.1 секунды
        if generation_time > 0.1:
            self.password_label.config(text=f"{password} (время генерации: {generation_time:.3f} сек)")
    
    def check_password(self):
        #Проверяет введенный пользователем пароль на соответствие требованиям
        password = self.check_entry.get()
        
        if not password:
            self.check_result.config(text="Введите пароль для проверки", font=("Montserrat", 10), foreground="red")
            return
        
        alphabet = self.get_alphabet()
        issues = []
        
        # Проверяем длину
        if len(password) != self.password_length.get():
            issues.append(f"Пароль имеет неправильную длину (длина должна быть {self.password_length.get()})")
        
        # Проверяем, что все символы из алфавита
        for char in password:
            if char not in alphabet:
                issues.append(f"Использован недопустимый символ '{char}'")
                break
        
        # Проверяем наличие типов символов, если выбраны
        if self.use_lower_latin.get() and self.use_uppercase.get():
            has_lower = any(c in string.ascii_lowercase for c in password)
            has_upper = any(c in string.ascii_uppercase for c in password)
            if not has_lower:
                issues.append("В пароле отсутствуют строчные латинские буквы")
            if not has_upper:
                issues.append("В пароле отсутствуют заглавные латинские буквы")
        
        if self.use_digits.get():
            if not any(c in string.digits for c in password):
                issues.append("В пароле отсутствуют цифры")
        
        if self.use_lower_russian.get() and self.use_uppercase.get():
            russian_lower = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
            russian_upper = russian_lower.upper()
            has_russian_lower = any(c in russian_lower for c in password)
            has_russian_upper = any(c in russian_upper for c in password)
            if not has_russian_lower:
                issues.append("В пароле отсутствуют строчные русские буквы")
            if not has_russian_upper:
                issues.append("В пароле отсутствуют заглавные русские буквы")
        
        special = self.special_chars.get()
        if special and not any(c in special for c in password):
            issues.append("В пароле отсутствуют спецсимволы")
        
        if issues:
            self.check_result.config(text=f"Проблемы: {', '.join(issues)}", font=("Montserrat", 10), foreground="red")
        else:
            self.check_result.config(text="Пароль соответствует всем требованиям!", font=("Montserrat", 10), foreground="green")
    
    def clear_all(self):
        #Очищает все поля
        self.password_length.set(8)
        self.use_lower_latin.set(True)
        self.use_lower_russian.set(False)
        self.use_digits.set(True)
        self.use_uppercase.set(True)
        self.special_chars.set("!@#$%^&*()_+-=[]{}|;:,.<>?")
        self.check_entry.delete(0, tk.END)
        self.check_result.config(text="")
        self.update_alphabet()
        self.generate_password()

def main():
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()