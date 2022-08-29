//SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

/// @title Charity auctions for limited edition shoes
/// @author Matteo Razzanelli

import "./parents/SafeMath.sol";
import "./parents/Governed.sol";

/**
* @title Auctioneer contract
* @dev This is the implementation of the the auctioneers.
*/

contract Auctioneer is Governed {

  // States
  mapping(address => bool) private auctioneers_;

  // Events
  event AuctioneerAdded(address indexed account);
  event AuctioneerRemoved(address indexed account);

  // Modifier
  modifier onlyAuctioneer() {
    require(isAuctioneer(msg.sender), "Only auctioneer can call");
    _;
  }

  // Set the owner as the first auctioneer
  constructor () {
    Governed._initialize(msg.sender);
    addAuctioneer(msg.sender);
  }

  // Add a new auctioneer.
  function addAuctioneer(address account) public onlyGovernor {
    auctioneers_[account] = true;
    emit AuctioneerAdded(account);
  }

  // Remove a auctioneer.
  function removeAuctioneer(address account) public onlyGovernor {
    auctioneers_[account] = false;
    emit AuctioneerRemoved(account);
  }

  // Return true if `account` is a auctioneer.
  function isAuctioneer(address account) public view returns (bool) {
    return auctioneers_[account];
  }
}

/**
* @title Auctions contract
* @dev This is the implementation of the the auctions service.
*/

contract Platform is Auctioneer {

  using SafeMath for uint;

  struct Auction {
    address payable beneficiary;
    string description;
    uint deadline;
    uint highestBid;
    address highestBidder;
    bool completed;
  }

  uint public numAuctions_ = 0;
  mapping( uint => Auction ) public auctions_;
  string public companyName_;

  mapping( uint => string) public receipts_;
  uint public numReceipts_ = 0;

  // Events
  event NewAuctionCreated(uint indexed auctionID, address indexed beneficiary, uint indexed deadline, uint startingPrice);
  event NewHighestBid(uint indexed auctionID, address indexed bidder, uint amount);
  event AuctionEnded(uint indexed auctionID, address indexed beneficiary, address indexed winner, uint amount);

  // Initialize variables
  constructor(string memory companyName) Auctioneer() {
    companyName_ = companyName;
  }

  // Create a new charity auction
  function newAuction( address payable beneficiary, string memory description, 
  uint startingPrice, uint deadline ) external {
    require(beneficiary != address(0), "Zero address entered");
    require(startingPrice >= 0, "Starting price has to be positive or null");
    require(deadline > 0, "Available time to bid has to be greather than zero");

    uint auctionID = numAuctions_++;
    // at the creation moment the highest bidder is the beneficiary itself
    auctions_[auctionID] = Auction (beneficiary, description, block.timestamp.add(deadline), startingPrice, beneficiary, false);
    emit NewAuctionCreated(auctionID, beneficiary, deadline, startingPrice);
  }

  // New offer
  function newOffer(uint auctionID) external payable {

    require(auctions_[auctionID].completed == false, "Auction has already ended!");
    require(auctions_[auctionID].highestBid < msg.value, "Your bid value is lower than the highest bid");

    auctions_[auctionID].highestBid = msg.value;
    auctions_[auctionID].highestBidder = msg.sender;
    emit NewHighestBid(auctionID, msg.sender, msg.value);
  }

  // End an auction, transfer the highest bid to beneficiary and store hash of json receipt
  function auctionEnd(uint auctionID, string memory hash) external {

    // Checks
    require(bytes(hash).length != 0, "Hash string not passed");
    // require(block.timestamp > auctions_[auctionID].deadline, "Auction has not reached its deadline yet");
    require(auctions_[auctionID].completed == false, "Auction has been already completed");

    // Transfer
    auctions_[auctionID].completed = true;
    auctions_[auctionID].beneficiary.transfer(auctions_[auctionID].highestBid);

    // Store hash
    receipts_[auctionID] = hash;
    numReceipts_++;

    emit AuctionEnded(auctionID, auctions_[auctionID].beneficiary, auctions_[auctionID].highestBidder, auctions_[auctionID].highestBid);
  }

  // We have to create our own getter
  function getAuction(uint auctionID) public view returns (Auction memory) {
    return auctions_[auctionID];
  }

}