# Coded by: https://t.me/CryptoResearchLab
import time
from tqdm import tqdm


def countdown_timer(seconds):
    progress_bar = tqdm(total=seconds, desc=" | Ожидание", unit="s")

    for _ in range(seconds, 0, -1):
        time.sleep(1)
        progress_bar.update(1)

    progress_bar.close()

    print(" | Переходим к следующему действию | ")
