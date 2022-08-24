from brownie import Lottery, network, accounts, config
from scripts.helpful_scripts import get_acc, get_contract, fund_with_link
import time


def deploy():
    acc = get_acc()
    contract = Lottery.deploy(
        get_contract("eth-usd-priceFeed").address,
        get_contract("vrf-coordinator").address,
        get_contract("link-token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["key_hash"],
        {"from": acc},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Lottery Deployed!!")


def start_lottery():
    acc = get_acc()
    lottery = Lottery[-1]
    tx = lottery.startLottery({"from": acc})
    tx.wait(1)
    print("Lottery Started!")


def enter_lottery(name):
    acc = get_acc()
    lottery = Lottery[-1]
    entrance_fee = lottery.getEntranceFee() + 100000
    tx = lottery.enter(name, {"from": acc, "value": entrance_fee})
    tx.wait(1)
    print("You entered the Lottery!")


def end_lottery():
    acc = get_acc()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    tx = lottery.endLottery({"from": acc})
    tx.wait(1)
    time.sleep(60)
    winner_address = lottery.last_winner()
    print(
        f"Winner Address is: {winner_address} with Name: {lottery.player_names(winner_address)}"
    )


def main():
    deploy()
    start_lottery()
    enter_lottery("Abdullah")
    end_lottery()
