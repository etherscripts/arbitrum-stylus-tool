# Coded by: https://t.me/CryptoResearchLab
from web3 import Web3
import config
import time

rpc_endpoints = {
    "ETH-Sepolia": {
        "rpc": ["https://endpoints.omniatech.io/v1/eth/sepolia/public"]
    },
    "ARB-Sepolia": {
        "rpc": ["https://sepolia-rollup.arbitrum.io/rpc"]
    },
    "ARB-Stylus": {
        "rpc": ["https://stylus-testnet.arbitrum.io/rpc"]
    }
}


def fetch_prices(chain, tx_details=None, retries=config.max_gas_check_retries):
    if tx_details is None:
        tx_details = {}

    rpc_endpoints_chain = rpc_endpoints.get(chain, {}).get("rpc", [])

    for rpc_endpoint in rpc_endpoints_chain:
        for _ in range(retries):
            try:
                web3 = Web3(Web3.HTTPProvider(rpc_endpoint))
                gas_price = web3.eth.generate_gas_price()

                if gas_price is None:
                    gas_price = web3.eth.gas_price
                max_fee_per_gas = gas_price

                num_blocks = 5
                latest_block = web3.eth.block_number
                start_block = max(0, latest_block - num_blocks)

                total_priority_fees = 0
                total_txs = 0

                for block_number in range(start_block, latest_block + 1):
                    for _ in range(retries):
                        try:
                            block = web3.eth.get_block(block_number, full_transactions=True)
                            break
                        except Exception as e:
                            if 'block not found' in str(e).lower():
                                time.sleep(10)
                    else:
                        continue

                    for tx in block['transactions']:
                        total_priority_fees += tx['gasPrice']
                        total_txs += 1

                if total_txs == 0:
                    raise Exception(f" ! Возникла ошибка: Транзакций в последних {num_blocks} не найдено ! ")

                average_priority_fee = total_priority_fees // total_txs
                max_priority_fee_per_gas = min(average_priority_fee, max_fee_per_gas)

                tx_details['maxFeePerGas'] = max_fee_per_gas
                tx_details['maxPriorityFeePerGas'] = max_priority_fee_per_gas

                return tx_details

            except ConnectionError as error:
                print(f" | Ошибка подключения к RPC ({rpc_endpoint}: {str(error)}) | ")
                continue
