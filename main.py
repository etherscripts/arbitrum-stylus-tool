# Coded by: https://t.me/CryptoResearchLab
import config
from modules import eth_sepolia_bridge, arb_sepolia_bridge, stylus_omnibase
from pyfiglet import Figlet


def start_eth_sepolia_bridge():
    try:
        with open(config.private_keys_file, 'r') as wallets_file:
            private_keys = wallets_file.readlines()
            private_keys_count = len(private_keys)
            print(f" | Загружено {private_keys_count} приватных ключей | ")

            for wallet_index, wallet_private_key in enumerate(private_keys):
                private_key = wallet_private_key.strip()
                eth_sepolia_bridge.deposit_eth_to_arb_sepolia(private_key)

            if wallet_index == private_keys_count - 1:
                print(" | Работа успешно завершена | ")
    except FileNotFoundError:
        print(f"! Возникла ошибка: Файл не найден {config.private_keys_file} !")
    except Exception as error:
        print(f"! Возникла ошибка: {str(error)} !")


def start_arb_sepolia_bridge():
    try:
        with open(config.private_keys_file, 'r') as wallets_file:
            private_keys = wallets_file.readlines()
            private_keys_count = len(private_keys)
            print(f" | Загружено {private_keys_count} приватных ключей | ")

            for wallet_index, wallet_private_key in enumerate(private_keys):
                private_key = wallet_private_key.strip()
                arb_sepolia_bridge.deposit_eth_to_arb_stylus(private_key)

            if wallet_index == private_keys_count - 1:
                print(" | Работа успешно завершена | ")
    except FileNotFoundError:
        print(f"! Возникла ошибка: Файл не найден {config.private_keys_file} !")
    except Exception as error:
        print(f"! Возникла ошибка: {str(error)} !")


def start_arb_stylus_nft_mint():
    try:
        with open(config.private_keys_file, 'r') as wallets_file:
            private_keys = wallets_file.readlines()
            private_keys_count = len(private_keys)
            print(f" | Загружено {private_keys_count} приватных ключей | ")

            for wallet_index, wallet_private_key in enumerate(private_keys):
                private_key = wallet_private_key.strip()
                stylus_omnibase.mint_nft(private_key)

            if wallet_index == private_keys_count - 1:
                print(" | Работа успешно завершена | ")
    except FileNotFoundError:
        print(f"! Возникла ошибка: Файл не найден {config.private_keys_file} !")
    except Exception as error:
        print(f"! Возникла ошибка: {str(error)} !")


if __name__ == "__main__":

    f = Figlet(font='slant')
    print(f.renderText(' Stylus Tool'))
    print(" |  - Coded by: t.me/CryptoResearchLab\n")

    print(" | 1. Перевести средства из ETH Sepolia в Sepolia Arbitrum.\n"
          " | 2. Перевести средства из Sepolia Arbitrum в Stylus Arbitrum.\n"
          " | 3. Минт NFT Omnibase")

    user_action = int(input(" | -  Пожалуйста выберите действие: "))
    if user_action == int(1):
        start_eth_sepolia_bridge()
    elif user_action == int(2):
        start_arb_sepolia_bridge()
    elif user_action == int(3):
        start_arb_stylus_nft_mint()
    else:
        print(" ! Ошибка выбора действия ! ")
