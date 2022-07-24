var NotaryContract = artifacts.require("NotaryContract");

module.exports = function(deployer) {
  deployer.deploy(NotaryContract);
};