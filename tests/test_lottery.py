from brownie import Lottery, accounts, network, config
from web3 import Web3

# 0.0319


def test_getEntraceFee():
    acc = accounts[0]
    contract = Lottery.deploy(
        config["networks"][network.show_active()]["eth-usd-priceFeed"], {"from": acc}
    )
    assert contract.getEntranceFee() > Web3.toWei(0.0315, "ether")
