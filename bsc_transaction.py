from web3 import Web3


class BSCTransaction():
    """
    This module provides methods to work with BSC transaction
    """
    def __init__(self):
        self.bsc = "https://bsc-dataseed.binance.org/"
        self.connect_w3_address()

    def connect_w3_address(self):
        try:
            self.w3 = Web3(Web3.HTTPProvider(self.bsc))
            return self.w3.isConnected()
        except Exception as e:
            print(e)
            return False