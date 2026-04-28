# EXPO's Supply Chain Optimization (SCO)

A full-stack Supply Chain Management & Optimization web application built with **Flask** (Python) and **vanilla JavaScript**. It features a futuristic, JARVIS-inspired UI for managing suppliers, manufacturers, distributors, inventory, orders, and logistics with real-time analytics and optimization insights.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)

---

## Features

- **Dashboard**: Real-time overview with active alerts, inventory by category charts, and recent orders
- **Supplier Management**: Track vendors, contact info, reliability ratings
- **Manufacturer Management**: Monitor production facilities, capacity, and status
- **Distributor Management**: Manage distribution networks, warehouse counts, and delivery SLAs
- **Inventory Tracking**: Stock levels, reorder points, auto-replenishment suggestions
- **Order Management**: Purchase orders with priority levels and status tracking
- **Logistics Tracking**: Shipments with carrier info, tracking numbers, and transport modes
- **Optimization Engine**: Inventory replenishment candidates, stockout risk analysis, transportation cost breakdown, order fulfillment pipeline, and supplier performance scores

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3, Flask, PyMongo |
| **Database** | MongoDB |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Styling** | Custom CSS with futuristic theme |

---

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── config.py            # Configuration settings
│   │   ├── extensions.py        # Flask extensions (CORS, MongoDB)
│   │   ├── routes/              # API blueprints
│   │   │   ├── suppliers.py
│   │   │   ├── manufacturers.py
│   │   │   ├── distributors.py
│   │   │   ├── inventory.py
│   │   │   ├── orders.py
│   │   │   ├── logistics.py
│   │   │   └── dashboard.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── serializers.py   # BSON/JSON serialization helpers
│   ├── requirements.txt
│   ├── run.py                   # Entry point
│   └── seed.py                  # Database seeder
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── api.js               # API client functions
│       ├── app.js               # Main application logic
│       └── ui.js                # UI helpers & rendering
├── .env.example
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- MongoDB (local or cloud instance)
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/supply-chain-optimization.git
   cd supply-chain-optimization
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

4. **Seed the database** (optional - creates sample data)
   ```bash
   python seed.py
   ```

5. **Run the backend server**
   ```bash
   python run.py
   ```
   The API will be available at `http://localhost:5000`

6. **Serve the frontend**
   
   Open `frontend/index.html` in your browser, or use a simple HTTP server:
   ```bash
   cd frontend
   # Python 3
   python -m http.server 5500
   ```
   Then navigate to `http://localhost:5500`

---

## Deployment

### Why No Data Shows on Vercel

**Vercel only hosts the frontend (HTML/CSS/JS).** The Flask backend API and MongoDB database are NOT included. You must deploy the backend separately and connect the two.

**Architecture:**
```
[Vercel: Static Frontend]  ←──API calls──→  [Render: Flask Backend]  ←──→  [MongoDB Atlas]
```

---

### Step 1: Deploy Backend on Render (Free)

1. **Get a MongoDB Atlas database** (free tier available at [mongodb.com](https://www.mongodb.com/cloud/atlas))
   - Create a cluster → Database Access → Add user → Network Access → Allow from anywhere (`0.0.0.0/0`)
   - Copy your connection string: `mongodb+srv://user:pass@cluster.mongodb.net/supplychain`

2. **Push this repo to GitHub** (already done)

3. **Go to [Render](https://render.com)** → **New Web Service** → Connect your GitHub repo
   - **Name:** `expo-api` (or any name)
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python run.py`
   - **Plan:** Free

4. **Add Environment Variables** in Render dashboard:
   | Key | Value |
   |-----|-------|
   | `SECRET_KEY` | A random secret string |
   | `MONGO_URI` | Your MongoDB Atlas connection string |
   | `FLASK_DEBUG` | `False` |

5. **Click Create Web Service**
   - Wait for build to complete (2-3 minutes)
   - Copy your Render URL: `https://expo-api.onrender.com`
   - Visit `https://expo-api.onrender.com/` to confirm it's running

---

### Step 2: Deploy Frontend on Vercel

1. **Go to [Vercel](https://vercel.com)** → **Add New Project** → Import your GitHub repo
2. **Framework Preset:** Other
3. **Root Directory:** `frontend` ⚠️ (This is critical - Vercel must look inside `frontend/` for `index.html`)
4. Click **Deploy**

---

### Step 3: Connect Frontend to Backend

1. **Edit `frontend/index.html`** in this repo
2. **Add this line BEFORE the `<script src="./js/api.js">` tag:**
   ```html
   <script>window.API_BASE_URL = 'https://expo-api.onrender.com/api';</script>
   ```
   Replace `expo-api.onrender.com` with your actual Render URL (no trailing slash before `/api`).

3. **Commit and push:**
   ```bash
   git add frontend/index.html
   git commit -m "Connect frontend to deployed backend"
   git push origin main
   ```

4. **Vercel will auto-redeploy** with the new URL

---

### Step 4: Seed the Database

Once your backend is live, run the seeder to populate MongoDB Atlas with sample data:

```bash
# Locally, point to your Atlas database
cd backend
cp .env.example .env
# Edit .env with your MONGO_URI
python seed.py
```

Alternatively, use Render's **Shell** tab:
```bash
cd backend
python seed.py
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/dashboard/stats` | GET | Dashboard statistics |
| `/api/dashboard/alerts` | GET | Active alerts & low stock items |
| `/api/dashboard/inventory-by-category` | GET | Inventory grouped by category |
| `/api/dashboard/recent-orders` | GET | Recent purchase orders |
| `/api/dashboard/optimization` | GET | All optimization analytics |
| `/api/suppliers` | GET, POST | List / Create suppliers |
| `/api/manufacturers` | GET, POST | List / Create manufacturers |
| `/api/distributors` | GET, POST | List / Create distributors |
| `/api/inventory` | GET, POST | List / Create inventory items |
| `/api/orders` | GET, POST | List / Create orders |
| `/api/logistics` | GET, POST | List / Create shipments |

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `dev-secret-key` |
| `MONGO_URI` | MongoDB connection URI | `mongodb://127.0.0.1:27017/supplychain` |

---

## Screenshots

> *Add screenshots of the Dashboard, Inventory, and Optimization pages here*

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Acknowledgments

- Built as a capstone project for Web Development
- UI inspired by futuristic HUD interfaces (JARVIS/Mark II theme)

