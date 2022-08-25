from brownie import MyVRF, network, accounts, config
from scripts.helpful_scripts import get_acc, get_contract, fund_with_link
import time


def deploy_myVRF():
    acc = get_acc()
    contract = MyVRF.deploy(
        get_contract("vrf-coordinator-v2").address,
        get_contract("link-token").address,
        config["networks"][network.show_active()]["key_hash"],
        {"from": acc},
        # publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Lottery Deployed!!")
    return contract


def create_subscription():
    # acc = get_acc()
    contract = MyVRF[-1]
    # contract.createNewSubscription({"from": acc})
    print(f"Subscription created with ID: {contract.s_subscriptionId()}")


def cancel_subscription():
    acc = get_acc()
    contract = MyVRF[-1]
    contract.cancelSubscription(acc.address, {"from": acc})
    print("Subscription Succesfully cancelled! PLease check!")


def menu():
    print("[1] to Deploy")
    print("[2] to Create Subscription")
    print("[3] to Cancel Subscription")
    print("[0] to Exit")


def main():
    while True:
        menu()
        option = int(input("Enter your choice: "))
        if option == 1:
            deploy_myVRF()
        elif option == 2:
            create_subscription()
        elif option == 3:
            cancel_subscription()
        elif option == 0:
            break
