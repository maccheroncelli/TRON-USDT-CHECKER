# TRON USDT CHECKER

## Minimum Requirements
- Python 3.x
- Required Python packages:

  ```bash
  pip install requests argparse prettytable

## Functionality

- This script retrieves transaction data for a TRON wallet address via Trongrid API.
- Does not list individual transactions, only lists the total value of USDT per address sent to/from the searched address.
- This helps to easily identify the addresses that are sending the most USDT, instead of reading multiple pages of transfers on blockchain explorer websites.
- You can enter the number next to a resulting TRON address to run another check with that address.

## Usage

4. Run the script with the following command:
   ```bash
   python TRON-USDT-CHECKER.py -a <WALLET_ADDRESS>
   ```

   Replace `<WALLET_ADDRESS>` with the TRON wallet address you want to search.

5. Follow the on-screen instructions to navigate through the results.
   - Enter 'exit' to quit the script.
   - Enter the number next to a TRON address to run another check with that address.

6. To exit the script, enter 'exit' when prompted.

## Example
   ```bash
   python TRON-USDT-CHECKER.py -a TUNuXdhr3KSzt8LyPz8618uhLkLdzSKCBv
   ```

   This command searches for transactions related to the specified wallet address.

![image](https://github.com/maccheroncelli/TRON-USDT-CHECKER/assets/154501937/872bfb90-1ead-4676-97af-11a63607b0a4)


