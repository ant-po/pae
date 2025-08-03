from binance.client import Client
from utils.config import BINANCE_API_KEY, BINANCE_API_SECRET

def get_binance_client():
    return Client(BINANCE_API_KEY, BINANCE_API_SECRET)