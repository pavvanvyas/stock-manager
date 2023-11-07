import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMessageBox,QHBoxLayout, QFileDialog,QPushButton, QComboBox, QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QFormLayout

class FileManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Management")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.create_db_button = QPushButton("Create New Database")
        self.open_db_button = QPushButton("Open Existing Database")

        self.create_db_button.clicked.connect(self.create_database)
        self.open_db_button.clicked.connect(self.open_database)

        self.layout.addWidget(self.create_db_button)
        self.layout.addWidget(self.open_db_button)
          # Create an instance of DatabaseApp
       

        # Database connection
        self.conn = None
        self.current_database = None
        self.selected_table = None

        # Database and table selection
        self.db_selector = QComboBox()
        self.db_selector.activated[str].connect(self.select_database)
        self.layout.addWidget(self.db_selector)

        self.table_selector = QComboBox()
        self.table_selector.activated[str].connect(self.select_table)
        self.layout.addWidget(self.table_selector)

        # Record management
        self.record_layout = QFormLayout()
        self.layout.addLayout(self.record_layout)

        
        # Button to clear the database
        self.clear_db_button = QPushButton("Clear Database")
        self.clear_db_button.clicked.connect(self.clear_database)
        self.layout.addWidget(self.clear_db_button)

        self.load_databases()

    def load_databases(self):
        # Load available databases
        self.db_selector.clear()
        self.table_selector.clear()
        self.conn = None
        self.current_database = None
        self.selected_table = None

        self.conn = sqlite3.connect('master.db')
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        databases = [row[0] for row in cursor.fetchall()]
        self.db_selector.addItems(databases)

    def create_database(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Create New Database", "", "Database Files (*.db)")
        if file_path:
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS master (name TEXT);")
            cursor.execute("INSERT INTO master (name) VALUES (?);", (file_path,))
            conn.commit()
            conn.close()
            self.load_databases()

    def open_database(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Database", "", "Database Files (*.db)")
        if file_path:
            self.conn = sqlite3.connect(file_path)
            self.current_database = file_path
            self.load_tables()

    def select_database(self, db_name):
        if self.current_database:
            self.conn.close()
        self.conn = sqlite3.connect(db_name)
        self.current_database = db_name
        self.load_tables()

    def load_tables(self):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            self.table_selector.clear()
            self.table_selector.addItems(tables)
            self.record_layout.takeAt(0)
            self.selected_table = None

    def select_table(self, table_name):
        self.selected_table = table_name
        self.setup_record_layout()

    def setup_record_layout(self):
        if self.selected_table:
            cursor = self.conn.cursor()
            cursor.execute(f"PRAGMA table_info({self.selected_table})")
            columns = [row[1] for row in cursor.fetchall()]
            self.record_layout = QFormLayout()

            self.input_fields = []
            for column in columns:
                label = QLabel(column + ":")
                input_field = QLineEdit()
                self.input_fields.append(input_field)
                self.record_layout.addRow(label, input_field)

            add_record_button = QPushButton("Add Record")
            add_record_button.clicked.connect(self.add_record)

            update_record_button = QPushButton("Update Record")
            update_record_button.clicked.connect(self.update_record)

            delete_record_button = QPushButton("Delete Record")
            delete_record_button.clicked.connect(self.delete_record)

            self.record_layout.addRow(add_record_button)
            self.record_layout.addRow(update_record_button)
            self.record_layout.addRow(delete_record_button)

            self.layout.addLayout(self.record_layout)

    def add_record(self):
        if self.selected_table:
            values = [input_field.text() for input_field in self.input_fields]
            placeholders = ','.join(['?'] * len(values))
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT INTO {self.selected_table} VALUES ({placeholders});", values)
            self.conn.commit()

    def update_record(self):
        if self.selected_table:
            values = [input_field.text() for input_field in self.input_fields]
            cursor = self.conn.cursor()
            cursor.execute(f"UPDATE {self.selected_table} SET name=? WHERE id=?;", (values[0], values[1]))
            self.conn.commit()

    def delete_record(self):
        if self.selected_table:
            values = [input_field.text() for input_field in self.input_fields]
            cursor = self.conn.cursor()
            cursor.execute(f"DELETE FROM {self.selected_table} WHERE id=?;", (values[0],))
            self.conn.commit()
        
    def clear_database(self):
        if self.current_database:
            confirm = QMessageBox.question(self, "Clear Database", "Do you want to clear the entire database?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                conn = sqlite3.connect(self.current_database)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall()]
                for table in tables:
                    cursor.execute(f"DROP TABLE IF EXISTS {table}")
                conn.commit()
                conn.close()
                self.load_tables()
                QMessageBox.information(self, "Database Cleared", "The database has been cleared.")
            else:
                QMessageBox.information(self, "Database Not Cleared", "The database was not cleared")


def main():
    app = QApplication(sys.argv)
    window = FileManagementApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
