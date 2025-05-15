import pandas as pd
from playwright.sync_api import sync_playwright
import time

INPUT_CSV = "varta_searchwords.csv"   # Fil med søkeord, kolonne 'searchword'
OUTPUT_EXCEL = "varta_search_results.xlsx"

def run_search(search_term: str, page):
    # Gå til siden (reset før hvert søk for å unngå problemer)
    page.goto("https://www.varta-automotive.com/nb-no/batterisok")

    # Fyll inn søkefeltet
    page.fill('input[type="search"]', search_term)

    # Klikk på søk
    page.click('button[type="submit"]')

    # Vent til resultatene vises (tilpass selector!)
    try:
        page.wait_for_selector(".product-listing, .result-item", timeout=10000)
    except Exception as e:
        print(f"Ingen resultater funnet for '{search_term}' eller timeout.")
        return []

    # Hent alle resultat-elementer
    results = page.query_selector_all(".product-listing .product, .result-item")

    extracted = []
    for result in results:
        text = result.inner_text().strip()
        extracted.append(text)

    return extracted

def main():
    df = pd.read_csv(INPUT_CSV)
    if 'searchword' not in df.columns:
        print("CSV-filen må ha en kolonne som heter 'searchword'")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        all_results = []

        for idx, row in df.iterrows():
            term = str(row['searchword']).strip()
            if not term:
                continue
            print(f"Søker etter: {term}")
            results = run_search(term, page)

            if results:
                for res_text in results:
                    all_results.append({"searchword": term, "result": res_text})
            else:
                # Legg inn tomt resultat for å indikere ingen treff
                all_results.append({"searchword": term, "result": ""})

            # Vent et lite øyeblikk for ikke å stresse serveren
            time.sleep(1)

        browser.close()

    # Lag DataFrame og skriv til Excel
    df_results = pd.DataFrame(all_results)
    df_results.to_excel(OUTPUT_EXCEL, index=False)
    print(f"Ferdig! Resultater lagret i {OUTPUT_EXCEL}")

if __name__ == "__main__":
    main()

