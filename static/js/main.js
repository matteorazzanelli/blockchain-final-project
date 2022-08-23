// This function detects most providers injected at window.ethereum
// import detectEthereumProvider from '@metamask/detect-provider';

// Handle button
const sendRequestButton = document.getElementById('sendRequestButton');
const connectButton = document.getElementById('connectButton', connect);
connectButton.addEventListener('click', connect);

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
  // this returns the provider, or null if it wasn't detected
  const provider = await detectEthereumProvider();
  if (provider) {
    console.log('Ethereum successfully detected!')
    startApp(provider);  // Initialize your app
  } else {
    console.error('MetaMask is not installed');
    connectButton.innerText = 'Metamask is not available';
    connectButton.disabled = true;
  }
}

// Permit connection with MetaMask if it is installed
async function startApp(provider) {
  // If the provider returned by detectEthereumProvider is not the same as
  // window.ethereum, something is overwriting it, perhaps another wallet.
  if (provider !== window.ethereum) {
    console.error('Do you have multiple wallets installed?');
    connectButton.innerText = 'Metamask is not available';
    connectButton.disabled = true;
    alert('Use a single wallet to access the page properly');
  }
  else 
    console.log('Only one wallet: ok!');
}

// You should only attempt to request the user's accounts in response to user interaction
function connect() {
  console.log("Connecting...");
  ethereum
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
}

function handleAccountsChanged(accounts) {
  if (accounts.length === 0) {
    console.log('Please connect to MetaMask.');
    alert('Please connect to MetaMask.');
    location.reload();
  } else {
    // Set current account
    console.log("Setting account...");
    currentAccount = accounts[0];
    console.log(currentAccount);
    sendRequestButton.disabled = false;
    // write on json for python
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

// Remove event listener
ethereum.removeListener('accountsChanged', handleAccountsChanged);