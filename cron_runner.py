import subprocess
from datetime import datetime

print("\n=== Automatisk fullsynkronisering startet ===\n")

start = datetime.now()

# Trinn 1: Fang kortkoder
print("\n🚀 Kjører fange_kortkoder_og_logg.py...")
try:
    subprocess.run(["python", "fange_kortkoder_og_logg.py"], check=True)
    print("✅ fange_kortkoder_og_logg.py ferdig")
except subprocess.CalledProcessError:
    print("❌ Feil i fange_kortkoder_og_logg.py")

# Trinn 2: Push til Mystore
print("\n🚀 Kjører auto_sync_mystore.py...")
try:
    subprocess.run(["python", "auto_sync_mystore.py"], check=True)
    print("✅ auto_sync_mystore.py ferdig")
except subprocess.CalledProcessError:
    print("❌ Feil i auto_sync_mystore.py")

slutt = datetime.now()
print(f"\n=== Fullført på {slutt.strftime('%Y-%m-%d %H:%M:%S')} ===")
print(f"⏱️ Total tid: {slutt - start}")

