import requests 
import json
url_Moedas = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"

cotacoes = requests.get(url_Moedas).json()
with open('cotacoes_moedas.json', 'w') as file:
    json.dump(cotacoes, file)

url_Dias = "https://economia.awesomeapi.com.br/json/daily/USD-BRL/15"

cotacoes = requests.get(url_Dias).json()
with open('cotacoes_dias.json', 'w') as file:
    json.dump(cotacoes, file)
