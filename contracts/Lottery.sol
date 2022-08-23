// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

contract Lottery is Ownable {
    address payable[] public players;
    uint256 internal minUSD;
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

    function enter() public payable {
        require(state == LOTTERY_STATE.open, "Lottery hasn't started yet!");
        require(
            msg.value >= getEntranceFee(),
            "Please send more ETH to enter!"
        );
        players.push(payable(msg.sender));
    }

    function startLottery() public onlyOwner {
        require(state == LOTTERY_STATE.close, "Lottery already running!");
        state = LOTTERY_STATE.open;
    }

    function endLottery() public {
        require(state == LOTTERY_STATE.open, "Please start the lottery first!");
        state = LOTTERY_STATE.close;
    }
}
