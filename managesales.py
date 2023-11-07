import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QDialog, QListWidget, QMessageBox, QHBoxLayout, QLineEdit, QLabel, QScrollArea
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from datetime import datetime

class DataEntryWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Entry")
        self.setGeometry(100, 100, 400, 400)

        self.column_labels = [
            "SER NO", "GROSS", "LESS", "NET", "UNIT WEIGHT", "PCS", "UNIT RATE",
            "MRP", "CHECK STATUS", "FIELD0", "ITEMNAME", "FIELD2", "FIELD3", "FIELD4",
            "FIELD5", "HUID", "LABOUR", "CARAT", "FIELD9", "FIELD10", "FIELD11",
            "FIELD12", "FIELD13", "FIELD14", "FIELD15"
        ]

        self.column_entries = {}
        layout = QVBoxLayout()

        for column_name in self.column_labels:
            label = QLabel(column_name + ":")
            entry = QLineEdit()
            self.column_entries[column_name] = entry
            layout.addWidget(label)
            layout.addWidget(entry)

        self.sell_button = QPushButton("Sell")
        self.sell_button.clicked.connect(self.add_sale)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.addLayout(layout)
        scroll_layout.addWidget(self.sell_button)
        scroll_widget.setLayout(scroll_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def add_sale(self):
        values = [self.column_entries[column_name].text() for column_name in self.column_labels]
        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query = QSqlQuery()
        query.prepare(f"INSERT INTO sales ({', '.join(self.column_labels)}, date_time) VALUES ({', '.join(['?'] * len(self.column_labels))}, ?)")

        for value in values:
            query.addBindValue(value)
        query.addBindValue(current_date_time)

        if query.exec_():
            QMessageBox.information(self, "Success", "Data has been added to the database.")
            self.clear_fields()

    def clear_fields(self):
        for entry in self.column_entries.values():
            entry.clear()

class SalesApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sales Management Application")
        self.setGeometry(100, 100, 400, 400)

        self.open_entry_window_button = QPushButton("Open Data Entry Window")
        self.open_entry_window_button.clicked.connect(self.open_data_entry_window)

        self.load_button = QPushButton("Load")
        self.load_button.clicked.connect(self.load_data)

        self.clear_database_button = QPushButton("Clear Database")
        self.clear_database_button.clicked.connect(self.clear_database)

        self.sales_listbox = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.open_entry_window_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.clear_database_button)
        layout.addWidget(self.sales_listbox)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_data_entry_window(self):
        data_entry_window = DataEntryWindow()
        data_entry_window.exec_()

    def load_data(self):
        query = QSqlQuery("SELECT * FROM sales")
        self.sales_listbox.clear()
        while query.next():
            values = [query.value(i) for i in range(len(self.column_labels) + 1)]
            date_time = values[-1]
            values = values[:-1]

            formatted_values = ", ".join(f"{column_name}: {value}" for column_name, value in zip(self.column_labels, values))
            self.sales_listbox.addItem(f"{formatted_values}, Time: {date_time}")

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName("sales_database.db")
    if not database.open():
        sys.exit(1)

    mainWin = SalesApplication()
    mainWin.show()
    sys.exit(app.exec_())
