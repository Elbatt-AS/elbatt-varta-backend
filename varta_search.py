from playwright.sync_api import sync_playwright

def run_search(search_term: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # False for å se nettleseren
        page = browser.new_page()
        page.goto("https://www.varta-automotive.com/nb-no/batterisok")

        # Fyll inn søkefeltet (legg merke til at ID/selector kan endre seg, tilpass om nødvendig)
        page.fill('input[type="search"]', search_term)

        # Klikk på søkeknappen (kan være knapp med bestemt tekst eller ikon)
        page.click('button[type="submit"]')

        # Vent til resultatene kommer
        page.wait_for_selector(".product-listing, .result-item", timeout=10000)

        # Hent alle resultater (tilpass selector etter side)
        results = page.query_selector_all(".product-listing .product, .result-item")

        # Hvis side ikke har disse klassene, kan du inspisere og justere selectors

        for i, result in enumerate(results, start=1):
            text = result.inner_text()
            print(f"Resultat {i}:\n{text}\n{'-'*40}")

        browser.close()

if __name__ == "__main__":
    søkeord = "BMW"
    run_search(søkeord)

