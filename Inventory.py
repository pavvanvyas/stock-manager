import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

class InventoryApp(QMainWindow):
    def __init__(self):
        super(InventoryApp, self).__init__()
        self.setWindowTitle("Inventory")
        self.setGeometry(100, 100, 800, 400)
        self.initUI()
        self.show()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        table_widget = QTableWidget()

        layout.addWidget(table_widget)

        self.load_inventory_data(table_widget)

    def load_inventory_data(self, table_widget):
        connection = sqlite3.connect('stock_manager.db')
        cursor = connection.cursor()

        # Query to fetch item names, counts, sum of gross weight, and sum of net weight
        cursor.execute('''
            SELECT ITEMNAME, COUNT(ITEMNAME), SUM(GROSS) AS GrossWeightSum, SUM(NET) AS NetWeightSum
            FROM sales
            GROUP BY ITEMNAME
        ''')

        data = cursor.fetchall()
        connection.close()

        # Set up the table widget
        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(4)
        table_widget.setHorizontalHeaderLabels(["Item Name", "Quantity", "Gross Weight Sum", "Net Weight Sum"])

        for row, item in enumerate(data):
            for col, value in enumerate(item):
                table_widget.setItem(row, col, QTableWidgetItem(str(value)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    sys.exit(app.exec_())
