import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt

class SalesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sales Database Viewer')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Filter options
        self.filter_criteria = []

        self.filter_layout = QVBoxLayout()
        self.add_filter_button = QPushButton('Add Filter')
        self.add_filter_button.clicked.connect(self.add_filter)
        self.show_all_button = QPushButton('Show All')
        self.show_all_button.clicked.connect(self.show_all_data)
        self.search_button = QPushButton('Search')
        self.search_button.clicked.connect(self.filter_data)

        self.filter_layout.addWidget(QLabel('Filter by:'))
        self.filter_layout.addWidget(self.add_filter_button)
        self.filter_layout.addWidget(self.show_all_button)
        self.filter_layout.addWidget(self.search_button)

        self.layout.addLayout(self.filter_layout)

        # Data table
        self.table = QTableWidget(self)

        self.central_widget.setLayout(self.layout)

        self.db_connection = sqlite3.connect('sales_manager.db')
        
         # Create a table named 'sales' with appropriate columns
        cursor = self.db_connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            "SER NO" INTEGER PRIMARY KEY,
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
            FIELD15 TEXT                                        
                  )  ''')

       
        self.load_data()

    def add_filter(self):
        if len(self.filter_criteria) >= 4:
            return  # Maximum 4 filter conditions allowed

        filter_widget = QWidget()
        filter_layout = QHBoxLayout()

        column_selector = QComboBox()
        column_names = self.get_column_names()
        column_selector.addItem('All Columns')  # Option to show all columns
        column_selector.addItems(column_names)

        operator_selector = QComboBox()
        operator_selector.addItems(['=', '>', '<'])

        value_input = QLineEdit()

        filter_layout.addWidget(column_selector)
        filter_layout.addWidget(operator_selector)
        filter_layout.addWidget(value_input)

        filter_widget.setLayout(filter_layout)
        self.filter_layout.addWidget(filter_widget)

        self.filter_criteria.append((column_selector, operator_selector, value_input))

    def show_all_data(self):
        # Clear the filters and reload all data
        for criteria in self.filter_criteria:
            criteria[0].setCurrentText('All Columns')
            criteria[1].setCurrentText('=')
            criteria[2].setText('')

        self.filter_data()

    def get_column_names(self):
        cursor = self.db_connection.cursor()
        cursor.execute("PRAGMA table_info(sales)")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        cursor.close()
        return column_names

    def filter_data(self):
        try:
            query = "SELECT * FROM sales"
            criteria = []
            for column_selector, operator_selector, value_input in self.filter_criteria:
                column = column_selector.currentText()
                operator = operator_selector.currentText()
                value = value_input.text()
                if column != 'All Columns' and value:
                    criteria.append(f"{column} {operator} '{value}'")
            if criteria:
                query += " WHERE " + " AND ".join(criteria)
            cursor = self.db_connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            self.load_data(result)
        except sqlite3.Error as e:
            print("SQLite error:", e)

    def load_data(self, data=None):
        self.table.clear()  # Clear the table before populating it

        if data is None:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM sales")
            data = cursor.fetchall()
            cursor.close()

        self.table.setRowCount(len(data))
        if data:
            self.table.setColumnCount(len(data[0]))
            self.table.setHorizontalHeaderLabels(self.get_column_names())  # Set column names as headers

        for row_index, row_data in enumerate(data):
            for column_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.table.setItem(row_index, column_index, item)
        self.layout.addWidget(self.table)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SalesApp()
    window.show()
    sys.exit(app.exec_())
