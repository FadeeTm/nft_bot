#!/usr/bin/python3
from brownie import SimpleCollectible, accounts, network, config
from scripts.helpful_scripts import OPENSEA_FORMAT
from pathlib import Path
import os
import requests
import json

# sample_token_uri = "https://ipfs.io/ipfs/Qma3WxC2PCAaRXMk7YoKWJbABUWjN4m7cjpFvW95tCXRrC?filename=2-LAIN.json"
def create_token_uri(name, desc, img_path, attrs=[]):
    # image_uri = upload_to_ipfs(img_path)

    base_token = {}
    base_token['name'] = name
    base_token['description'] = desc
    base_token['image'] = img_path # image_uri
    base_token['attributes'] = attrs

    json_object = json.dumps(base_token, indent = 4)
    filepath = f"{name}.json"
    with open(filepath, "w") as outfile:
        outfile.write(json_object)
    token_uri = upload_to_ipfs(filepath)
    os.remove(filepath)
    return token_uri


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = (
            os.getenv("IPFS_URL")
            if os.getenv("IPFS_URL")
            else "http://localhost:5001"
        )
        response = requests.post(ipfs_url + "/api/v0/add",
                                 files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = "https://ipfs.io/ipfs/{}?filename={}".format(
            ipfs_hash, filename)
        print(image_uri)
    return image_uri


def create_collectible(token_uri, private_key):
    dev = accounts.add(private_key)
    print(network.show_active())
    simple_collectible = SimpleCollectible[len(SimpleCollectible) - 1]
    token_id = simple_collectible.tokenCounter()
    transaction = simple_collectible.createCollectible(token_uri, {"from": dev})
    transaction.wait(1)
    return OPENSEA_FORMAT.format(simple_collectible.address, token_id)


def main():
    uri = create_token_uri('ABOBA-1', 'pamagite', 'https://static-cdn.jtvnw.net/jtv_user_pictures/3d5e726c-9b73-479b-8e90-9abb39562088-profile_image-300x300.png', attrs=[])
    nft_token = create_collectible(uri, '6bef675126d091db783b13ebe9a115a39181e7203ec4acb5744767608b61776c')
    print(nft_token)
