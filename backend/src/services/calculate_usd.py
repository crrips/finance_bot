import requests
    
def calculate_usd(amount_uah):
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&json"
    response = requests.get(url)
    data = response.json()

    if data:
        rate = data[0]['rate']
        amount_usd = amount_uah / rate
        return amount_usd
    else:
        print("Error fetching exchange rate data.")
        return None
