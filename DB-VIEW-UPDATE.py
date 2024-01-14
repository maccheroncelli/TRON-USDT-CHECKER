import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QTextEdit, QLabel, QMessageBox, QRadioButton, QDesktopWidget

class DatabaseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.centerOnScreen()

    def initUI(self):
        # Set up the main widget and layout
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)

        # Radio buttons for 'EDIT DB' and 'VIEW DB'
        self.edit_button = QRadioButton('Add new exchanges and/or addresses to DB..', self)
        self.view_button = QRadioButton('View database entries for each exchange..', self)
        self.edit_button.setChecked(True)  # Set EDIT as default checked
        self.edit_button.toggled.connect(self.toggle_mode)  # Connect to toggle_mode
        self.view_button.toggled.connect(self.toggle_mode)

        # Vertical layout for radio buttons
        toggle_layout = QVBoxLayout()
        toggle_layout.addWidget(self.edit_button)
        toggle_layout.addWidget(self.view_button)
        main_layout.addLayout(toggle_layout)

        # Dropdown box for exchanges
        self.exchange_combo = QComboBox(self)
        self.exchange_combo.setEditable(True)
        self.load_exchanges()  # Function to load exchange names
        main_layout.addWidget(self.exchange_combo)

        # Text area for addresses
        self.address_text_area = QTextEdit(self)
        main_layout.addWidget(self.address_text_area)

        # 'OK' button
        self.ok_button = QPushButton('OK', self)
        self.ok_button.clicked.connect(self.on_ok_clicked)
        main_layout.addWidget(self.ok_button)

        # Set the central widget and window properties
        self.setCentralWidget(main_widget)
        self.setWindowTitle('Database Viewer & Editor')
        self.setGeometry(100, 100, 800, 600)

    def toggle_mode(self):
        if self.sender() == self.view_button:
            self.edit_button.setChecked(False)
            self.enable_view_mode()
            self.address_text_area.clear()  # Clear the text area
            # Do not call load_exchanges or load_from_database here
        elif self.sender() == self.edit_button:
            self.view_button.setChecked(False)
            self.enable_edit_mode()
            self.load_exchanges()  # Refresh the dropdown list for edit mode

    
    def enable_edit_mode(self):
        # Logic to set the application in edit mode
        self.address_text_area.setReadOnly(False)
        self.address_text_area.clear()

    def enable_view_mode(self):
        # Logic to set the application in view mode
        self.address_text_area.setReadOnly(True)
        # Optionally, load data immediately upon switching to view mode
        self.load_from_database()  
            
    def load_exchanges(self):
        self.exchange_combo.clear()  # Clear existing items
        self.exchange_combo.addItem("")  # Add a blank first selection
        try:
            conn = sqlite3.connect('USDT-TRON-HOTWALLETS.DB')
            cursor = conn.cursor()
            cursor.execute("SELECT ExchangeName FROM Exchanges")
            exchanges = cursor.fetchall()
            for exchange in exchanges:
                self.exchange_combo.addItem(exchange[0])
            conn.close()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    def save_to_database(self):
        exchange_name = self.exchange_combo.currentText().strip()
        addresses = self.address_text_area.toPlainText().strip().split('\n')
        new_exchange_added = False
        addresses_added = 0
        existing_addresses = []
        valid_addresses = [addr for addr in addresses if addr.strip() and self.is_valid_tron_address(addr)]

        if not valid_addresses:
            QMessageBox.warning(self, 'Warning', 'No valid TRON addresses found.')
            return new_exchange_added, addresses_added, existing_addresses

        try:
            conn = sqlite3.connect('USDT-TRON-HOTWALLETS.DB')
            cursor = conn.cursor()

            # Check if the exchange exists
            cursor.execute("SELECT ExchangeID FROM Exchanges WHERE ExchangeName = ?", (exchange_name,))
            result = cursor.fetchone()

            if result:
                exchange_id = result[0]
            else:
                # Insert new exchange and get its ID
                cursor.execute("INSERT INTO Exchanges (ExchangeName) VALUES (?)", (exchange_name,))
                exchange_id = cursor.lastrowid
                new_exchange_added = True

            for address in valid_addresses:
                cursor.execute("SELECT Address FROM Addresses WHERE ExchangeID = ? AND Address = ?", (exchange_id, address))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO Addresses (ExchangeID, Address) VALUES (?, ?)", (exchange_id, address))
                    addresses_added += 1
                else:
                    existing_addresses.append(address)

            conn.commit()
            conn.close()
        except sqlite3.Error as error:
            # Optionally, you can log the error to a file or console instead of showing it to the user.
            print("Database Error:", error)

        return new_exchange_added, addresses_added, existing_addresses

    def is_valid_tron_address(self, address):
        return len(address) == 34 and address.startswith('T')


    def is_valid_tron_address(self, address):
        return len(address) == 34 and address.startswith('T')


    def load_from_database(self):
        exchange_name = self.exchange_combo.currentText().strip()

        if not exchange_name:
            # Clear the text area if no exchange is selected
            self.address_text_area.clear()
            return

        try:
            # Connect to the database
            conn = sqlite3.connect('USDT-TRON-HOTWALLETS.DB')
            cursor = conn.cursor()

            # Fetch the exchange ID
            cursor.execute("SELECT ExchangeID FROM Exchanges WHERE ExchangeName = ?", (exchange_name,))
            result = cursor.fetchone()

            if result:
                exchange_id = result[0]
                # Fetch addresses for the selected exchange
                cursor.execute("SELECT Address FROM Addresses WHERE ExchangeID = ?", (exchange_id,))
                addresses = cursor.fetchall()

                # Display addresses in the text area
                formatted_addresses = '\n'.join([address[0] for address in addresses])
                self.address_text_area.setText(formatted_addresses)

            conn.close()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            
    def on_ok_clicked(self):
        if self.edit_button.isChecked():
            exchange_name = self.exchange_combo.currentText().strip()
            addresses = self.address_text_area.toPlainText().strip().split('\n')
            valid_addresses = [addr for addr in addresses if addr.strip() and self.is_valid_tron_address(addr)]

            if not valid_addresses:
                QMessageBox.warning(self, 'Warning', 'No valid TRON addresses found.')
                return

            # Save to database and provide feedback
            new_exchange_added, addresses_added, existing_addresses = self.save_to_database()
            
            if addresses_added > 0 or new_exchange_added:
                success_message = ""
                if new_exchange_added:
                    success_message += f"New exchange '{exchange_name}' added successfully.\n"
                if addresses_added:
                    success_message += f"{addresses_added} new addresses added successfully.\n"
                if existing_addresses:
                    success_message += f'These addresses already exist in the database:\n' + '\n'.join(existing_addresses)
                QMessageBox.information(self, 'Success', success_message)
            elif existing_addresses:
                QMessageBox.information(self, 'Existing Addresses', f'These addresses already exist in the database:\n' + '\n'.join(existing_addresses))

        elif self.view_button.isChecked():
            # Load from database for VIEW mode
            self.load_from_database()
            
    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move(int((resolution.width() / 2) - (self.frameSize().width() / 2)),
                  int((resolution.height() / 2) - (self.frameSize().height() / 2)))
            
def main():
    app = QApplication(sys.argv)
    ex = DatabaseApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()