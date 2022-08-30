<div id="top"></div>
<br />
<div align="center">
  <a href="">
    <img src="logo_solidity.png" alt="Logo" width="80" height="80">
  </a>

  <h1 align="center">Demo auctions platform</h1>
  <p align="center">
    This demo platform allows users to make a bid on one or more not completed auctions on limited edition eco-shoes.
    The bets are handled by using a no-relational databse (i.e. Redis).
    When an auction ends, the results are stored in:
  </p>
  </div>
  <p align="left">
    <ul>
      <li>a relational database (i.e. sqlite)</li>
      <li>in a JSON</li>
      <li>on the Ethereum blockchain (Ganache)</li>
    </ul>
  </p>

### Languages
* [Solidity](https://docs.soliditylang.org/en/v0.8.11/)
* [Python](https://www.python.org/)
* [Javascript](https://www.javascript.com/)

### Frameworks/IDE
* [Truffle](https://trufflesuite.com/truffle/)
* [Django](https://www.djangoproject.com/)

### Databases
* [SQLite](https://www.sqlite.org/index.html)
* [Redis](https://redis.io/)

### Tools
* [Ganache](https://trufflesuite.com/ganache/)
* [MetaMask](https://metamask.io/)

### Important libs
* [Web3.py](https://web3py.readthedocs.io/en/stable/)
* [Web3.js](https://web3js.readthedocs.io/en/v1.7.5/)

## Getting Started
1. Clone the repo
  ```sh
  git clone https://github.com/matteorazzanelli/ethereum-project.git
  ```
2. Install external packages using requirements.txt file
  ```sh
  pip install -r /path/to/requirements.txt
  ```
3. Open Ganache and instantiate a workspace
4. In case you are on Windows, follow [these](https://redis.io/docs/getting-started/installation/install-redis-on-windows/) instructions, then open a shell and run redis server
  ```sh
  sudo service redis-server restart
  ```
5. Install [MetaMask](https://metamask.io/) as a Chrome extension
6. Open a shell and go to your smart contract folder (deploy the contract on your local blockchain, see truffle-config.js for details)
  ```sh
  truffle compile
  ```
  ```sh
  truffle test
  ```
  ```sh
  truffle deploy --network development
  ```
7. Copy the resulting smart contract address and copy and paste it in the views.py file (line 21)
8. Open a shell and run the website (go where the manage.py file is)
  ```sh
  python manage.py makemigrations
  ```
  ```sh
  python manage.py migrate
  ```
  ```sh
  python manage.py runserver
  ```
8. Go to http://127.0.0.1:8000/