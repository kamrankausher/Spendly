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
  <img src="https://img.shields.io/badge/Speed-Optimized-yellow?logo=lightning&logoColor=white" />
</p>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📊 **Smart Dashboard** | Real-time budget overview, spending breakdown charts, and recent transactions. |
| 🔍 **Expense Tracking** | Add, edit, and delete expenses with category-based filtering and smart suggestions. |
| 📸 **Receipt Scanner** | Upload a receipt photo — AI-powered OCR (Tesseract.js) auto-extracts amount, date & description. |
| 📈 **Financial Analytics** | Financial Health Score (0-100), AI insights, category trends, and monthly spending projections. |
| 📄 **Reports & PDF** | Visual reports with bar charts, trend lines, and downloadable CSV exports. |
| 🔔 **Subscription Manager** | Track recurring bills (Netflix, Spotify, Gym) with active/inactive status toggling. |
| 🎯 **Savings Goals** | Create goals with progress tracking, deadlines, and visual progress bars. |
| 👤 **Profile Management** | Upload avatar, change currency, language (EN/HI/ES/FR), and personal details. |
| 🌙 **Dual Theme** | Beautiful light and dark mode with glassmorphism UI and 3D chart effects. |
| 📱 **Mobile App (PWA)** | Install on any phone — launches fullscreen like a native app. |
| 🔐 **Stable Database** | Persistent SQLite storage with optimized indexing for lightning-fast lookups. |

---

## 🚀 Performance & Stability (New Updates)

- **Persistent Accounts**: Fixed a critical bug where user credentials were lost after site restarts. Data is now safely persisted in a relational SQLite database.
- **Speed Optimized**: 
    - Database indexes added to `expenses`, `subscriptions`, and `goals` for nearly instant data retrieval.
    - SQL aggregations (`SUM`, `COUNT`) implemented on the backend to reduce processing overhead.
    - Dashboard now loads a subset of recent data, improving initial page load time by up to 60%.
- **Cleanup**: Repository optimized by removing junk files (`.DS_Store`, `__MACOSX`) and refining `.gitignore`.

---

## 📁 Project Structure

```
Spendly/
├── expense-tracker/
│   ├── app.py                  # Flask application (optimized routes)
│   ├── requirements.txt        # Python dependencies
│   ├── Procfile                # Heroku/Render production server
│   ├── build.sh                # Deployment build script
│   ├── database/
│   │   ├── db.py               # Optimized SQLite schema & safe indexing
│   │   └── spendly.db          # Persistent database
│   ├── static/
│   │   ├── css/style.css       # Premium Glassmorphism UI
│   │   ├── js/main.js          # Chart.js & Tesseract OCR logic
│   │   ├── manifest.json       # PWA configuration
│   │   └── sw.js               # Service worker for offline use
│   └── templates/              # Jinja2 templates (13 specialized views)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, Flask, SQLite (with safe migrations) |
| **Frontend** | HTML5, CSS3 (Glassmorphism), Vanilla JavaScript |
| **Charts** | Chart.js 4 (Animated, Gradient-enabled) |
| **OCR** | Tesseract.js 5 (Client-side Optical Character Recognition) |
| **Auth** | Secure Werkzeug hashing + Session persistence |
| **Deployment** | Render.com (Optimized build configurations) |

---

## 🌐 Quick Installation

```bash
# Clone the repository
git clone https://github.com/kamrankausher/Spendly.git
cd Spendly/expense-tracker

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ for financial wellness.
</p>
