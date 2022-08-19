var Platform = artifacts.require("Platform");

module.exports = function(deployer) {
  deployer.deploy(Platform, "Test_Company_name");
};