# ⚽ Football Player Performance Analytics Dashboard

> **⚠️ Synthetic Data Notice:** All player names, teams, and statistics in this project are **computer-generated** and do **not** represent real-world football results or actual players.

An interactive football (soccer) analytics dashboard built with **Python**, **Streamlit**, and **Plotly**. Designed as a portfolio-quality project for data analysts and Python developers.

---

## 📸 Features

| Page | What You Get |
|---|---|
| **Overview** | 5 live KPI cards · Top-10 Goals · Top-10 Rating · Top-10 Assists |
| **Player Analysis** | Side-by-side player comparison · Goals vs Assists scatter · Shots vs Goals scatter · Searchable stats table · CSV export |
| **Team Analysis** | Goals & Assists per team · Squad composition stacked bar · Avg Rating per team · Team summary table |
| **Position Analysis** | Donut squad composition · Rating box plot · Avg Goals/Assists per role · Clean sheets (GK & DEF) |

- 🎛️ **Sidebar filters** — Season, Team, Position, Player (all multiselect)
- 🌑 **Dark football-pitch theme** — green accent, dark background
- 📥 **CSV download** — export the filtered stats table
- ✅ **Input validation** — handles missing data and empty filter states gracefully

---

## 📁 Project Structure

```
IBM Analytics/
├── app.py                  # Main Streamlit application
├── generate_data.py        # Standalone synthetic dataset generator
├── football_players.csv    # Pre-generated synthetic dataset (200 rows)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🗃️ Dataset

The synthetic dataset contains **200 rows** — 100 unique players × 2 seasons (`2022-23`, `2023-24`).

| Column | Description |
|---|---|
| `player_id` | Unique player identifier |
| `player_name` | Synthetic full name |
| `team` | One of 8 fictional clubs |
| `position` | GK · DEF · MID · FWD |
| `season` | 2022-23 or 2023-24 |
| `age` | Player age that season |
| `nationality` | Country string |
| `appearances` | Matches played |
| `minutes_played` | Total minutes |
| `goals` | Goals scored |
| `assists` | Assists provided |
| `shots` | Total shots attempted |
| `shots_on_target` | Shots on target |
| `pass_accuracy` | Pass accuracy % |
| `dribbles` | Successful dribbles |
| `tackles` | Tackles made |
| `yellow_cards` | Yellow cards received |
| `red_cards` | Red cards received |
| `clean_sheets` | Clean sheets (GK/DEF only) |
| `rating` | Composite performance rating (5.0–9.5) |

---

## ⚙️ Prerequisites

- Python **3.10+**
- pip

---

## 🚀 Run Locally

### 1. Clone or download the project

```bash
git clone https://github.com/your-username/football-analytics-dashboard.git
cd football-analytics-dashboard
```

### 2. Create and activate a virtual environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. (Optional) Re-generate the dataset

The CSV is already included. To regenerate it:

```bash
python generate_data.py
```

### 5. Launch the dashboard

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## ☁️ Deploy to Streamlit Community Cloud

1. Push this entire project to a **public GitHub repository**.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **"New app"**, select your repository, branch (`main`), and set the main file to `app.py`.
4. Click **"Deploy"** — Streamlit will install `requirements.txt` automatically.
5. Your dashboard will be live at a public URL within ~2 minutes.

> **Note:** `football_players.csv` must be committed to the repository alongside `app.py`. Streamlit Community Cloud does not persist files generated at runtime.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web app framework |
| [Pandas](https://pandas.pydata.org) | Data manipulation |
| [NumPy](https://numpy.org) | Numerical operations |
| [Plotly Express & Graph Objects](https://plotly.com/python/) | Interactive charts |

---

## 📌 KPI Calculation Reference

All KPIs are calculated live from the **filtered** DataFrame — nothing is hardcoded.

| KPI | Formula |
|---|---|
| Total Players | `df["player_id"].nunique()` |
| Total Goals | `df["goals"].sum()` |
| Total Assists | `df["assists"].sum()` |
| Total Minutes | `df["minutes_played"].sum()` |
| Avg Rating | `df["rating"].mean()` |

---

## ⚠️ Disclaimer

This project uses **entirely synthetic data** generated for educational and portfolio demonstration purposes. The player names, team names, statistics, and ratings bear no resemblance to any real football players, clubs, or competitions. Do not cite this data as factual football statistics.
