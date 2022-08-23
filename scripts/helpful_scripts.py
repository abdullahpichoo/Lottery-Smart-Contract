# from brownie import network, accounts, MockV3Aggregator, config
# import os
# from web3 import Web3

# DECIMALS = 8
# STARTING_PRICE = 2
# MAINNET_FORK = "mainnet-fork-dev"
# LOCAL_BLOCKCHAINS = ["development", "ganache-local"]


# def get_acc():
#     if (
#         network.show_active() in LOCAL_BLOCKCHAINS
#         or network.show_active() in MAINNET_FORK
#     ):
#         return accounts[0]
#     else:
#         return accounts.add(os.getenv("priv_key"))  # My MetaMask Account


# def get_priceFeed_address():
#     if network.show_active() in LOCAL_BLOCKCHAINS:
#         print(f"Current network: {network .show_active()}")
#         if (len(MockV3Aggregator)) <= 0:
#             print("Deploying a Mock Aggregator Contract....")
#             MockV3Aggregator.deploy(
#                 DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_acc()}
#             )
#         price_feed = MockV3Aggregator[-1].address
#     else:
#         price_feed = config["networks"][network.show_active()]["eth-usd-priceFeed"]
#     return price_feed
