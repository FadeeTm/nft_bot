#!/usr/bin/python3
import os
from brownie import SimpleCollectible, accounts, network, config


def deploy_simple(private_key):
    dev = accounts.add(private_key)
    print(network.show_active())
    publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False
    SimpleCollectible.deploy({"from": dev}, publish_source=publish_source)
