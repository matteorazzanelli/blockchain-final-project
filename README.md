<div id="top"></div>
<br />
<div align="center">
  <a href="">
    <img src="startup_token/logo_solidity.png" alt="Logo" width="80" height="80">
  </a>

  <h1 align="center">Notary contract Platform</h1>
  <p align="center">
      Develop a platform that leverages on an ERC20 token that allows to read and update smart contracts created on the platform itself and to save emitted events on a No-SQL database.
  </p>
</div>

### Tools

* [Solidity](https://docs.soliditylang.org/en/v0.8.11/)
* [Truffle](https://trufflesuite.com/truffle/)
* [Ganache](https://trufflesuite.com/ganache/)
* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [MongoDB](https://www.mongodb.com/)
* [Redis](https://redis.io/)
* [Web3.py](https://web3py.readthedocs.io/en/stable/)

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
  sudo service redis-server start
  ```
5. Create a .env file in your workspace and set your private key (for deploying and retrieving contract)
  ```sh
  PRIVATE_KEY_GANACHE=<YOUR-PRIVATE-KEY>
  ```
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
7. Copy the resulting smart contract address and copy and paste it in the views.py file (line 25)
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