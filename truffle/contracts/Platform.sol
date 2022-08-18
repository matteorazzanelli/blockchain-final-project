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

contract Auctions is Auctioneer {

  using SafeMath for uint;

  struct Auction {
    address payable beneficiary;
    string description;
    uint deadline;
    mapping( address => uint ) offers;
    uint numOffers;
    uint highestBid;
    address highestBidder;
    bool completed;
  }

  uint public numAuctions_ = 0;
  mapping( uint => Auction ) public auctions_;
  string public companyName_;

  mapping( uint => string) public receipts;
  uint public numReceipts;

  // Events
  event NewAuctionCreated(uint indexed auctionID, address beneficiary, uint indexed deadline, uint indexed startingPrice);
  event NewHighestBid(uint indexed auctionID, address indexed bidder, uint indexed amount);
  event AuctionFailed(uint indexed auctionID, address indexed winner, uint indexed amount, address beneficiary);

  // Initialize variables
  constructor(string memory companyName) Auctioneer() {
    companyName_ = companyName;
  }

  // Create a new charity auction
  function newAuction( address payable beneficiary, string memory description, uint startingPrice, uint deadline ) external onlyAuctioneer {
    require(beneficiary != address(0), "Zero address entered");
    require(startingPrice >= 0, "Starting price has to be positive or null");
    require(deadline > 0, "Available time to bid has to be greather than zero");

    uint auctionID = numAuctions_++;
    auctions_[auctionID] = Auction ({
      beneficiary: beneficiary,
      description: description, 
      deadline : block.timestamp.add(deadline), 
      numOffers: 0,
      highestBid: startingPrice,
      completed: false
    });
    emit NewAuctionCreated(auctionID, beneficiary, deadline, startingPrice);
  }

  // New offer
  function newOffer(uint auctionID) external payable {

    require(auctions_[auctionID].completed == false, "Auction has already ended!");
    // require(msg.value > auctions[auctionID].highestBid, "Your bid value is lower than the highest bid");
    require(a.deadline > 0, "AuctionID is not correct!");

    // Increase sender already offer
    auctions[auctionID].offers[msg.sender] = auctions[auctionID].offers[msg.sender].add(msg.value);
    auctions[auctionID].numOffers++;

    if(auctions[auctionID].highestBid < msg.value){
      auctions[auctionID].highestBid = msg.value;
      auctions[auctionID].highestBidder = msg.sender;
      emit HighestBidIncreased(auctionID, msg.sender, msg.value);
    }
    else{
      payable(address(msg.sender)).transfer(msg.value);
    }
  }

    

  /**
    * @dev End an auction, transfer the highest bid to beneficiary and store hash of json receipt, only auctioneers
    * @param auctionID ID associated with the auction
    * @param hash string of json auction receipt
    */
  function auctionEnd(uint auctionID, string memory hash) external onlyAuctioneer{

      // Checks
      Auction storage a = auctions[auctionID];
      require(a.deadline > 0, "AuctionID is not correct!");
      require(bytes(hash).length != 0, "Hash string not passed");
      require(block.timestamp > a.deadline, "Auction has not reached its deadline yet");
      require(a.completed == false, "Auction has been already completed");


      // Effects
      a.completed = true;
      uint amount = a.highestBid;
      a.highestBid = 0;

      // Interaction
      a.beneficiary.transfer(amount);

      // Store hash
      receipts[auctionID] = hash;
      numReceipts++;

      emit AuctionEnded(auctionID, a.highestBidder, amount, a.beneficiary);
  }

    // We have to create our own getter
  function getTitleDeed(uint auctionID) public view returns (Auction memory) {
    return acts_[auctionID];
  }

}