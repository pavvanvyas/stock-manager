import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QCheckBox
from PyQt5.QtCore import Qt

import sqlite3

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Database Operations')

        self.table_sell = QTableWidget(self)
        self.table_sell.setColumnCount(26)  # Increase the column count for the checkbox column
        self.table_sell.setHorizontalHeaderLabels(["Select", "SER NO", "GROSS", "LESS", "NET", "UNIT WEIGHT", "PCS",
            "UNIT RATE", "MRP", "CHECK STATUS", "FIELD0", "ITEMNAME",
            "FIELD2", "FIELD3", "FIELD4", "FIELD5", "HUID", "LABOUR",
            "CARAT", "FIELD9", "FIELD10", "FIELD11", "FIELD12", "FIELD13", "FIELD14", "FIELD15"])

        self.lbl_sell = QLabel("Table: sales | stock_manager", self)

        self.btn_sell = QPushButton('Sell', self)
        self.btn_sell.clicked.connect(self.sell)

        self.btn_load = QPushButton('Load Data', self)
        self.btn_load.clicked.connect(self.load_data)

        self.table_load = QTableWidget(self)
        self.table_load.setColumnCount(25)  # Adjust based on your columns
        self.table_load.setHorizontalHeaderLabels(["SER NO", "GROSS", "LESS", "NET", "UNIT WEIGHT", "PCS",
            "UNIT RATE", "MRP", "CHECK STATUS", "FIELD0", "ITEMNAME",
            "FIELD2", "FIELD3", "FIELD4", "FIELD5", "HUID", "LABOUR",
            "CARAT", "FIELD9", "FIELD10", "FIELD11", "FIELD12", "FIELD13", "FIELD14", "FIELD15"])

        self.lbl_load = QLabel("Table: sales |  sales_manager", self)

        btn_refresh = QPushButton('Refresh Tables', self)
        btn_refresh.clicked.connect(self.refresh_tables)

        layout = QVBoxLayout()
        layout.addWidget(self.table_sell)
        layout.addWidget(self.lbl_sell)
        layout.addWidget(self.btn_sell)
        layout.addWidget(self.btn_load)
        layout.addWidget(self.table_load)
        layout.addWidget(self.lbl_load)
        layout.addWidget(btn_refresh)

        self.setLayout(layout)

    def refresh_tables(self):
        try:
            stock_conn = sqlite3.connect('stock_manager.db')
            sales_conn = sqlite3.connect('sales_manager.db')

            selected_rows = self.get_selected_rows_from_stock(stock_conn)

            self.insert_into_sales(sales_conn, selected_rows)

            self.delete_from_sales(stock_conn, selected_rows)

            self.update_date_time(sales_conn)

            self.load_data()

            sales_conn.commit()
            stock_conn.commit()

        except Exception as e:
            print(f"Error: {e}")
            sales_conn.rollback()
            stock_conn.rollback()

        finally:
            sales_conn.close()
            stock_conn.close()

    def get_selected_rows_from_stock(self, conn):
        cursor = conn.cursor()
        selected_rows = []

        for row_index in range(self.table_sell.rowCount()):
            if self.table_sell.cellWidget(row_index, 0).isChecked():
                cursor.execute("SELECT * FROM stock WHERE 'SER NO'=?", (self.table_sell.item(row_index, 1).text(),))
                selected_rows.append(cursor.fetchone())

        return selected_rows

    def insert_into_sales(self, conn, selected_rows):
        cursor = conn.cursor()
        for row in selected_rows:
            cursor.execute('''INSERT INTO sales ("SER NO", GROSS, LESS, NET, "UNIT WEIGHT", PCS, "UNIT RATE", MRP,
                "CHECK STATUS", FIELD0, ITEMNAME, FIELD2, FIELD3, FIELD4, FIELD5, HUID, LABOUR,
                CARAT, FIELD9, FIELD10, FIELD11, FIELD12, FIELD13, FIELD14, FIELD15, Date_Time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)  # Replace with actual column names
        conn.commit()

    def delete_from_sales(self, conn, selected_rows):
        cursor = conn.cursor()
        for row in selected_rows:
            cursor.execute("DELETE FROM stock WHERE 'SER NO'=?", (row[0],))  # Assuming 'SER NO' is the primary key
        conn.commit()

    def update_date_time(self, conn):
        cursor = conn.cursor()
        cursor.execute("UPDATE sales SET Date_Time = CURRENT_TIMESTAMP WHERE Date_Time IS NULL")
        conn.commit()

    def load_data(self):
        # Load data into the QTableWidgets

        # Load data for the 'stock' table
        stock_conn = sqlite3.connect('stock_manager.db')
        stock_cursor = stock_conn.cursor()
        stock_cursor.execute("SELECT * FROM sales")
        stock_data = stock_cursor.fetchall()
        stock_conn.close()

        self.table_sell.setRowCount(len(stock_data))
        for row_index, row in enumerate(stock_data):
            # Add checkboxes to the first column
            checkbox = QCheckBox()
            self.table_sell.setCellWidget(row_index, 0, checkbox)

            for col_index, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table_sell.setItem(row_index, col_index + 1, item)

    def sell(self):
        # Sell items logic

        # Get selected rows from the 'sales' table
        selected_rows = self.get_selected_rows_from_stock()

        # Update 'sales' table with the selected rows
        sales_conn = sqlite3.connect('sales_manager.db')
        sales_cursor = sales_conn.cursor()

        for row in selected_rows:
            sales_cursor.execute('''INSERT INTO sales ("SER NO", GROSS, LESS, NET, "UNIT WEIGHT", PCS, "UNIT RATE", MRP,
                    "CHECK STATUS", FIELD0, ITEMNAME, FIELD2, FIELD3, FIELD4, FIELD5, HUID, LABOUR,
                    CARAT, FIELD9, FIELD10, FIELD11, FIELD12, FIELD13, FIELD14, FIELD15, Date_Time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                row["SER NO"], row["GROSS"], row["LESS"], row["NET"], row["UNIT WEIGHT"], row["PCS"],
                row["UNIT RATE"],
                row["MRP"], row["CHECK STATUS"], row["FIELD0"], row["ITEMNAME"], row["FIELD2"], row["FIELD3"],
                row["FIELD4"], row["FIELD5"], row["HUID"], row["LABOUR"], row["CARAT"], row["FIELD9"],
                row["FIELD10"],
                row["FIELD11"], row["FIELD12"], row["FIELD13"], row["FIELD14"], row["FIELD15"], None))  # Replace with actual column names

        sales_conn.commit()
        sales_conn.close()

        # Remove sold items from the 'stock' table
        stock_conn = sqlite3.connect('stock_manager.db')
        stock_cursor = stock_conn.cursor()

        for row in selected_rows:
            stock_cursor.execute("DELETE FROM sales WHERE 'SER NO'=?", (row["SER NO"],))  # Assuming 'SER NO' is the primary key

        stock_conn.commit()
        stock_conn.close()

        # Refresh the tables after selling
        self.refresh_tables()

        # Update the displayed table
        self.update_displayed_table()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
