# Smart Contract Lottery using Solidity and Python
 A solidity contract where users can participate in a lottery and a random winner is selected.

# How it Works
Here's a brief explanation on how this contract works:
- Users can participate in the Lottery by paying a Entrance Fee to the contract.
- The Contract keeps track of all the funds received as Entrance Fee from different users.
- A random number is requested from the Chainlink VRF Node and a winner is selected at random.
- All the funds in the contract are transfered to the winner's account and the lottery is concluded.
 
 This project is compiled and deployed using python. A python frameworks based on web3.py called **Brownie** is used to deploy and test this contract.
 The contract is deployed to different networks to test its working. The networks I used include
 - Local Ganache Instance
 - Goerli Testnet
 - Mainnet Fork

## Randomness
Since blockchains are deterministic we cannot really get a random number in solidity. Even if there was a ``call_random`` function, each node in the blockchain would return a different random number and no one node can agree on one random number. 
A bad practise would be to use the global variables of the blockchain for example ``Block Difficulty``, ``Nonce`` etc and hash them using a hashing algorithm such as keccak256. This makes our contract very vulnerable to attacks as the hashing algorithm is going to be the same everytime and all the randomness wouldn't really be random.
This is where the Chainlink VRF comes into play. Chainlink VRF is a way to receive random numbers in your smart contracts. A detailed explanation on how chainlink VRF works is given on the Chainlink Documentation here: https://docs.chain.link/docs/vrf/v2/introduction/

A detailed explanation on how I've implemented the Chainlink VRF version 2.0 and how I receive random numbers in my solidity contract is given in my following repo:
https://github.com/abdullahpichoo/Custom-ChainlinkVRFv2-Randomness-Contract

