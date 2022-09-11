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





# Folders
The repo consists of the following folders:
- contracts
  - This folder consists of the FundMe.sol smart contract and a MockAggregator.sol file that is used in testing.
- scripts 
  - All of the python scripts including the deploy script and interaction scripts are contained in this folder.
- test
  - The scripts that are used to test the contract on Local RPC Client are contained in this folder. Theses test files make sure the contract is behaving the way its supposed to and doesn't run into any problems.
 
 # Soliidty Files 
 ### FundMe.sol
Here are the details of this contract and how it works.
The contracts has following public variables.
- ``` address payable public owner ```
  - The address that calls and deploys this contract is stored as the owner is stored as the Owner in this address variable. This is a payable address that can receive funds from other addresses.
- ``` address[] public funders ```
  - This is a list of all the address that have funded this contract.
- ``` mapping(address => uint256) public address_to_balance ```
  - This map stores the funder address and the amount of ether they have funded.
- ``` AggregatorV3Interface public price_feed ```
  - This contract uses real price feeds to return the current market value of ethereum in USD. The contract imports the ```AggregatorV3Interface.sol``` from the **Chainlink-Mix** repository and stores the conversion address in this variable. _Note that Mainnet ETH/USD price feed address will be different from the rinkeby ETH/USD price feed address_. This variable stores one of these addresses so that they can be passed as a parameter to a function.

#### Here's how this contract works:
The contructor gets a Price Feed address as a parameter and initializes the ``` address payable public owner ``` variable to the deployer of this contract.
- The ``fund`` function check for a minimum price condition and adds the funder to the ```address[] public funders``` variable and the ``withdraw`` functions withdraws the fund to the owner and initializes the funders to a new address (removing all the previous funders). There's also a Owner modifier that makes sure that only the owner can withdraw all of the funds.
- In order to get the ETH/USD Price Feeds, ``getPrice()`` is used that returns the current price of ethereum in WEI and ``ETH_to_USD_conversion(uint256 ETH)`` is used to convert that price in USD.

### MockV3Aggregator.sol
Just like the AggregatorV3Interface that is used to return real ETH/USD price feeds, this contract mocks that contract and returns a mock price feed. This is useful if we're testing our contract on a Local RPC Client and as testing on local networks is much faster, this contract comes quite handy when we're running multiple tests.

# Python Files
I have used python to deploy this contract using **Brownie**, a very powerful framework and it makes interacting with the contract a lot simpler.
### deploy.py
This python script deploys the contract on a chain. The brownie command that we use determines the chain it deploys this contract on. For example, using the ``brownie run ./scripts/deploy.py`` deploys this contract on the default chain which is set to a local rpc client by default. We can deploy this contract on **Rinkeby Testnet** by specifying the network in the command i.e. ``--networks rinkeby`` ``--networks ganache-cli`` ``mainnet-fork``. _Note that the Ganache-Cli and Mainnet-Fork network has to be added manually in brownie through the command line._
The scripts also utilizes the ``brownie-config.yaml`` to get different keys that I have set. This makes the code much cleaner.

This scripts also verifies the contract when it deploys it to the Rinkeby Testnet chain. We can see the verification if we copy the address it deploys the contract to the rinkeyby etherscan.

### fund_and_withdraw.py
Deploying the contract again and again to run its functions is not very efficient. One feature of brownie is that when it deploys a contract, it saves all of its information in a JSON file. Every time we deploy the contract the list of FundMe contract gets updated. Now we can use this contract list to run our functions without deploying the contract everytime we need to run a function.
This scripts simply runs the fund and withdraw functions to interact with the fund and withdraw functions of FundMe.sol file.

### helpful_scripts.py
This is a very useful file that contains some functions which are used again and again. 
- ``getacc()`` function returns an accounts depending on what chain we're deploying our contract on. If we're using a local ganache instance it returns one of the fake ganache accounts. If we're deploying our contract on the Rinkeby Testnet, it connects to our Metamask account and returns our account address.
- ``get_priceFeed_address()`` returns price feeds depending on our choice of deploying networks. For local networks, it returns the price feed from the ``MockV3Aggregator.sol`` and for rinkeby testnet it returns the price feeds from the ``AggregatorV3Interface.sol`` file that we've imported in our contract.

## Purpose
The purpose of coding all of this is to get familiar with smart contract development and deploying them on different chains.

#### How to interact with this project?
_You need to have brownie installed in order to interact with this project._
**Following are the steps for interacting with this project:**
- Make an empty folder in VS Code and run this command in terminal ``brownie init``. This will initialize all the required folders for this project.
- Deploy the contract using this scripts ``brownie run ./scripts/deploy.py``.
- In order to fund and withdraw from this contract, you can run the fund_and_withdraw.py file using this command ``brownie run ./scripts/fund_and_withdraw.py``.
- If you want to run the test, use this command ``brownie test``. This is run the functions in your scripts contained in the test folder.

