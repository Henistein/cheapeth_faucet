// SPDX-License-Identifier: MIT
pragma solidity ^0.7.1;

contract faucet{
  uint public _amount = 50000000000000000;
  address payable public owner = 0xDf1B72FC1bA5a77DD6c038DC2bc70746fFCA5caA;

  constructor() payable{}

  function sendEther(address payable _to) public payable{
    // Check if the faucet has enough ether
    require(address(this).balance >= _amount);
    // Send the ether
    _to.transfer(_amount);
  }

  // function to withdraw all the balance from the faucet to the owner
  // so if something need to be change, there is some way to get the balance
  function withdrawAll() public payable{
    require(msg.sender == owner, "Just the owner can call this function!");
    owner.transfer(address(this).balance);
  }

  //function to donate funds to the faucet contract
  receive() external payable {}
}
