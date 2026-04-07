<div align="center">

# 💎 Spendly — Smart Financial Intelligence Platform

### Track Expenses · Manage Budgets · Monitor Subscriptions · Build Savings Goals

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Chart.js](https://img.shields.io/badge/Chart.js-4-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)](https://github.com/kamrankausher/Spendly/pulls)

A **premium, full-featured personal finance management** web application built with Flask. Features a glassmorphic UI with 3D effects, real-time interactive analytics, AI-powered spending suggestions, OCR receipt scanning, multi-currency support, and Progressive Web App (PWA) capabilities for mobile installation.

---

**[Features](#-features) · [Tech Stack](#-tech-stack) · [Quick Start](#-quick-start) · [Project Structure](#-project-structure) · [Deployment](#-deployment) · [Contributing](#-contributing)**

</div>

---

## ✨ Features

### Core Functionality
| Feature | Description |
|---------|-------------|
| 📊 **Smart Dashboard** | Real-time budget tracking with interactive bar charts, doughnut charts, and spending breakdowns powered by Chart.js |
| 🔍 **Expense Tracking** | Add, edit, and delete transactions with category-based filtering (lifetime, year, 60 days, month, week) |
| 📈 **Financial Analytics** | Financial health score (0–100), AI-powered spending insights, daily average, monthly projections, and category analysis |
| 🎯 **Savings Goals** | Create financial targets with visual progress bars, deadline tracking, and real-time saved amount updates |
| 🔔 **Subscription Alerts** | Track recurring services (Netflix, Spotify, etc.), toggle active/inactive, monitor costs and billing dates |
| 📸 **Receipt Scanner** | Client-side OCR receipt scanning using Tesseract.js — drag & drop or upload, auto-extracts amount, date, and description |
| 📄 **Reports & Export** | Detailed category reports with charts, print-to-PDF, and CSV export of all transaction history |

### User Experience
| Feature | Description |
|---------|-------------|
| 👤 **User Profiles** | Avatar upload, personal info management, password change |
| 💱 **Multi-Currency** | Switch between ₹ (INR), $ (USD), € (EUR), £ (GBP) across all dashboards |
| 🗣️ **Multi-Language** | Interface translation support for English, Hindi, Spanish, and French |
| 🌙 **Dark/Light Theme** | Smooth theme toggle with persistent preference saved in localStorage |
| 📱 **PWA Ready** | Install as a native-like mobile app, responsive across all screen sizes (phone, tablet, desktop) |
| 🔐 **Secure Authentication** | Werkzeug password hashing (PBKDF2), 30-day persistent sessions, CSRF-safe cookie config |
| ⚡ **Optimized Performance** | SQLite WAL mode, connection pooling via Flask `g`, query-level indexing, single DB connection per request |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.9+, Flask 3.x, SQLite3 (WAL mode), Werkzeug |
| **Frontend** | Vanilla HTML5, CSS3, JavaScript (ES6+) |
| **Charts** | Chart.js 4 (bar, doughnut, line charts with gradients) |
| **OCR** | Tesseract.js 5 (client-side, no server processing needed) |
| **Design** | Glassmorphic UI, 3D CSS transforms, micro-animations, custom scrollbar |
| **PWA** | Service Worker (static asset caching), Web App Manifest |
| **Deployment** | Gunicorn, Render / Railway / Heroku compatible |

---

## 🚀 Quick Start

### Prerequisites

Make sure you have the following installed on your system:

- **Python 3.9 or higher** — [Download Python](https://www.python.org/downloads/)
- **pip** (comes bundled with Python)
- **Git** — [Download Git](https://git-scm.com/downloads/)

### Step 1: Clone the Repository

```bash
git clone https://github.com/kamrankausher/Spendly.git
cd Spendly
```

### Step 2: Create a Virtual Environment

Creating a virtual environment isolates the project dependencies from your system Python.

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

> 💡 You'll know the virtual environment is active when you see `(.venv)` at the beginning of your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r expense-tracker/requirements.txt
```

This installs:
- `flask==3.1.3` — Web framework
- `werkzeug==3.1.6` — Password hashing & utilities
- `gunicorn==23.0.0` — Production WSGI server (used for deployment)

### Step 4: Run the Application

```bash
cd expense-tracker
python app.py
```

You should see output like:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5001
```

### Step 5: Open in Browser

Navigate to **http://localhost:5001** in your browser.

### 🎉 Demo Account

A demo account with sample data is **automatically seeded** on first run:

| Field | Value |
|-------|-------|
| **Email** | `demo@spendly.com` |
| **Password** | `password123` |

The demo account comes pre-loaded with:
- 12 sample transactions across 8 categories
- 4 subscription services (Netflix, Spotify, Gym, Adobe)
- 3 savings goals (Emergency Fund, Laptop, Vacation)
- ₹15,000 monthly budget

> **📝 Note:** The SQLite database (`spendly.db`) is auto-created in the `database/` folder on first run. To reset all data and start fresh, simply delete this file and restart the app.

---

## 📁 Project Structure

```
Spendly/
│
├── expense-tracker/              # Main application directory
│   ├── app.py                    # Flask app — all routes, auth, business logic
│   ├── requirements.txt          # Python dependencies (Flask, Werkzeug, Gunicorn)
│   ├── Procfile                  # Gunicorn start command for deployment
│   ├── build.sh                  # Build script for Render deployment
│   │
│   ├── database/
│   │   ├── __init__.py           # Package init
│   │   ├── db.py                 # Database layer — connection pooling, schema, seed data
│   │   └── spendly.db            # SQLite database (auto-generated, git-ignored)
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css         # Complete stylesheet — glassmorphism, animations, responsive
│   │   ├── js/
│   │   │   └── main.js           # Client-side JS — charts, theme, scanner, translations
│   │   ├── sw.js                 # Service Worker — static asset caching for PWA
│   │   ├── manifest.json         # PWA manifest — app name, icons, theme
│   │   └── uploads/              # User avatar uploads (git-ignored)
│   │
│   └── templates/
│       ├── base.html             # Root HTML template (head, body, toast stack)
│       ├── app.html              # Authenticated layout (sidebar, topbar, bottom nav)
│       ├── landing.html          # Public landing page with login/register forms
│       ├── dashboard.html        # Main dashboard — stats, charts, transactions
│       ├── tracking.html         # Expense tracking with filters and suggestions
│       ├── analytics.html        # Financial analytics — health score, insights
│       ├── reports.html          # Reports with charts, tables, export options
│       ├── alerts.html           # Subscription management (add, toggle, delete)
│       ├── goals.html            # Savings goals with progress tracking
│       ├── scanner.html          # OCR receipt scanner with Tesseract.js
│       └── profile.html          # User profile settings and preferences
│
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
├── README.md                     # This file
└── run.bat                       # Windows quick-start script
```

---

## 🗄️ Database Schema

Spendly uses SQLite with the following tables:

| Table | Purpose | Key Fields |
|-------|---------|-----------|
| `users` | User accounts | name, email, password_hash, currency, language, avatar_url |
| `expenses` | Transaction records | amount, category, date, description |
| `budgets` | Monthly budgets | amount, period |
| `subscriptions` | Recurring services | platform, cost, start/end dates, is_active |
| `goals` | Savings targets | title, target_amount, saved_amount, deadline |

All tables use `ON DELETE CASCADE` foreign keys linked to `users.id`, so deleting a user cleanly removes all their data.

**Performance optimizations:**
- WAL (Write-Ahead Logging) mode for concurrent reads
- Indexes on `expenses(user_id, date)`, `expenses(user_id, category)`, `users(email)`
- 8MB SQLite page cache
- Single connection per request via Flask's `g` object

---

## 🌐 Deployment

### Option 1: Deploy on Render (Free Tier)

1. Push your code to GitHub
2. Go to [render.com](https://render.com) → **New → Web Service**
3. Connect your GitHub repository
4. Configure the service:

| Setting | Value |
|---------|-------|
| **Root Directory** | `expense-tracker` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |

5. Add environment variable: `SECRET_KEY` = *(generate a long random string)*
6. Click **Deploy**

### Option 2: Deploy on Railway

1. Go to [railway.app](https://railway.app) → **New Project → Deploy from GitHub**
2. Select your repository
3. Set the **root directory** to `expense-tracker`
4. Railway auto-detects the `Procfile` and deploys

### Option 3: Deploy with Docker (Advanced)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY expense-tracker/ .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5001
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
```

> ⚠️ **Important:** On free-tier hosting (Render, Railway), the filesystem is ephemeral — the SQLite database resets on each deploy. For production use, consider migrating to PostgreSQL or a persistent volume.

---

## 🔧 Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | **Yes** (production) | Dev fallback key | Flask session signing key — use a long random string in production |
| `PORT` | No | `5001` | Server port number |

**Generate a secure secret key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🧪 Running on Different Systems

### Windows
```powershell
git clone https://github.com/kamrankausher/Spendly.git
cd Spendly
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r expense-tracker/requirements.txt
cd expense-tracker
python app.py
# Open http://localhost:5001
```

### macOS
```bash
git clone https://github.com/kamrankausher/Spendly.git
cd Spendly
python3 -m venv .venv
source .venv/bin/activate
pip install -r expense-tracker/requirements.txt
cd expense-tracker
python3 app.py
# Open http://localhost:5001
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update && sudo apt install python3 python3-venv python3-pip git -y
git clone https://github.com/kamrankausher/Spendly.git
cd Spendly
python3 -m venv .venv
source .venv/bin/activate
pip install -r expense-tracker/requirements.txt
cd expense-tracker
python3 app.py
# Open http://localhost:5001
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/Spendly.git`
3. **Create a branch**: `git checkout -b feature/amazing-feature`
4. **Make changes** and test them locally
5. **Commit**: `git commit -m "Add amazing feature"`
6. **Push**: `git push origin feature/amazing-feature`
7. **Open a Pull Request** on the original repository

### Contribution Ideas
- 🔗 Connect to a real database (PostgreSQL/MySQL)
- 📊 Add more chart types and export options
- 🤖 Integrate AI/ML for spending predictions
- 📱 Build a React Native mobile companion app
- 🔄 Add recurring expense auto-tracking
- 🌍 Add more languages and currencies

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

You are free to use, modify, and distribute this project for personal or commercial purposes.

---

<div align="center">

**Built with ❤️ by [Kamran Kausher](https://github.com/kamrankausher)**

💎 *Spendly — Take Control of Your Financial Future*

⭐ If you found this project helpful, please consider giving it a star!

</div>
