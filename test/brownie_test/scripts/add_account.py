from brownie import accounts, config

def add_account(private_key):
    accounts.add(private_key)

def main():
    add_account(config["wallets"]["from_key"])