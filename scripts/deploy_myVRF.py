from distutils.errors import LinkError
from brownie import MyVRF, network, accounts, config
from scripts.helpful_scripts import get_acc, get_contract, fund_with_link
import time


def deploy_myVRF():
    acc = get_acc()
    contract = MyVRF.deploy(
        get_contract("vrf-coordinator-v2").address,
        get_contract("link-token").address,
        config["networks"][network.show_active()]["key_hash-v2"],
        {"from": acc},
        # publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Lottery Deployed!!")
    return contract


def create_subscription():
    acc = get_acc()
    contract = MyVRF[-1]
    tx = contract.createNewSubscription({"from": acc})
    tx.wait(1)
    print(f"Subscription created with ID: {contract.s_subscriptionId()}")


def cancel_subscription():
    acc = get_acc()
    contract = MyVRF[-1]
    tx = contract.cancelSubscription(acc.address, {"from": acc})
    tx.wait(1)
    print("Subscription Succesfully cancelled! PLease check!")


def fund_subscription():
    acc = get_acc()
    contract = MyVRF[-1]
    link_amount = 3000000000000000000  # 3 LINK
    link_in_decimals = link_amount / (10**18)
    tx = fund_with_link(contract.address, amount=link_amount)
    tx.wait(1)
    tx = contract.topUpSubscription(link_amount)
    tx.wait(1)
    print(f"Contract Successfully funded with {link_in_decimals} LINK")


def add_consumer():
    acc = get_acc()
    contract = MyVRF[-1]
    tx = contract.addConsumer(contract.address)
    tx.wait(1)
    print("This deployment has been added as a Consumer Successsfeuly")


def get_random_number():
    acc = get_acc()
    contract = MyVRF[-1]
    tx = contract.requestRandomWords()
    tx.wait(1)
    time.sleep(60)
    print(
        f"Following random word was returned by the ChainLink Node: {contract.s_randomWords(0)}"
    )
    return contract.s_randomWords(0)


def get_random():
    deploy_myVRF()
    create_subscription()
    fund_subscription()
    add_consumer()
    rand = get_random_number()
    cancel_subscription()
    return rand


def menu():
    print("[1] to Deploy")
    print("[2] to Create Subscription")
    print("[3] to Cancel Subscription")
    print("[4] to Fund Subscription")
    print("[5] to Add Consumer")
    print("[6] to Get Random Num")
    print("[7] to Auto")
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
        elif option == 4:
            fund_subscription()
        elif option == 5:
            add_consumer()
        elif option == 6:
            get_random_number()
        elif option == 7:
            auto_random()
        elif option == 0:
            break
