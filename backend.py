from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import requests
from config import API_TOKEN

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Bytt til ditt domene i produksjon
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join("static", "index.html"))

@app.get("/api/search")
def search_product(plate: str = Query(..., min_length=3)):
    # For demo: Vi søker direkte i Elbatt API med platenummer som søketekst
    url = f"https://api.elbatt.no/products?search={plate}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Accept": "application/json"
    }
    resp = requests.get(url, headers=headers)
    if resp.ok:
        data = resp.json()
        produkter = data.get("products", [])
        return {"count": len(produkter), "products": produkter}
    else:
        return {"error": f"API call failed: {resp.status_code}"}

