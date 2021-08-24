import json


class ZoonTokens():

    def __init__(self, BSC_network, account_info, token_address):
        self.account = account_info
        if not account_info.w3:
            BSC_network.isConnect_w3_address()
            account_info.w3 = BSC_network.w3
        self.w3 = account_info.w3
        with open('contractABI_Pancake.json', 'r') as f:
            self.contractABI = json.load(f)
        self.token_address = token_address
        # self.token_symbol = self.get_symbol(self.token_address)
        self.token_balance = 0

    def get_contract(self, token_address):
        return self.w3.eth.contract(token_address, abi=self.contractABI)

    def get_Zoon_token_balance(self):
        token_address = self.w3.toChecksumAddress(self.token_address)
        contract = self.get_contract(token_address)
        zoon_balance = contract.functions.balanceOf(
            self.account.default_account).call()
        if zoon_balance != 0:
            zoon_balance = zoon_balance / (10**18)
        return zoon_balance
