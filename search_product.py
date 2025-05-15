import requests
from config import API_TOKEN

def search_product(product_number):
    url = f"https://api.elbatt.no/products?search={product_number}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        data = response.json()
        return data.get("products", [])
    else:
        print(f"API-feil: {response.status_code} - {response.text}")
        return []

if __name__ == "__main__":
    produktnummer = input("Skriv inn produktnummer for søk: ").strip()
    produkter = search_product(produktnummer)
    if produkter:
        print(f"Fant {len(produkter)} produkt(er):")
        for p in produkter:
            print(f"- {p.get('name')} | Pris: {p.get('price')} kr | URL: {p.get('url')}")
    else:
        print("Ingen produkter funnet.")

