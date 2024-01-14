# USDT - TRON TRC20 Checker

## Overview
The USDT - TRON TRC20 Checker is an advanced desktop tool for analyzing USDT transactions on the TRON network. Featuring a robust GUI developed with PyQt5, it extends its functionality to include attribution of transactions to known exchange hot wallets and direct Tronscan access for address details.

## Minimum Requirements
- Python 3.x
- PyQt5
- Requests library
- SQLite3

## Installation and Setup
1. Install Python 3.x from [Python's official website](https://www.python.org/downloads/).
2. Install PyQt5, requests, and SQLite3 via pip:

   ```bash
   pip install PyQt5 requests sqlite3
   ```
   
3. Clone the repository or download both 'tron_usdt_checker.py' **and** 'db_view_update.py'.
4. The Database file (Optional) comes pre-filled with Binance TRON/USDT Hotwallets as of '01/14/2024'.  This file will be created upon first run regardless.
5. Run 'tron_usdt_checker.py' using Python.

## Features
- **Data Fetching & Analysis**: Retrieves and analyzes transactions from the TRON network.
- **Customizable Query**: Set the number of transactions to retrieve (up to 200).
- **Transaction Attribution**: Identifies transactions linked to known exchange hot wallets.
- **Database View/Update**: A separate script ('db_view_update.py') to view and update exchange hot wallet information in the database.
- **Direct Tronscan Access**: Double-click an address to view its details on Tronscan.
- **Copy Functionality**: Copy data directly from the tables.
- **Re-run Functionality**: Re-query with a selected address.

## How to Use
1. **Enter Details**: Input the wallet address, contract address, token type, and transaction limit.
2. **Run Search**: Click 'Search' to fetch and display transactions.
3. **View/Update Database**: Use the separate script to manage hot wallet attribution data.
4. **Copy Data**: Select and copy table cells data.
5. **Tronscan Access**: Double-click an address to open its Tronscan page.

## Hot Wallets - Additional Resources
- To find out the specific Hot Wallets that exchanges use and potentially include them into the Database, visit CoinMarketCap's [Proof of Reserves](https://coinmarketcap.com/academy/article/cmc-launches-proof-of-reserves) and [Exchange Rankings](https://coinmarketcap.com/rankings/exchanges/) pages.  All the information you require is there...

## Limitations
- Restricted by the TRONGrid API's rate limits, especially when querying exchange wallets.
- Primarily supports TRC-20 token types, with potential to add more.

Ensure you have both scripts in the same directory for full functionality. The application provides a holistic view of TRON transactions, making it a valuable asset for users interested in detailed blockchain analysis.

## Screenshot
![Screenshot 2024-01-14 162058](https://github.com/maccheroncelli/TRON-USDT-CHECKER/assets/154501937/90ef5a82-75ce-49c9-9dc1-6765a89e6039)
![Screenshot 2024-01-14 155946](https://github.com/maccheroncelli/TRON-USDT-CHECKER/assets/154501937/d5694095-c164-4f5c-bc2c-21113d12b653)




