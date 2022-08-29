
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
  // this returns the provider, or null if it wasn't detected
  const provider = await detectEthereumProvider();
  if (provider) {
    // Initialize your app
    startApp(provider);
  } else {
    // if something wrong also show a msg to user.
    deactivateConnection("MetaMask is not installed");
    alert('MetaMask is not installed');
  }
}

// Permit connection with MetaMask if it is installed
async function startApp(provider) {
  // If the provider returned by detectEthereumProvider is not the same as
  // window.ethereum, something is overwriting it, perhaps another wallet.
  if (provider !== window.ethereum) {
    deactivateConnection("Use a single wallet to access the page properly");
    alert('Use a single wallet to access the page properly');
  }
  else {
    activateConnection("Ethereum successfully detected!");
    console.log('Only one wallet: ok!');
  }
}

// Try to connect in response to user interaction only
function connect() {
  console.log("Connecting...");
  ethereum
    .request({ method: 'eth_requestAccounts' })
    .then(handleAccountsChanged)
    .catch((err) => {
      if (err.code === 4001) {
        console.log("The user rejected the connection request.");
      } else {
        console.error(err);
      }
    });
}

// Handle new accounts; "accounts" will always be an array, but it can be empty.
function handleAccountsChanged(accounts) {
  if (accounts.length === 0) {
    alert('Please connect to MetaMask.');
  } else if (accounts[0] !== currentAccount) {
    // Set current account
    console.log("Setting account...");
    currentAccount = accounts[0];
    deactivateConnection("Deactivating connection button.");    
    // write on json for python
    sendUserToPython(currentAccount);
  }
  else{
    // you are already conected and account is the same as before
    console.log("do nothing");
    // or there is an error
  }
}

// Make an ajax request to send param from js to python
function sendUserToPython(account){
  const dict_values = {account}
  const s = JSON.stringify(dict_values)
  console.log(s)
  window.alert(s)
  $.ajax({
    url:'/test',
    type:'POST',
    contentType: "application/json",
    data: s,
    success: function(data){
      //this gets called when server returns an OK response
      console.log('it worked!');
      activateRequest("You can now send eth requests");
      // location.reload();
    },
    error: function(){
      console.log("it didnt work");
      deactivateRequest("Access to send request removed.");
    }
  });
}

// Utility functions
function deactivateConnection(message){
  connectButton.removeEventListener('click', connect);
  connectButton.disabled = true;
  console.log(message);
}

function activateConnection(message){
  connectButton.addEventListener('click', connect);
  connectButton.disabled = false;
  console.log(message);
}

function deactivateRequest(message){
  sendRequestButton.removeEventListener('click', sendRequest);
  sendRequestButton.disabled = true;
  console.log(message);
}

function activateRequest(message){
  sendRequestButton.addEventListener('click', sendRequest);
  sendRequestButton.disabled = false;
  console.log(message);
}

function sendRequest(){
  console.log("Sending...");
}

// Remove event listener
ethereum.removeListener('accountsChanged', handleAccountsChanged);