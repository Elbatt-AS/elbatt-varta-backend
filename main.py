from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/sok")
async def sok_batteri(platenr: str = Query(..., min_length=1)):
    url = f"https://www.varta-automotive.com/nb-no/batterisok?plateno={platenr}&platelang=nb-NO"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail="Feil fra Varta")

    soup = BeautifulSoup(resp.text, "html.parser")

    resultater = []
    # Juster CSS-selectors under etter inspeksjon!
    for item in soup.select(".battery-result-item"):  
        navn = item.select_one(".battery-name").get_text(strip=True)
        kode = item.select_one(".battery-code").get_text(strip=True)
        resultater.append({"navn": navn, "kode": kode})

    if not resultater:
        return {"melding": "Ingen resultater funnet."}

    return {"resultater": resultater}
