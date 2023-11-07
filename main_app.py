import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QStackedWidget,QMessageBox, QDialog,QVBoxLayout, QWidget, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog,QInputDialog, QLineEdit
import pandas as pd
import sqlite3
import hashlib
from createsale import DatabaseApp
from managesales import SalesApplication
from salesreport import SalesApp
from stock import DatabaseManagerApp
from file import FileManagementApp
from Inventory import InventoryApp
class ItemManagerApp(QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.setWindowTitle("Item Manager Application")
        self.setGeometry(100, 100, 800, 600)
        self.current_database = None  # Store the current database filename
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.menu_bar = self.menuBar()
        self.create_menus()
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)
        self.init_ui()
         # Create an instance of DatabaseApp
        self.database_app = DatabaseApp()
        self.database_app.hide() 
         # Create an instance of Datanentry window
        self.SalesApplication = SalesApplication()
        self.SalesApplication.hide()
         # Create an instance of Salesapp window
        self.SalesApp = SalesApp()
        self.SalesApp.hide()
        #create  an instance of DatabaseManagerApp window
        self.DatabaseManagerApp = DatabaseManagerApp()
        self.DatabaseManagerApp.hide()
        #create an instance of InventoryApp window
        self.InventoryApp =InventoryApp()
        self.InventoryApp.hide()
    def create_menus(self):
        file_menu = self.menu_bar.addMenu("File")
        sales_menu = self.menu_bar.addMenu("Sales")
        item_menu = self.menu_bar.addMenu("Stock")
        activity_menu = self.menu_bar.addMenu("Activity")
        help_menu = self.menu_bar.addMenu("Help")

        self.create_file_menu_actions(file_menu)
        self.create_sales_menu_actions(sales_menu)
        self.create_item_menu_actions(item_menu)
        self.create_help_menu_actions(help_menu)
    def create_menu_action(self, text, slot=None):
        action = QAction(text, self)
        if slot is not None:
            action.triggered.connect(slot)
        return action
    def create_file_menu_actions(self,menu):
        menu.addAction(self.create_menu_action("manage files",self.show_manage_FileManagementApp))
    def create_sales_menu_actions(self, menu):
        menu.addAction(self.create_menu_action("Create Sale",self.show_database_app ))
        menu.addAction(self.create_menu_action("Manage Sales",self.show_manage_sales_window))
        menu.addAction(self.create_menu_action("Sales Reports",self.show_manage_Salesapp))
    def create_item_menu_actions(self, menu):
        menu.addAction(self.create_menu_action("Add Items",self.show_manage_database_window))
        menu.addAction(self.create_menu_action("View Inventory",self.show_manage_InventoryApp ))
    def create_help_menu_actions(self, menu):
     menu.addAction(self.create_menu_action("About", self.show_about_dialog))
     menu.addAction(self.create_menu_action("Documentation", self.show_documentation))
    def show_about_dialog(self):
     about_text = "Item Manager Application\n\n" \
                 "Version: 1.0\n" \
                 "Creator: paavan vyas\n" \
                 "Contact : +918866679929\n"\
                 "Company: Arids Marketing"
     about_dialog = QDialog(self)
     about_dialog.setWindowTitle("About Item Manager Application")
     about_layout = QVBoxLayout()
     about_label = QLabel(about_text)
     about_layout.addWidget(about_label)
     about_dialog.setLayout(about_layout)
     about_dialog.exec_()
    def create_menu_action(self, text, slot=None):
        action = QAction(text, self)
        if slot is not None:
            action.triggered.connect(slot)
        return action
    def show_documentation(self):
     documentation_text = """
      Item Manager Application Documentation
      Introduction
      The Item Manager Application is a graphical user interface (GUI) program designed to help users manage items, sales, and user profiles. It allows users to create, edit, and view data related to items, sales, and user information.
      Features
      1. User Authentication
      Users can log in using their username and password or create a new account.
      Passwords are securely hashed for authentication.
      2. Item Management
      Users can add, edit, and view items in the inventory.
      Items are stored in a database with information such as product name, quantity, and price.
      3. Sales Management
      Users can create sales records, specifying product name, quantity, and price.
      Sales data can be saved to a database for future reference.
      4. Data Management
      Users can create and manage tables in the database to organize their data.
      Data can be imported from CSV or Excel files into the application.
      5. User Profile
      Users have a profile that includes their username, full name, and email.
      They can edit their profile information.
      6. Database Interaction
      Users can create new databases, open existing ones, and save data to databases.
      Version: 1.0
      License: [Your License Name] License (open-source)
      Developer: Paavan Vyas
      Contact: PAVANVYAS481@gmail.com
      Acknowledgments
      We acknowledge the developers of PyQt5, SQLite, and Pandas for their valuable contributions to this project.
     """
     documentation_box = QMessageBox()
     documentation_box.setWindowTitle("Documentation")
     documentation_box.setText(documentation_text)
     documentation_box.exec_()
    def init_ui(self):
        self.show_content("New File")
    def show_content(self, content_name):
        content_widget = QLabel(f"This is the {content_name} content.")
        self.stacked_widget.addWidget(content_widget)
        self.stacked_widget.setCurrentWidget(content_widget)
      # Define a function to show the DatabaseApp window
    def show_database_app(self):
        self.database_app = DatabaseApp()
        self.database_app.show()
    
    def show_manage_sales_window(self):
        self.SalesApplication= SalesApplication()
        self.SalesApplication.show()
    
    def show_manage_Salesapp(self):
        self.SalesApp = SalesApp()
        self.SalesApp.show()
        
    def show_manage_database_window(self):
        self.DatabaseManagerApp = DatabaseManagerApp()
        self.DatabaseManagerApp.show()

    def show_manage_FileManagementApp(self):
        self.FileManagementApp = FileManagementApp()
        self.FileManagementApp.show()
    
    def show_manage_InventoryApp(self):
        self.InventoryApp =InventoryApp()
        self.InventoryApp.show()
       
def main():
    app = QApplication(sys.argv)
    window = ItemManagerApp()
    window.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
