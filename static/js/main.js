// This function detects most providers injected at window.ethereum
import detectEthereumProvider from '@metamask/detect-provider';

// Handle button
const sendRequestButton = document.getElementById('sendRequestButton');
const connectButton = document.getElementById('connectButton');

// Handle events
ethereum.on('accountsChanged', handleAccountsChanged);

// current acount to save
let currentAccount = null;

// On loaded document
window.addEventListener('DOMContentLoaded', () => {
  init();
});

// Check for a provider
async function init() {
  const provider = await detectEthereumProvider();
  if (provider) {
    console.log('Ethereum successfully detected!')
    startApp(provider);
  } else {
  // Warn
  console.error('MetaMask is not installed');
  connectButton.innerText = 'Metamask is not available';
  connectButton.style.backgroundColor = "grey";
  connectButton.style.color = 'black';
  connectButton.style.border = '1px solid black'
  connectButton.style.cursor = "not-allowed";
  alert('Please install MetaMask to access the page properly');
  }
}

// Permit connection with MetaMask if it is installed
async function startApp(provider) {
  if (provider !== window.ethereum) {
    console.error('Do you have multiple wallets installed?');
    connectButton.innerText = 'Metamask is not available';
    connectButton.style.backgroundColor = "grey";
    connectButton.style.color = 'black';
    connectButton.style.border = '1px solid black'
    connectButton.style.cursor = "not-allowed";
    alert('Use a single wallet to access the page properly');
  }
  // if ok, do a request
  else
    await ethereum
      .request({ method: 'eth_requestAccounts' })
      .then(handleAccountsChanged)
      .catch((err) => {
        if (err.code === 4001) {
          // EIP-1193 userRejectedRequest error
          // If this happens, the user rejected the connection request.
          console.log('Please connect to MetaMask.');
        } else {
          console.error(err);
        }
      });

    // In case we need to handle the smart contract directly here in js...
    // try {
    //   // Initialize web3
    //   web3 = new Web3(window.ethereum);
    //   web3.eth.defaultAccount = currentAccount;
    //   web3.eth.Contract.transactionPollingTimeout = 60*5;
  
    //   // Reference to the smart contract
    //   contract = new web3.eth.Contract(abi, contractAddress);
    //   contract.transactionPollingTimeout = 60*5;
    // }
    // catch (error) {
    //   console.error(error);
    // }
}

function handleAccountsChanged(accounts) {
  if (accounts.length === 0) {
    console.log('Please connect to MetaMask.');
    alert('Please connect to MetaMask.');
    location.reload();
  } else {
    // Set current account
    currentAccount = accounts[0];
    console.log(currentAccount);
    sendRequestButton.disabled = false;
    // write on json
    const dict_values = {currentAccount};
    const s = JSON.stringify(dict_values);
    console.log(s);
    window.alert(s);
    $.ajax({
      url:"/test",
      type:"POST",
      contentType: "application/json",
      data: JSON.stringify(s)
    });
    location.reload();
  }
}

/**********************************************************/
/* Handle chain (network) and chainChanged (per EIP-1193) */
/**********************************************************/

const chainId = await ethereum.request({ method: 'eth_chainId' });
handleChainChanged(chainId);

ethereum.on('chainChanged', handleChainChanged);

function handleChainChanged(_chainId) {
  // We recommend reloading the page, unless you must do otherwise
  window.location.reload();
}