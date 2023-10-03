# Coded by: https://t.me/CryptoResearchLab
from web3 import Web3
import eth_gas
import config
import random
import utils


def mint_nft(private_key):
    try:
        w3_arb_stylus = Web3(Web3.HTTPProvider(config.arb_stylus_rpc))

        account = w3_arb_stylus.eth.account.from_key(private_key)
        nonce = w3_arb_stylus.eth.get_transaction_count(account.address)
        balance = w3_arb_stylus.eth.get_balance(account.address)
        balance_ether = Web3.from_wei(balance, "ether")

        print(f" | Текущий аккаунт: {account.address} | Баланс: {balance_ether} ETH | Nonce: {nonce} | ")

        omnibase_nft_contract = w3_arb_stylus.eth.contract(address=config.omnibase_nft_address,
                                                           abi=config.omnibase_nft_abi)

        fee = Web3.to_wei(0.00023, "ether")

        transaction = omnibase_nft_contract.functions.mint(1).build_transaction(
            {
                "from": account.address,
                "nonce": nonce,
                "value": fee
            }
        )

        tx = eth_gas.fetch_prices("ARB-Stylus", tx_details=transaction)

        signed_tx = w3_arb_stylus.eth.account.sign_transaction(tx, private_key=private_key)
        tx_hash = w3_arb_stylus.eth.send_raw_transaction(signed_tx.rawTransaction)

        gas_fee_gwei = Web3.from_wei(tx['maxFeePerGas'], 'gwei')

        print(f" | Пытаюсь отправить транзакцию |  Газ: {gas_fee_gwei} GWEI |")

        tx_receipt = w3_arb_stylus.eth.wait_for_transaction_receipt(tx_hash, timeout=config.max_tx_wait_time)

        if tx_receipt.status == 1:
            print(
                f" | Транзакция отправлена успешно (https://stylus-testnet-explorer.arbitrum.io/tx/{Web3.to_hex(tx_hash)}) |")
        else:
            print(" ! Возникла ошибка отправки транзакции !")

        random_sleep_time = random.randint(config.sleep_from, config.sleep_to)
        print(f" | Ожидание следующего действия: {random_sleep_time:.2f} секунд | ")
        utils.countdown_timer(random_sleep_time)

    except Exception as error:
        print(f" ! Возникла ошибка: {str(error)} !")

