from web3 import Web3


class Account():
    """
    This module provides methods to work with wallet account
    """
    default_account = ''

    def __init__(self, w3, private_key):
        self.w3 = w3
        self.private_key = private_key
        self.connect_account(private_key)

    def connect_account(self, private_key):
        try:
            self.account = self.w3.eth.account.privateKeyToAccount(private_key)
            self.set_default_account()
            self.last_nonce = self.w3.eth.getTransactionCount(
                self.account.address)
            print("Connect to account successfully")
            print(f'The last nonce of account is: {self.last_nonce}')
        except Exception as e:
            print(e)

    def set_default_account(self):
        self.default_account = self.account.address

    def build_transaction(self, petID, monsterType):
        # petID is the ID of NFT item provided by BSC network
        # # Monster Type will be 0,1,2,3 corresding from easiest to hardest
        target_address = self.w3.toChecksumAddress(
            '0xf70c08a428f300c7f3e3f09217211d21f7a50410')

        # target_address = self.w3.toChecksumAddress(
        #     '0xB9c0E9D49eC3F5f059d767DE2E8BFFea8983fda8')

        petID_hex = hex(int(petID))
        petID_hex = petID_hex[2:]

        if (len(petID_hex) == 5):
            string_data = '0x88f56f0900000000000000000000000000000000000000000000000000000000000' + \
                petID_hex + '000000000000000000000000000000000000000000000000000000000000000' + \
                str(monsterType)
        else:
            string_data = '0x88f56f09000000000000000000000000000000000000000000000000000000000000' + \
                petID_hex + '000000000000000000000000000000000000000000000000000000000000000' + \
                str(monsterType)

        raw_transaction = {
            'to': target_address,
            'value': Web3.toWei(0, "ether"),
            'gas':  int(300000),
            'gasPrice': Web3.toWei('5', "gwei"),
            'data': string_data,
            'nonce': self.w3.eth.getTransactionCount(self.account.address),
            'chainId': 56
        }
        #print(raw_transaction)
        return raw_transaction

    def transaction_auto_sequence(self, raw_transaction):
        singed_raw_transaction = self.w3.eth.account.sign_transaction(
            raw_transaction, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(
            singed_raw_transaction.rawTransaction)

        tx_hash = self.w3.toHex(tx_hash)

        return tx_hash

    def get_transaction_gas_fee(self, tx_hash):
        gas_used = self.w3.eth.getTransactionReceipt(tx_hash).gasUsed
        transacion_cost = 0.000000005 * gas_used  # ( gWei: 5)

        return transacion_cost            # BNB value
