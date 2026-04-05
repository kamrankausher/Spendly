# 💎 Spendly — Financial Intelligence Platform

<p align="center">
  <strong>Track expenses, scan receipts, and manage your finances with AI-powered insights.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-3.1-green?logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/Chart.js-4.0-orange?logo=chartdotjs&logoColor=white" />
  <img src="https://img.shields.io/badge/Tesseract.js-5.0-red?logo=googlecloud&logoColor=white" />
  <img src="https://img.shields.io/badge/PWA-Installable-purple?logo=pwa&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
</p>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📊 **Smart Dashboard** | Real-time budget overview, spending breakdown charts, and recent transactions |
| 🔍 **Expense Tracking** | Add, edit, and delete expenses with category-based filtering and smart suggestions |
| 📸 **Receipt Scanner** | Upload a receipt photo — AI-powered OCR (Tesseract.js) auto-extracts amount, date & description |
| 📈 **Financial Analytics** | Financial Health Score (0-100), AI insights, category trends, and monthly spending projections |
| 📄 **Reports & PDF** | Visual reports with bar charts, trend lines, and downloadable PDF/CSV exports |
| 🔔 **Subscription Manager** | Track recurring bills (Netflix, Spotify, Gym) with active/inactive status toggling |
| 🎯 **Savings Goals** | Create goals with progress tracking, deadlines, and visual progress bars |
| 👤 **Profile Management** | Upload avatar, change currency, language (EN/HI/ES/FR), and personal details |
| 🌙 **Dual Theme** | Beautiful light and dark mode with glassmorphism UI and 3D chart effects |
| 📱 **Mobile App (PWA)** | Install on any phone — launches fullscreen like a native app |
| 🔐 **Secure Auth** | Password hashing with Werkzeug, session management, login-protected routes |

---

## 🖼️ Screenshots

### Dashboard (Light Mode)
> Real-time budget stats, spending breakdown bar chart, budget overview doughnut, transaction table with delete, and quick-add expense form.

### Receipt Scanner
> Drag-and-drop receipt images — Tesseract.js OCR extracts amount, date, and merchant info automatically.

### Financial Analytics
> Health Score ring chart, AI-driven smart insights, category spending bar chart, and monthly trend line chart.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ ([python.org](https://python.org))
- pip (comes with Python)

### Installation

```bash
# Clone the repository
git clone https://github.com/kamrankausher/Spendly.git
cd Spendly/expense-tracker

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
.\venv\Scripts\Activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open **http://127.0.0.1:5001** in your browser.

> **Demo Account**: `demo@spendly.com` / `password123`

---

## 📁 Project Structure

```
Spendly/
├── expense-tracker/
│   ├── app.py                  # Flask application (all routes)
│   ├── requirements.txt        # Python dependencies
│   ├── Procfile                # Production server (gunicorn)
│   ├── build.sh                # Build script for deployment
│   ├── database/
│   │   ├── db.py               # SQLite schema & seed data
│   │   └── spendly.db          # Database (auto-created)
│   ├── static/
│   │   ├── css/style.css       # Glassmorphism themes & responsive design
│   │   ├── js/main.js          # Charts, OCR, translations, delete modal
│   │   ├── manifest.json       # PWA manifest
│   │   ├── sw.js               # Service worker (offline caching)
│   │   └── uploads/            # User avatar uploads
│   └── templates/              # 13 Jinja2 HTML templates
│       ├── base.html           # Root template
│       ├── app.html            # Sidebar shell (extends base)
│       ├── landing.html        # Landing/marketing page
│       ├── login.html          # Login form
│       ├── register.html       # Registration form
│       ├── dashboard.html      # Main dashboard
│       ├── tracking.html       # Expense tracking + insights
│       ├── scanner.html        # Receipt OCR scanner
│       ├── analytics.html      # Financial analytics
│       ├── reports.html        # Reports & exports
│       ├── alerts.html         # Subscription manager
│       ├── goals.html          # Savings goals
│       └── profile.html        # User profile & settings
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, Flask, SQLite |
| **Frontend** | HTML5, CSS3 (Glassmorphism), Vanilla JavaScript |
| **Charts** | Chart.js 4 (bar, doughnut, line with gradients) |
| **OCR** | Tesseract.js 5 (client-side receipt scanning) |
| **Auth** | Werkzeug (password hashing + session management) |
| **PWA** | Service Worker + Web App Manifest |
| **Production** | Gunicorn WSGI server |
| **Deployment** | Render.com (free tier) |

---

## 🌐 Deployment

### Deploy to Render (Free)

1. Push this repo to your GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repo
4. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Root Directory**: `expense-tracker`
5. Add environment variable: `SECRET_KEY` = any random string
6. Click **Deploy** → Live in ~2 minutes!

---

## 🔧 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes (production) | Flask session secret key. Use a long random string. |
| `PYTHON_VERSION` | No | Set to `3.11.0` on Render if needed. |

---

## 📱 Install as Mobile App

Spendly is a **Progressive Web App (PWA)**:

1. Open the deployed URL on your phone's browser (Chrome/Edge)
2. Tap the **"📱 Install App"** button in the header
3. Or use browser menu → **"Add to Home Screen"**
4. The app launches fullscreen — just like a native app!

---

## 🌍 Multi-Language Support

| Language | Code |
|----------|------|
| 🇬🇧 English | `en` |
| 🇮🇳 Hindi | `hi` |
| 🇪🇸 Spanish | `es` |
| 🇫🇷 French | `fr` |

Change language from **Profile → Preferences → Language**.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/kamrankausher">Kamran Kausher</a>
</p>
