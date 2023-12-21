```markdown
# TRON Wallet Address Search

## Minimum Requirements
- Python 3.x
- Required Python packages:
```

  ```bash
  pip install requests argparse
  ```

## Functionality

- This script retrieves transaction data for a TRON wallet address.
- It displays transactions sent from and to the specified wallet address.
- The results include the address, unique total amount, and can be sorted in descending order based on the total amount.
- You can enter the number next to a resulting TRON address to run another check with that address.

## Usage

4. Run the script with the following command:
   ```bash
   python script.py -a <WALLET_ADDRESS>
   ```

   Replace `<WALLET_ADDRESS>` with the TRON wallet address you want to search.

5. Follow the on-screen instructions to navigate through the results.
   - Enter 'exit' to quit the script.
   - Enter the number next to a TRON address to run another check with that address.

6. To exit the script, enter 'exit' when prompted.

## Example
   ```bash
   python script.py -a TTVkMTYuNBEwaap6omzivNunc5KnSkv2wx
   ```

   This command searches for transactions related to the specified wallet address.
