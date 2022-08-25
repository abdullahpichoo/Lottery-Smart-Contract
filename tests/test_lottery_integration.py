from brownie import Lottery, accounts, network, config, exceptions
from web3 import Web3
from scripts.deploy import deploy
from scripts.helpful_scripts import (
    get_acc,
    fund_with_link,
    get_contract,
    LOCAL_BLOCKCHAINS,
)
import pytest, random, time


def test_can_choose_winner():
    if network.show_active() in LOCAL_BLOCKCHAINS:
        pytest.skip("This test is only for Testnets")
    lottery = deploy()
    acc = get_acc()
    lottery.startLottery({"from": acc})
    player_names = ["Abdullah", "Saif", "Junaid"]
    for i in range(len(player_names)):
        lottery.enter(
            player_names[i],
            {"from": get_acc(), "value": lottery.getEntranceFee() + 10000},
        )
    fund_with_link(lottery)
    lottery.endLottery({"from": acc})
    time.sleep(60)
    rand = lottery.random_val()
    winner_acc = get_acc(index=rand % len(player_names))
    assert lottery.last_winner() == winner_acc
    assert lottery.balance() == 0
