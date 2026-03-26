# IP Geolocation Viewer

A beginner-friendly Python + Flask web app that detects your IP address and compares geolocation results from **ip-api.com** and **ipinfo.io** side by side.

Built as part of the Moringa School AI-Assisted Learning Capstone.



##  Project Structure


ip-geolocation-demo/
├── app.py               # Flask backend — queries both APIs
├── templates/
│   └── index.html       # Frontend — dark-themed comparison page
├──      
└── README.md




 Setup & Run

### 1. Clone or download this repo

bash
git clone https://github.com/Hibaq434/ip-geolocation-demo.git
cd ip-geolocation-demo


### 2. Create a virtual environment

bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows


### 3. Install dependencies

bash
pip install flask requests



### 4. Add your ipinfo.io token

1. Sign up free at https://ipinfo.io/signup
2. Open `app.py` and replace:
   python
   IPINFO_TOKEN = "your_token_here"
   
   with your actual token.

### 5. Run the app

bash
python app.py
`

Open your browser at: **http://localhost:5000**



###  Expected Output

A dark-themed webpage showing two cards — one per API — each displaying:
- Country, Region, City, ZIP
- Latitude & Longitude
- Timezone, ISP, Organization



##  API Details

| API | Auth | Free Limit | HTTPS |
|-----|------|-----------|-------|
| ip-api.com | None | 45 req/min | ❌ |
| ipinfo.io | Free token | 50k/month | ✅ |


## 🐛 Common Issues

| Error | Fix |
|-------|-----|
| `private range` from ip-api | You're on localhost — app auto-fetches public IP via ipify |
| `Unauthorized` from ipinfo | Add your token to `app.py` |
| `ModuleNotFoundError` | Run `pip install flask requests` |
| Port 5000 in use (macOS) | Change to `port=5001` in `app.py` |



