# USDT - TRON TRC20 Checker

## Overview
The USDT - TRON TRC20 Checker is a desktop application for analyzing USDT transactions on the TRON network. It fetches and displays transaction data for specified wallet addresses, offering insights into transaction patterns and volumes. It utilizes PyQt5 for its GUI and interacts with the TRONGrid API.

## Minimum Requirements
- Python 3.x
- PyQt5
- Requests library

## Installation and Setup
1. Install Python 3.x from [Python's official website](https://www.python.org/downloads/).
2. Install PyQt5 and requests via pip:

   ```bash
   pip install PyQt5 requests
   ```

3. Clone the repository or download the script.
4. Run the script using Python.

Ensure your environment meets these requirements for smooth operation of the application.

## Features
- **Fetch Transactions**: Retrieves transaction data from the TRON network using wallet addresses, token types, and contract addresses.
- **Customizable Query**: Allows setting the number of transactions to retrieve (up to 200).
- **Transaction Analysis**: Displays the total amount and count of transactions sent to and from different addresses.
- **Re-run Functionality**: Easily re-query the network with a selected address from the table.
- **Copy Functionality**: Enables copying selected data directly from the tables.

## How to Use
1. **Enter Details**: Input the wallet address, contract address (default provided), token type (default 'TRC-20'), and the transaction limit.
2. **Run Search**: Click 'Search' to fetch and display transactions.
3. **Re-run Search**: Select an address from the table and click 'Re-run with selected address' to perform a new search.
4. **Copy Data**: Select table cells and press Ctrl+C to copy data.

## Limitations
- Rate limits from the TRONGrid API may restrict data completeness (max is 200 transactions/transfers).  If you are hitting the limits, more than likely querying an exchange wallet.
- Only supports TRC-20 token types. More can be easily added..
