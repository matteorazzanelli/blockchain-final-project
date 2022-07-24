var HDWalletProvider = require("truffle-hdwallet-provider");
const fs = require('fs');
const mnemonic = fs.readFileSync("../.secret").toString().trim();

module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 7545,
      network_id: "*"
    },
    ropsten: {
      provider: function() {
        return new HDWalletProvider(mnemonic, "https://ropsten.infura.io/v3/7340ba294b4f4b1da1ffdd1d23ef3022")
      },
      network_id: 3, // official id of the ropsten network
      gas: 4000000      //make sure this gas allocation isn't over 4M, which is the max
    }
  },

  contracts_directory: './contracts/',
  contracts_build_directory: './build/',

	// Configure your compilers
  compilers: {
    solc: {
      optimizer: { enabled: true, runs: 200 },
      version: "0.8.0", // A version or constraint - Ex. "^0.5.0"
    }
  }
};
