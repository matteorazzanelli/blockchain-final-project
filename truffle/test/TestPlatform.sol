// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/Platform.sol";

contract TestPlatform {

  using SafeMath for uint;

  // The address of the Platform contract to be tested
  Platform p = Platform(DeployedAddresses.Platform());
  // address governor = p.governor();
  uint public initialBalance = 1 ether; // or any other value
  uint amount = 1 gwei;
  uint deadline = 24 hours;
  address payable auctioneer = payable(address(0x2cB5ecA49f415a730410a94907373b2330D2cfBC));
  address payable beneficiary = payable(address(0x38773F6e467C15CF7D1CC8BF3D8F971a867Fa82C));

  event Balance(address indexed from, uint amount);
  event User(address user);

  ////////////////////////////////////////////////////////////////
  function testInitialVarsUsingDeployedContract() public {
    Assert.equal(p.numAuctions_(), 0, "At the beginning num of auctions must be 0.");
    Assert.equal(p.governor(), auctioneer, "Governor and auciotneer do not coincide.");
    Assert.isTrue(p.isAuctioneer(p.governor()), "Governor is not auciotneer.");
  }

  ////////////////////////////////////////////////////////////////
  function testNewContract() public {
    p.newAuction(beneficiary, "Prova", amount, deadline);
    uint num = uint(p.numAuctions_());
    Assert.equal(uint(num), uint(1), "Number of auctions should be 1");
    Assert.equal(p.getAuction(0).beneficiary,beneficiary,"Beneficiary not correct.");
    Assert.isAtMost(p.getAuction(0).deadline, block.timestamp.add(deadline), "Deadline not correct.");
  }

  ////////////////////////////////////////////////////////////////
  function testNewOffer() public {
    uint to_offer = 2 gwei;
    p.newOffer{value: to_offer}(0);
    Assert.equal(p.getAuction(0).highestBid, to_offer, "Highest bid not correct.");
    Assert.equal(p.getAuction(0).highestBidder, address(this), "Highest bidder not correct.");
    emit User(address(this));
    emit User(p.governor());
    emit User(p.getAuction(0).highestBidder);
  }

  ////////////////////////////////////////////////////////////////
  function testAuctionEnd() public {
    emit Balance(address(this), address(this).balance);
    emit Balance(beneficiary, beneficiary.balance);
    uint amount_for_now = beneficiary.balance;
    p.auctionEnd(0,"0x000000000");
    emit Balance(address(this), address(this).balance);
    emit Balance(beneficiary, beneficiary.balance);

    Assert.isTrue(p.getAuction(0).completed, "Auction not completed.");
    Assert.equal(p.numReceipts_(), uint(1), "Wrong number of receipts.");
    Assert.equal(p.receipts_(0), "0x000000000", "Wrong hash");
    Assert.equal(beneficiary.balance, uint(amount_for_now + 2 gwei), "Wrong balance.");
  }

}