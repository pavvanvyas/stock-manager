import sys
import sqlite3
import hashlib
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class UserAuthenticationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("User Authentication")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.register_button)

        # Create the user accounts database or connect to an existing one
        self.create_user_accounts_database()

    def create_user_accounts_database(self):
        self.conn = sqlite3.connect("user_accounts.db")
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT
            )
        ''')
        self.conn.commit()

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            self.show_message("Error", "Please enter a username and password.")
            return

        # Hash the password before storing it
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        self.conn.commit()

        self.show_message("Success", "Registration successful. You can now log in.")

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            self.show_message("Error", "Please enter a username and password.")
            return

        # Hash the entered password for comparison
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = cursor.fetchone()

        if user:
            self.show_message("Success", "Login successful.")
        else:
            self.show_message("Error", "Login failed. Invalid username or password.")

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

def main():
    app = QApplication(sys.argv)
    window = UserAuthenticationApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
