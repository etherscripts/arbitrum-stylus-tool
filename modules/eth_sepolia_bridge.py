# Coded by: https://t.me/CryptoResearchLab
from web3 import Web3
import eth_gas
import config
import random
import utils


def deposit_eth_to_arb_sepolia(private_key):
    try:
        w3_eth_sepolia = Web3(Web3.HTTPProvider(config.eth_sepolia_rpc))

        account = w3_eth_sepolia.eth.account.from_key(private_key)
        nonce = w3_eth_sepolia.eth.get_transaction_count(account.address)
        balance = w3_eth_sepolia.eth.get_balance(account.address)
        balance_ether = Web3.from_wei(balance, "ether")

        print(f" | Текущий аккаунт: {account.address} | Баланс: {balance_ether} ETH | Nonce: {nonce} | ")

        random_percent = random.uniform(config.eth_sum_transfer_percent_min, config.eth_sum_transfer_percent_max)

        bridge_amount_ether = (float(random_percent) / 100) * float(balance_ether)
        bridge_amount_wei = Web3.to_wei(float(bridge_amount_ether), "ether")

        print(f" | Рандомный процент перевода: {random_percent}% | Сумма перевода: {bridge_amount_ether} ETH | ")

        eth_sepolia_bridge_contract = w3_eth_sepolia.eth.contract(address=config.sepolia_eth_bridge_address,
                                                                  abi=config.sepolia_eth_bridge_abi)

        transaction = eth_sepolia_bridge_contract.functions.depositEth(bridge_amount_wei).build_transaction(
            {
                "from": account.address,
                "nonce": nonce,
                "value": bridge_amount_wei
            }
        )

        tx = eth_gas.fetch_prices("ETH-Sepolia", tx_details=transaction)

        signed_tx = w3_eth_sepolia.eth.account.sign_transaction(tx, private_key=private_key)
        tx_hash = w3_eth_sepolia.eth.send_raw_transaction(signed_tx.rawTransaction)

        gas_fee_gwei = Web3.from_wei(tx['maxFeePerGas'], 'gwei')

        print(f" | Пытаюсь отправить транзакцию |  Газ: {gas_fee_gwei} GWEI |")

        tx_receipt = w3_eth_sepolia.eth.wait_for_transaction_receipt(tx_hash, timeout=config.max_tx_wait_time)

        if tx_receipt.status == 1:
            print(f" | Транзакция отправлена успешно (https://sepolia.etherscan.io/tx/{Web3.to_hex(tx_hash)}) |")
        else:
            print(" ! Возникла ошибка отправки транзакции !")

        random_sleep_time = random.randint(config.sleep_from, config.sleep_to)
        print(f" | Ожидание следующего действия: {random_sleep_time:.2f} секунд | ")
        utils.countdown_timer(random_sleep_time)

    except Exception as error:
        print(f" ! Возникла ошибка: {str(error)} !")