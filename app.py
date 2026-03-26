# app.py
# IP Geolocation Demo — Flask backend
# Queries ip-api.com and ipinfo.io for the visitor's IP and renders results

from flask import Flask, render_template, request
import requests

app = Flask(__name__)


IPINFO_TOKEN = "86f31f75862065"


def get_public_ip():
    """
    Detect the requester's public IP address.
    Reads X-Forwarded-For header if behind a proxy (e.g., Nginx, Heroku).
    Falls back to ipify.org for local testing.
    """
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        return response.json().get("ip", "Unknown")
    except Exception:
        return "8.8.8.8"  # Fallback to Google DNS for demo purposes


def query_ipapi(ip):
    """
    Query ip-api.com (free, no API key, HTTP only on free tier).
    Returns normalized dict with location fields.
    """
    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("status") == "success":
            return {
                "source": "ip-api.com",
                "ip": data.get("query"),
                "country": data.get("country"),
                "region": data.get("regionName"),
                "city": data.get("city"),
                "zip": data.get("zip"),
                "latitude": data.get("lat"),
                "longitude": data.get("lon"),
                "timezone": data.get("timezone"),
                "isp": data.get("isp"),
                "org": data.get("org"),
                "error": None
            }
        else:
            return {"source": "ip-api.com", "error": data.get("message", "Lookup failed")}
    except Exception as e:
        return {"source": "ip-api.com", "error": str(e)}


def query_ipinfo(ip):
    """
    Query ipinfo.io (free tier: 50k req/month, requires token).
    Returns normalized dict with location fields.
    """
    try:
        url = f"https://ipinfo.io/{ip}/json"
        headers = {"Authorization": f"Bearer {IPINFO_TOKEN}"}
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()

        # ipinfo returns lat/lng as a single "loc" string: "-1.2921,36.8219"
        loc = data.get("loc", ",").split(",")
        latitude = loc[0] if len(loc) == 2 else "N/A"
        longitude = loc[1] if len(loc) == 2 else "N/A"

        # Check for error response from API
        if "error" in data:
            return {"source": "ipinfo.io", "error": data["error"].get("message", "Unknown error")}

        return {
            "source": "ipinfo.io",
            "ip": data.get("ip"),
            "country": data.get("country"),
            "region": data.get("region"),
            "city": data.get("city"),
            "zip": data.get("postal"),
            "latitude": latitude,
            "longitude": longitude,
            "timezone": data.get("timezone"),
            "isp": data.get("org"),
            "org": data.get("org"),
            "error": None
        }
    except Exception as e:
        return {"source": "ipinfo.io", "error": str(e)}


@app.route("/")
def index():
    ip = get_public_ip()
    ipapi_result = query_ipapi(ip)
    ipinfo_result = query_ipinfo(ip)
    return render_template("index.html", ip=ip, ipapi=ipapi_result, ipinfo=ipinfo_result)


if __name__ == "__main__":
    # debug=True enables auto-reload on code change — disable in production
    app.run(debug=True, port=5000)
