import requests
import os

LOGOS_DIR = "/home/ubuntu/d2c-website/logos"
os.makedirs(LOGOS_DIR, exist_ok=True)

# Map: filename -> domain for Clearbit Logo API
clients = {
    "hsbc":            "hsbc.com",
    "barclays":        "barclays.co.uk",
    "bp":              "bp.com",
    "walmart":         "walmart.com",
    "aldi":            "aldi.co.uk",
    "microsoft":       "microsoft.com",
    "ms":              "marksandspencer.com",
    "mitchell_butlers":"mbplc.com",
    "virgin":          "virgin.com",
    "vodafone":        "vodafone.com",
    "severn_trent":    "severntrent.com",
}

for name, domain in clients.items():
    url = f"https://logo.clearbit.com/{domain}?size=200&format=png"
    out = os.path.join(LOGOS_DIR, f"{name}.png")
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            with open(out, "wb") as f:
                f.write(r.content)
            print(f"OK  {name} ({len(r.content)} bytes)")
        else:
            print(f"FAIL {name} — HTTP {r.status_code}")
    except Exception as e:
        print(f"ERR  {name} — {e}")
