#!/usr/bin/python3
import os
from brownie import SimpleCollectible, accounts, network, config


def deploy_simple(private_key):
    dev = accounts.add(private_key)
    print(network.show_active())
    publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False
    SimpleCollectible.deploy({"from": dev}, publish_source=publish_source)

def main(): 
    deploy_simple('6bef675126d091db783b13ebe9a115a39181e7203ec4acb5744767608b61776c')