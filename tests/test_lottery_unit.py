# from brownie import Lottery, accounts, network, config, exceptions
# from web3 import Web3
# from scripts.deploy import deploy
# from scripts.helpful_scripts import (
#     get_acc,
#     fund_with_link,
#     get_contract,
#     LOCAL_BLOCKCHAINS,
# )
# import pytest, random

# # 0.0319

# # Arrange
# # Act
# # Assert
# def test_getEntraceFee():
#     # Arrange
#     if network.show_active() not in LOCAL_BLOCKCHAINS:
#         pytest.skip("This test is only for Local Ganache Blockchain")
#     lottery = deploy()
#     # Act
#     expected_entry_fee = Web3.toWei(50 / 2000, "ether")
#     entry_fee = lottery.getEntranceFee()
#     # Assert
#     assert entry_fee == expected_entry_fee


# def test_enter_without_starting_lottery():
#     if network.show_active() not in LOCAL_BLOCKCHAINS:
#         pytest.skip("This test is only for Local Ganache Blockchain")
#     lottery = deploy()
#     with pytest.raises(exceptions.VirtualMachineError):
#         lottery.enter("Adullah", {"from": get_acc(), "value": lottery.getEntranceFee()})


# def test_enter_lottery_after_starting():
#     if network.show_active() not in LOCAL_BLOCKCHAINS:
#         pytest.skip("This test is only for Local Ganache Blockchain")
#     lottery = deploy()
#     acc = get_acc()
#     lottery.startLottery({"from": acc})
#     player_name = "Abdullah"
#     lottery.enter(
#         player_name, {"from": get_acc(), "value": lottery.getEntranceFee() + 10000}
#     )
#     assert lottery.players(0) == acc
#     assert lottery.player_names(acc) == player_name


# def test_can_end_lottery():
#     if network.show_active() not in LOCAL_BLOCKCHAINS:
#         pytest.skip("This test is only for Local Ganache Blockchain")
#     lottery = deploy()
#     acc = get_acc()
#     lottery.startLottery({"from": acc})
#     player_name = "Abdullah"
#     lottery.enter(
#         player_name, {"from": get_acc(), "value": lottery.getEntranceFee() + 10000}
#     )
#     fund_with_link(lottery)
#     lottery.endLottery({"from": acc})
#     assert lottery.state() == 2


# def test_only_owner_can_start_lottery():
#     if network.show_active() not in LOCAL_BLOCKCHAINS:
#         pytest.skip("This test is only for Local Ganache Blockchain")
#     lottery = deploy()
#     not_owner = accounts.add()
#     with pytest.raises(exceptions.VirtualMachineError):
#         lottery.startLottery({"from": not_owner})


# def test_can_end_lottery_and_choose_winner():
#     if network.show_active() not in LOCAL_BLOCKCHAINS:
#         pytest.skip("This test is only for Local Ganache Blockchain")
#     lottery = deploy()
#     acc = get_acc()
#     lottery.startLottery({"from": acc})
#     player_names = ["Abdullah", "Saif", "Junaid"]
#     for i in range(len(player_names)):
#         lottery.enter(
#             player_names[i],
#             {"from": get_acc(index=i), "value": lottery.getEntranceFee() + 10000},
#         )
#     fund_with_link(lottery)
#     trx = lottery.endLottery({"from": acc})
#     requestID = trx.events["requested_randomness"]["requestID"]
#     # Now that we have the requestID, we can mock the Chainlink Node as if it actually returned a random value
#     # We can use the "CallBackWithRandomness" function of the VRFCoorinator that actually returns the
#     # random number by taking requestID, ConsumerContract and a Chainlink-node-returned random value
#     # but as we are not calling any chainlink node, we'll just give a random number on our own
#     STATIC_RANDOM = random.randint(0, 500)
#     get_contract("vrf-coordinator").callBackWithRandomness(
#         requestID, STATIC_RANDOM, lottery.address, {"from": acc}
#     )
#     winner_acc = get_acc(index=STATIC_RANDOM % len(player_names))
#     initial_balance_of_winner = winner_acc.balance()
#     balance_of_lottery = lottery.balance()

#     assert lottery.last_winner() == winner_acc
#     assert lottery.balance() == 0
#     assert winner_acc.balance() == initial_balance_of_winner + balance_of_lottery


# def test_winner_gets_all_money():
#     pass
