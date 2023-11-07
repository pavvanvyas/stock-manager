import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QLineEdit, QLabel, QDateTimeEdit
from PyQt5.Qt import QDateTime

class DatabaseApp(QMainWindow):
    def __init__(self):
        super(DatabaseApp, self).__init__()
        self.setWindowTitle("Database App")
        self.setGeometry(100, 100, 800, 400)
         
        self.initUI()
        self.show()

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.sell_button = QPushButton("Sell")
        self.load_button = QPushButton("Load Data")
  
        self.table_widget = QTableWidget()

        self.layout.addWidget(self.sell_button)
        self.layout.addWidget(self.load_button)
       
        self.layout.addWidget(self.table_widget)

        self.sell_button.clicked.connect(self.sell_selected_row)
        self.load_button.clicked.connect(self.load_data)
        self.db_connection = sqlite3.connect("sales_manager.db")

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
            FIELD15 TEXT,
            "SALE DATE" TEXT  -- Add SALE DATE column
                  )  ''')

        self.load_data()

    def load_data(self):
        connection = sqlite3.connect('stock_manager.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM sales')
        data = cursor.fetchall()
        connection.close()

        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(26)  # Increased to accommodate "SALE DATE" column
        self.table_widget.setHorizontalHeaderLabels(["SER NO", "GROSS", "LESS", "NET", "UNIT WEIGHT", "PCS",
            "UNIT RATE", "MRP", "CHECK STATUS", "FIELD0", "ITEMNAME",
            "FIELD2", "FIELD3", "FIELD4", "FIELD5", "HUID", "LABOUR",
            "CARAT", "FIELD9", "FIELD10", "FIELD11", "FIELD12", "FIELD13", "FIELD14", "FIELD15", "SALE DATE"])

        for row, item in enumerate(data):
            for col, value in enumerate(item):
                self.table_widget.setItem(row, col, QTableWidgetItem(str(value)))

    def sell_selected_row(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            selected_row_data = [self.table_widget.item(selected_row, col).text() for col in range(25)]
            
            # Add the current date and time
            current_datetime = QDateTime.currentDateTime().toString()
            selected_row_data.append(current_datetime)
            
            # Step 1: Add the selected row to 'sales_manager.db' 's sales table
            connection_sales_manager = sqlite3.connect('sales_manager.db')
            cursor_sales_manager = connection_sales_manager.cursor()
            
            # Insert the row into 'sales' table in 'sales_manager.db' with the added "SALE DATE"
            cursor_sales_manager.execute('''
                INSERT INTO sales ("SER NO", GROSS, LESS, NET, "UNIT WEIGHT", PCS, "UNIT RATE", MRP,
                    "CHECK STATUS", FIELD0, ITEMNAME, FIELD2, FIELD3, FIELD4, FIELD5, HUID, LABOUR,
                    CARAT, FIELD9, FIELD10, FIELD11, FIELD12, FIELD13, FIELD14, FIELD15, "SALE DATE")
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', selected_row_data)
            
            connection_sales_manager.commit()
            connection_sales_manager.close()
            
            # Step 2: Delete the row from 'stock_manager.db' 's sales table
            connection_stock_manager = sqlite3.connect('stock_manager.db')
            cursor_stock_manager = connection_stock_manager.cursor()
            ser_no = selected_row_data[0]
            
            # Delete the row from 'sales' table in 'stock_manager.db'
            cursor_stock_manager.execute('DELETE FROM sales WHERE "SER NO"=?', (ser_no,))
            connection_stock_manager.commit()
            connection_stock_manager.close()
            
            self.load_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseApp()
    window.show()
    sys.exit(app.exec_())

