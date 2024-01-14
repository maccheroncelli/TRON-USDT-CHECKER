import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QMessageBox, QComboBox, QHeaderView, QDesktopWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from collections import defaultdict
import requests
import sqlite3
import webbrowser
import subprocess
import os

def create_label_input(label_text):
    layout = QHBoxLayout()
    label = QLabel(label_text)
    line_edit = QLineEdit()
    layout.addWidget(label)
    layout.addWidget(line_edit)
    return layout, line_edit

class TronUsdtChecker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.centerOnScreen()
        
    def get_exchange_for_address(self, address):
        db_path = './USDT-TRON-HOTWALLETS.DB'       

        if not os.path.exists(db_path):
            self.create_database(db_path)

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT ExchangeName FROM Exchanges INNER JOIN Addresses ON Exchanges.ExchangeID = Addresses.ExchangeID WHERE Address = ?", (address,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else None
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            return None
            
    def create_database(self, db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Create Exchanges table
            cursor.execute("""
                CREATE TABLE Exchanges (
                    ExchangeID INTEGER PRIMARY KEY,
                    ExchangeName TEXT NOT NULL UNIQUE
                );
            """)

            # Create Addresses table
            cursor.execute("""
                CREATE TABLE Addresses (
                    ExchangeID INTEGER,
                    Address TEXT NOT NULL,
                    PRIMARY KEY (ExchangeID, Address),
                    FOREIGN KEY (ExchangeID) REFERENCES Exchanges(ExchangeID)
                );
            """)

            conn.commit()
            conn.close()
        except sqlite3.Error as error:
            print("Error while creating the database", error)

    @staticmethod
    def get_tron_data(wallet_address, token_type, contract_address, limit):
        url = f"https://api.trongrid.io/v1/accounts/{wallet_address}/transactions/{token_type}?&contract_address={contract_address}&only_confirmed=true&limit={limit}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            limit_hit = len(data.get('data', [])) >= limit
            return data, limit_hit
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None, False


    @staticmethod
    def process_tron_data(tron_data, searched_wallet_address):
        if not tron_data:
            return None
        
        transactions = tron_data.get('data', [])
        sent_from = defaultdict(lambda: {'amount': 0, 'count': 0})
        sent_to = defaultdict(lambda: {'amount': 0, 'count': 0})

        for transaction in transactions:
            from_address = transaction.get('from')
            to_address = transaction.get('to')
            amount = float(transaction.get('value', 0)) / 10**6

            if from_address and from_address != searched_wallet_address:
                sent_from[from_address]['amount'] += amount
                sent_from[from_address]['count'] += 1

            if to_address and to_address != searched_wallet_address:
                sent_to[to_address]['amount'] += amount
                sent_to[to_address]['count'] += 1

        # Sort the results by amount
        sent_from = dict(sorted(sent_from.items(), key=lambda item: item[1]['amount'], reverse=True))
        sent_to = dict(sorted(sent_to.items(), key=lambda item: item[1]['amount'], reverse=True))

        return sent_from, sent_to

    def run_search(self):
        wallet_address = self.address_input.text()
        token_type = self.token_type_combo.currentData()
        contract_address = self.contract_combo.currentData()
        api_limit = self.api_limit_input.text()

        try:
            limit = int(api_limit)
            if not 1 <= limit <= 200:
                raise ValueError("Limit must be between 1 and 200")
        except ValueError as e:
            QMessageBox.warning(self, 'Invalid Input', str(e))
            return

        tron_data, limit_hit = self.get_tron_data(wallet_address, token_type, contract_address, limit)
        if limit_hit:
            QMessageBox.warning(self, 'Rate Limit Hit', f"Transaction limit of {limit} reached. Address totals may not be complete. Refer to TRON blockchain explorer for more details.")

        if tron_data:
            processed_data = self.process_tron_data(tron_data, wallet_address)
            if processed_data:
                sent_from, sent_to = processed_data
                self.populate_table(self.from_table, sent_from)
                self.populate_table(self.to_table, sent_to)
            else:
                QMessageBox.warning(self, 'Warning', 'No data found for the provided addresses.')
        else:
            QMessageBox.warning(self, 'Warning', 'No data found or an error occurred.')

            
    def rerun_search(self):
        # Get selected items from both tables
        selected_items_from = self.from_table.selectedItems()
        selected_items_to = self.to_table.selectedItems()

        # Combine selections from both tables
        all_selected_items = selected_items_from + selected_items_to

        # Check if exactly one address is selected
        if len(all_selected_items) == 1:
            selected_address = all_selected_items[0].text()
            self.address_input.setText(selected_address)
            self.run_search()
        else:
            print("Please select only one address.")

    def populate_table(self, table, data):
        table.setColumnCount(4)  # Four columns: Address, No. Trans., Unique Total, Attribution
        table.setHorizontalHeaderLabels(['Address', 'No. Trans.', 'Unique Total', 'Attribution'])
        table.setRowCount(len(data))

        for i, (address, values) in enumerate(data.items()):
            exchange_name = self.get_exchange_for_address(address) or "N/A"
            
            address_item = QTableWidgetItem(address)
            trans_count_item = QTableWidgetItem(str(values['count']))
            amount_item = QTableWidgetItem(f"{values['amount']:,.2f}")
            attribution_item = QTableWidgetItem(exchange_name)

            # Set text alignment to center and make items non-editable
            for item in [address_item, trans_count_item, amount_item, attribution_item]:
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

            # Add items to the table
            table.setItem(i, 0, address_item)
            table.setItem(i, 1, trans_count_item)
            table.setItem(i, 2, amount_item)
            table.setItem(i, 3, attribution_item)

        self.adjust_table_formatting(table)


    def adjust_table_formatting(self, table):
        table.resizeColumnsToContents()
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        font = QFont("Consolas", 8)
        table.setFont(font)
        row_height = font.pointSize() + 4
        for row in range(table.rowCount()):
            table.setRowHeight(row, row_height)
            
    def table_keyPressEvent(self, event):
        if event.key() == Qt.Key_C and (event.modifiers() & Qt.ControlModifier):
            self.copy_selected_cells()
        else:
            # Call the base class method to continue normal event processing
            super(TronUsdtChecker, self).keyPressEvent(event)
            
    def deselectCell(self):
        self.from_table.clearSelection()
        self.to_table.clearSelection()

    def copy_selected_cells(self):
        text = ''
        for table in [self.from_table, self.to_table]:
            selected_ranges = table.selectedRanges()
            for range_ in selected_ranges:
                for row in range(range_.topRow(), range_.bottomRow() + 1):
                    row_text = []
                    for col in range(range_.leftColumn(), range_.rightColumn() + 1):
                        item = table.item(row, col)
                        row_text.append(item.text() if item else '')
                    text += '\t'.join(row_text) + '\n'
        
        QApplication.clipboard().setText(text.strip())  # Remove the last newline character
        
    def on_address_double_clicked(self, item):
        if item.column() == 0:  # Check if the clicked item is in the address column
            address = item.text()
            url = f"https://tronscan.org/#/address/{address}/transfers"
            webbrowser.open(url)
        
    def initUI(self):
        # Set the main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Create wallet address input
        self.address_label = QLabel('Wallet Address:')
        self.address_input = QLineEdit()

        # Create drop-down for the contract address with a default value
        self.contract_label = QLabel('Contract Address:')
        self.contract_combo = QComboBox()
        self.contract_combo.setEditable(True)
        self.contract_combo.addItem('USDT (TRON) - TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t', 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t')
        self.contract_combo.setCurrentIndex(0)  # Set the default selected item

        # Create drop-down for the token type with a default value
        self.token_type_label = QLabel('Token Type:')
        self.token_type_combo = QComboBox()
        self.token_type_combo.setEditable(True)
        self.token_type_combo.addItem('TRC-20', 'trc20')
        self.token_type_combo.setCurrentIndex(0)  # Set the default selected item
        
        # Create API transaction limit input
        self.api_limit_label = QLabel('API Transaction Limit (Default:100, Max 200):')
        self.api_limit_input = QLineEdit('100')
        
        # Create button for viewing/updating the Attribution DB
        self.db_view_update_button = QPushButton('View/Update Attribution DB', self)
        self.db_view_update_button.clicked.connect(self.run_db_script)

        # Create search and exit buttons
        self.search_button = QPushButton('Search')
        self.exit_button = QPushButton('Exit')
        self.rerun_button = QPushButton('Re-run with selected address')

        # Create tables for FROM and TO
        self.from_table = QTableWidget()
        self.to_table = QTableWidget()
        
        # Set the event handler for both tables
        self.from_table.keyPressEvent = self.table_keyPressEvent
        self.to_table.keyPressEvent = self.table_keyPressEvent
        
        # Setup for the 'From' and 'To' tables to select individual cells
        self.from_table.setSelectionMode(QTableWidget.ExtendedSelection)
        self.from_table.setSelectionBehavior(QTableWidget.SelectItems)
        self.to_table.setSelectionMode(QTableWidget.ExtendedSelection)
        self.to_table.setSelectionBehavior(QTableWidget.SelectItems)
        
        # Setup for the double click action to open an instance of Tronscan with default browser.
        self.from_table.itemDoubleClicked.connect(self.on_address_double_clicked)
        self.to_table.itemDoubleClicked.connect(self.on_address_double_clicked)
        
        # Add widgets to the layout
        main_layout.addWidget(self.address_label)
        main_layout.addWidget(self.address_input)
        main_layout.addWidget(self.contract_label)
        main_layout.addWidget(self.contract_combo)
        main_layout.addWidget(self.token_type_label)
        main_layout.addWidget(self.token_type_combo)
        main_layout.addWidget(self.api_limit_label)
        main_layout.addWidget(self.api_limit_input)
        main_layout.addWidget(self.search_button)
        main_layout.addWidget(QLabel('FROM:'))
        main_layout.addWidget(self.from_table)
        main_layout.addWidget(QLabel('TO:'))
        main_layout.addWidget(self.to_table)
        main_layout.addWidget(self.rerun_button)
        main_layout.addWidget(self.db_view_update_button)
        main_layout.addWidget(self.exit_button)

        # Set the central widget
        self.setCentralWidget(main_widget)

        # Connect buttons to functions
        self.search_button.clicked.connect(self.run_search)
        self.exit_button.clicked.connect(self.close)
        self.rerun_button.clicked.connect(self.rerun_search)

        # Set window properties
        self.setWindowTitle('USDT - TRON TRC20 Checker')
        self.setGeometry(300, 300, 1255, 1510)
        
    def run_db_script(self):
        # Running another Python script in the same directory
        script_path = './DB-VIEW-UPDATE.py'  # Relative path to the script in the same directory
        subprocess.Popen(['python', script_path], start_new_session=True) 

    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move(int((resolution.width() / 2) - (self.frameSize().width() / 2)),
                  int((resolution.height() / 2) - (self.frameSize().height() / 2)))       

def main():
    app = QApplication(sys.argv)
    ex = TronUsdtChecker()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()