import tkinter as tk
from tkinter import messagebox
import smtplib
import random
from email.mime.text import MIMEText

class FakeBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FakeBank App")
        self.root.geometry("350x300")
        self.root.configure(bg="#FFD700")  # Фон золотой

        # База данных: {email: {"card_number": str, "balance": float}}
        self.accounts = {}

        # Поле для ввода Gmail
        self.email_label = tk.Label(root, text="Введите ваш Gmail:", bg="#FFD700", font=("Arial", 12))
        self.email_label.pack(pady=20)

        self.email_entry = tk.Entry(root, width=35)
        self.email_entry.pack(pady=10)

        # Кнопка "Продолжить"
        self.continue_button = tk.Button(
            root,
            text="Продолжить",
            command=self.on_continue,
            bg="#FFA500",
            fg="white",
            font=("Arial", 12, "bold")
        )
        self.continue_button.pack(pady=20)

        # Текст для результата
        self.result_label = tk.Label(
            root,
            text="",
            bg="#FFD700",
            font=("Arial", 10),
            wraplength=320
        )
        self.result_label.pack(pady=10)

        self.current_code = None  # Хранит сгенерированный код

    def generate_code(self):
        """Генерирует случайный 4-значный код."""
        return str(random.randint(1000, 9999))

    def generate_card_number(self):
        """Генерирует уникальный 16-значный номер карты (Visa-формат)."""
        while True:
            card_number = "4" + "".join(random.choices("0123456789", k=15))
            formatted_card = f"{card_number[:4]}-{card_number[4:8]}-{card_number[8:12]}-{card_number[12:]}"
            if formatted_card not in [data["card_number"] for data in self.accounts.values()]:
                return formatted_card

    def send_email(self, email, code):
        """Отправляет реальный email через Gmail SMTP."""
        fake_sender = "fakebank_kostya@facebank.kostya"
        real_sender = email
        to_email = email
        app_password = "bafd zqrq scnq lbqk"

        subject = "Ваш код от FakeBank"
        body = f"Ваш код: {code}\n\nПроверьте inbox и spam."
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = f"FakeBank Kostya <{fake_sender}>"
        msg["To"] = to_email

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(real_sender, app_password)
                server.sendmail(real_sender, to_email, msg.as_string())
            return fake_sender, True
        except smtplib.SMTPAuthenticationError:
            print(f"Ошибка отправки: Неверный Gmail или пароль приложения")
            return None, False
        except smtplib.SMTPConnectError:
            print(f"Ошибка отправки: Не удалось подключиться к SMTP-серверу")
            return None, False
        except Exception as e:
            print(f"Ошибка отправки: {str(e)}")
            return None, False

    def open_code_window(self, code, email, fake_sender):
        """Открывает окно для ввода кода."""
        self.code_window = tk.Toplevel(self.root)
        self.code_window.title("Проверка кода")
        self.code_window.geometry("300x200")
        self.code_window.configure(bg="#FFD700")

        code_label = tk.Label(self.code_window, text="Введите полученный код:", bg="#FFD700", font=("Arial", 12))
        code_label.pack(pady=20)

        code_entry = tk.Entry(self.code_window, width=10)
        code_entry.pack(pady=10)

        check_button = tk.Button(
            self.code_window,
            text="Проверить",
            command=lambda: self.verify_code(code_entry.get(), code, email, fake_sender),
            bg="#FFA500",
            fg="white",
            font=("Arial", 12, "bold")
        )
        check_button.pack(pady=20)

    def verify_code(self, entered_code, correct_code, email, fake_sender):
        """Проверяет введенный код и открывает окно карты."""
        if entered_code == correct_code:
            self.code_window.destroy()
            self.root.destroy()
            self.open_card_window(email, fake_sender)
        else:
            messagebox.showerror("Ошибка", "Неверный код. Попробуйте снова.")

    def open_card_window(self, email, fake_sender):
        """Открывает окно с информацией о карте."""
        if email not in self.accounts:
            self.accounts[email] = {"card_number": self.generate_card_number(), "balance": 1000.0}

        card_window = tk.Toplevel()
        card_window.title("Ваша карта FakeBank")
        card_window.geometry("350x300")
        card_window.configure(bg="#FFD700")

        card_label = tk.Label(
            card_window,
            text=f"Ваша карта:\nНомер: {self.accounts[email]['card_number']}\nEmail: {email}\nБаланс: {self.accounts[email]['balance']}",
            bg="#FFD700",
            font=("Arial", 12),
            justify="center"
        )
        card_label.pack(pady=20)

        payments_button = tk.Button(
            card_window,
            text="Платежи",
            command=lambda: self.open_payments_window(email),
            bg="#FFA500",
            fg="white",
            font=("Arial", 12, "bold")
        )
        payments_button.pack(pady=10)

        ok_button = tk.Button(
            card_window,
            text="ОК",
            command=card_window.destroy,
            bg="#FFA500",
            fg="white",
            font=("Arial", 12, "bold")
        )
        ok_button.pack(pady=10)

    def open_payments_window(self, email):
        """Открывает окно с опциями платежей."""
        payments_window = tk.Toplevel()
        payments_window.title("Платежи FakeBank")
        payments_window.geometry("300x400")
        payments_window.configure(bg="#FFD700")

        payment_options = [
            ("Оплатить за квартиру", lambda: messagebox.showinfo("Успех", "Оплата за квартиру успешно выполнена!")),
            ("Оплатить за роутер", lambda: messagebox.showinfo("Успех", "Оплата за роутер успешно выполнена!")),
            ("Оплатить за интернет", lambda: messagebox.showinfo("Успех", "Оплата за интернет успешно выполнена!")),
            ("Оплатить за создание", lambda: messagebox.showinfo("Успех", "Оплата за создание успешно выполнена!")),
            ("Перевести", lambda: messagebox.showinfo("Успех", "Перевод успешно выполнен!")),
            ("Пополнить", lambda: messagebox.showinfo("Успех", "Счет успешно пополнен!"))
        ]

        for text, command in payment_options:
            button = tk.Button(
                payments_window,
                text=text,
                command=command,
                bg="#FFA500",
                fg="white",
                font=("Arial", 12)
            )
            button.pack(pady=10, fill="x", padx=20)

    def on_continue(self):
        email = self.email_entry.get()
        if email:
            if "@gmail.com" not in email:
                self.result_label.config(text="")
                messagebox.showwarning("Ошибка", "Используйте Gmail-адрес!")
                return

            self.current_code = self.generate_code()
            fake_sender, success = self.send_email(email, self.current_code)
            if success:
                self.result_label.config(
                    text=f"Проверьте inbox и spam.\nОтправлено от: {fake_sender}"
                )
                messagebox.showinfo("Успех", f"Код отправлен на {email}")
                self.open_code_window(self.current_code, email, fake_sender)
            else:
                self.result_label.config(text="")
                messagebox.showerror(
                    "Ошибка",
                    "Не удалось отправить email.\nВозможные причины:\n- Неверный пароль приложения\n- Отключена двухфакторная аутентификация\n- Проблемы с интернетом\nПодробности в консоли."
                )
        else:
            self.result_label.config(text="")
            messagebox.showwarning("Ошибка", "Введите ваш Gmail!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FakeBankApp(root)
    root.mainloop()
