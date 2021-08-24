from datetime import datetime, timedelta
import time

from account import Account
from bsc_transaction import BSCTransaction
from tokens import ZoonTokens
from utilities import *


class ZoonPlay():
    """
    This module provide methods to work with Zoon
    """
    configs_file = "config.json"
    tracking_file = "tracking.csv"

    def __init__(self):
        self.configs = read_config(self.configs_file)
        self.private = self.configs["private"]
        self.pets = self.configs["pets"]
        self.waittime = self.configs["waittime"]
        self.zoon_address = self.configs["ZoonAddress"]
        self.bsc = BSCTransaction()
        self.w3 = self.bsc.w3
        self.account = Account(self.w3, self.private)
        self.zoon_token = ZoonTokens(
            self.bsc, self.account, '0x9d173e6c594f479b4d47001f8e6a95a7adda42bc')
        self.app_running = True
        while self.app_running:
            self.play_zoon()

    def get_last_play(self):
        tracking_log = read_tracking(self.tracking_file)
        logs = [row.strip().split(',')
                for row in tracking_log.strip().split("\n") if row]
        pet_plays = [row for row in logs]
        return pet_plays[-1] if len(pet_plays) > 1 else []

    def play_zoon(self):
        last_play = self.get_last_play()
        last_play_time = datetime.strptime(
            last_play[0], self.configs['TimeFormat']) if last_play else datetime.min
        waittime = max(
            0, self.configs['waittime']*3600 - (datetime.now() - last_play_time).seconds + 1)
        print(f"Now is {datetime.now().strftime('%H:%M:%S')}. {timedelta(seconds=waittime)} to next turn...")
        time.sleep(waittime)
        print("==================")
        print("Start playing zoon")
        for pet in self.pets:
            self.send_play_transaction(pet)

    def send_play_transaction(self, pet):
        try:
            petID = pet['id']
            print(f"Playing pet {petID}")
            turns = pet['rare']
            monsterType = self.configs['monsterTypes'][str(pet['winrate'])]
            for turn in range(1, 1 + turns):
                raw_transaction = self.account.build_transaction(
                    petID, monsterType)
                tx_hash = self.account.transaction_auto_sequence(
                    raw_transaction)
                self.account.w3.eth.waitForTransactionReceipt(
                    tx_hash, 360)
                time.sleep(5)

                fee = self.account.get_transaction_gas_fee(tx_hash)
                now = datetime.now().strftime(self.configs['TimeFormat'])
                log = ",".join(
                    [now, petID, str(turn), str(fee)])
                print(log)
                write_tracking(log)
            print(f"Finish playing pet {petID} at turn {turn}")
        except Exception as e:
            print(e)
