import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox,QTableWidget, QTableWidgetItem, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery,QSqlDatabase

import sqlite3

class DatabaseManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Relational Database Data Manager")
        self.setGeometry(100, 100, 800, 600)

        self.db_connection = sqlite3.connect("stock_manager.db")  # Connect to SQLite database
        self.cursor = self.db_connection.cursor()
        cursor = self.db_connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
        SER NO INTEGER PRIMARY KEY,
        GROSS REAL,
        LESS REAL,
        NET REAL,
        "UNIT WEIGHT" REAL,
        PCS INTEGER,
        "CHECK STATUS" TEXT,               
        FIELD0 TEXT,          
        ITEMNAME TEXT,
        FIELD2 TEXT,
        FIELD3 TEXT,              
        FIELD4 TEXT,
        FIELD5 TEXT,
        HUID TEXT,
        LABOUR TEXT,
        CARAT TEXT,
        FIELD9 TEXT,
        FIELD10 TEXT,
        FIELD11 TEXT,         
        FIELD12 TEXT,
        FIELD13 TEXT,
        FIELD14 TEXT,
        FIELD15 TEXT                                        )
        ''')

        self.table_name = "sales"  # Use a single table name
        self.column_names = [
        "SER NO", "GROSS", "LESS", "NET", "UNIT WEIGHT", "PCS",
        "UNIT RATE", "MRP", "CHECK STATUS", "FIELD0", "ITEMNAME",
        "FIELD2", "FIELD3", "FIELD4", "FIELD5", "HUID", "LABOUR",
        "CARAT", "FIELD9", "FIELD10", "FIELD11", "FIELD12", "FIELD13", "FIELD14", "FIELD15"
        ]

        self.init_ui()
        self.refresh_table()

    def init_ui(self):
        self.import_button = QPushButton("Import Data", self)
        self.import_button.setGeometry(10, 10, 120, 30)
        self.import_button.clicked.connect(self.import_data)

        self.save_button = QPushButton("Save Data", self)
        self.save_button.setGeometry(140, 10, 120, 30)
        self.save_button.clicked.connect(self.save_data)

        self.refresh_button = QPushButton("Refresh Table", self)
        self.refresh_button.setGeometry(270, 10, 120, 30)
        self.refresh_button.clicked.connect(self.refresh_table)

        self.clear_database_button = QPushButton("Clear Database")
        self.clear_database_button.setGeometry(370, 10, 120, 30)
        self.clear_database_button.clicked.connect(self.clear_database)

        self.table = QTableWidget(self)
        self.table.setGeometry(10, 50, 780, 480)
        self.table.setColumnCount(len(self.column_names))
        self.table.setHorizontalHeaderLabels(self.column_names)
        
        
        # Add the clear_database_button to your layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.import_button)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.refresh_button)
        self.layout.addWidget(self.clear_database_button)  # Add this line
        self.layout.addWidget(self.table)
    def import_data(self):
     options = QFileDialog.Options()
     file_path, _ = QFileDialog.getOpenFileName(self, "Import Data", "", "CSV Files (*.csv);;All Files (*)", options=options)

     if file_path:
        try:
            data = pd.read_csv(file_path)
            data.columns = self.column_names  # Ensure the columns match
            data.to_sql(self.table_name, self.db_connection, if_exists="append", index=False)  # Replace data in the table
            self.refresh_table()  # Update the UI to display the imported data
        except Exception as e:
            print(f"Error importing data: {e}")


    def save_data(self):
        # Not needed as data is already saved with import_data
        pass

    def create_table(self):
    # Check if the table exists, if not create it
     self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} ("SER NO" INTEGER PRIMARY KEY)')  # Fix the table creation SQL
     self.db_connection.commit()
     self.refresh_table()

    def refresh_table(self):
        self.cursor.execute(f"PRAGMA table_info({self.table_name})")
        column_info = self.cursor.fetchall()
        column_names = [column[1] for column in column_info]
        self.table.setColumnCount(len(column_names))
        self.table.setHorizontalHeaderLabels(column_names)

        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        data = self.cursor.fetchall()
        self.table.setRowCount(len(data))

        for row_num, record in enumerate(data):
            for col_num, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
                self.table.setItem(row_num, col_num, item)


    def clear_database(self):
        confirm = QMessageBox.question(self, "Clear Database", "Do you want to clear the entire database?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            query = QSqlQuery()
            query.exec("SELECT name FROM sqlite_master WHERE type='table';")
            tables = []
            while query.next():
                tables.append(query.value(0))

            for table in tables:
                query.exec(f"DROP TABLE IF EXISTS {table}")

            self.sales_listbox.clear()
            QMessageBox.information(self, "Database Cleared", "The database has been cleared.")
        else:
            QMessageBox.information(self, "Database Not Cleared", "The database was not cleared.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseManagerApp()
    window.show()
    sys.exit(app.exec_())
