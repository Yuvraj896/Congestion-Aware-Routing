#  Traffic Congestion Visualizer & Smart Path Planner

An interactive web app to visualize **real-time and historical traffic congestion** and compute optimized travel routes using OpenStreetMap data.   

>  Built using Streamlit, OSMnx, NetworkX, and TomTom Traffic API.
---

##  Live Demo

[🔗 Click to try the app](https://congestion-aware-routing-guzamqdy7wnttjmmywsvrt.streamlit.app
)  
*(Hosted on Streamlit Cloud)*

---

## 📌 Features

- **Search for locations** using autocomplete suggestions by Nominatim API
- **Visualize road networks** of any city or between two points.
- **Shortest path computation** using real-time or simulated congestion data.
- **Live congestion scores** using TomTom Traffic API.
- **Graph caching** to speed up loading and reduce API usage.
- **Auto-detect user location** (with privacy).
- Congestion-aware path cost visualization.

---

##  Screenshots

City Map
![App Screenshot](data/images/23_2682678_77_4137447_23_2208832_77_4393691.png)

Congestion Map
![App Screenshot](data/images/Chhindwara,%20Madhya%20Pradesh_congestion_map.png)



---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/traffic-visualizer.git
cd traffic-visualizer
pip install -r requirements.txt

### 2. Configure API Key

Create a `.env` file in the root folder and add your TomTom API key:
```env
TOMTOM_API_KEY=your_api_key_here

```markdown
### 3. Run the App

```bash
streamlit run app_streamlit.py