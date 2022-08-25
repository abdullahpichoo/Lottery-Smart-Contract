// SPDX-License-Identifier: MIT

pragma solidity >=0.4.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./MyVRF.sol";

contract LotteryV2 is Ownable {
    address payable[] public players;
    mapping(address => string) public player_names;
    uint256 internal minUSD;
    uint256 random_val;
    address payable public last_winner;
    AggregatorV3Interface public price_feed;
    enum LOTTERY_STATE {
        open,
        close,
        running
    }
    LOTTERY_STATE public state;

    constructor(address _price_feed) {
        price_feed = AggregatorV3Interface(_price_feed);
        minUSD = 50 * (10**18);
        state = LOTTERY_STATE.close;
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

    function endLottery(uint256 rand) public {
        state = LOTTERY_STATE.running;
        require(state == LOTTERY_STATE.running, "Still working!");
        require(rand > 0, "Random Number not Returned");
        updateRandomness(rand);
        uint256 winner_index = rand % players.length;
        last_winner = players[winner_index];
        last_winner.transfer(address(this).balance);
        //Lottery Reset
        players = new address payable[](0);
        state = LOTTERY_STATE.close;
    }

    // function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
    //     internal
    //     override
    // {
    //     require(state == LOTTERY_STATE.running, "Still working!");
    //     require(_randomness > 0, "Random Number not Returned");
    //     updateRandomness(_randomness);
    //     uint256 winner_index = _randomness % players.length;
    //     last_winner = players[winner_index];
    //     last_winner.transfer(address(this).balance);
    //     //Lottery Reset
    //     players = new address payable[](0);
    //     state = LOTTERY_STATE.close;
    // }

    function updateRandomness(uint256 _randomness) public {
        random_val = _randomness;
    }
}
