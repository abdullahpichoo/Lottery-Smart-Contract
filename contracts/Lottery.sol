// SPDX-License-Identifier: MIT

pragma solidity >=0.4.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract Lottery is Ownable, VRFConsumerBase {
    address payable[] public players;
    mapping(address => string) public player_names;
    uint256 internal minUSD;
    uint256 public random_val;
    address payable public last_winner;
    AggregatorV3Interface public price_feed;
    enum LOTTERY_STATE {
        open,
        close,
        running
    }
    LOTTERY_STATE public state;
    uint256 fee; //Link Token fee
    bytes32 keyHash;
    event requested_randomness(bytes32 requestID);

    constructor(
        address _price_feed,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyHash
    ) VRFConsumerBase(_vrfCoordinator, _link) {
        price_feed = AggregatorV3Interface(_price_feed);
        minUSD = 50 * (10**18);
        state = LOTTERY_STATE.close;
        fee = _fee;
        keyHash = _keyHash;
    }

    function getEntranceFee() public view returns (uint256) {
        //IF entry fee = 50 and eth price is 1000
        // 50/1000 ==> this cannot be done as solidity doesn't deal in decimals
        // 50*(10**18)/1000
        uint256 price = getPrice();
        uint256 EntranceCost = (minUSD * (10**18)) / price;
        return EntranceCost;
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = price_feed.latestRoundData();
        return uint256(answer * 10**10); //18 decimals
    }

    function enter(string memory name) public payable {
        require(state == LOTTERY_STATE.open, "Lottery hasn't started yet!");
        require(msg.value > getEntranceFee(), "Please send more ETH to enter!");
        players.push(payable(msg.sender));
        player_names[msg.sender] = name;
    }

    function startLottery() public onlyOwner {
        require(state == LOTTERY_STATE.close, "Lottery already running!");
        state = LOTTERY_STATE.open;
    }

    function endLottery() public {
        state = LOTTERY_STATE.running;
        bytes32 requestID = requestRandomness(keyHash, fee); //This will return a bytes32 requestID
        emit requested_randomness(requestID);
        //This is done so that the request ID is emitted onthe blockchain node as an event that we can access
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(state == LOTTERY_STATE.running, "Still working!");
        require(_randomness > 0, "Random Number not Returned");
        updateRandomness(_randomness);
        uint256 winner_index = _randomness % players.length;
        last_winner = players[winner_index];
        last_winner.transfer(address(this).balance);
        //Lottery Reset
        players = new address payable[](0);
        state = LOTTERY_STATE.close;
    }

    function updateRandomness(uint256 _randomness) public {
        random_val = _randomness;
    }
}
