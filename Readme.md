# 🏏 PSL Analytics Hub

**Comprehensive Pakistan Super League statistics, analytics, and insights platform**

A full-stack analytics platform featuring a FastAPI backend, Streamlit dashboard, and comprehensive cricket statistics from the Pakistan Super League (PSL) 2016-2025.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/PSL-Analytics-Hub)

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Dashboard](#dashboard)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Contributing](#contributing)

## ✨ Features

### 🎯 Core Features
- **Player Statistics**: Comprehensive batting and bowling statistics for all PSL players
- **Team Analytics**: Team performance metrics, win/loss records, and head-to-head comparisons
- **Bowler Analytics**: Detailed bowling statistics including economy rates, wickets, and match performance
- **Interactive Comparisons**: Side-by-side player and team comparisons
- **Leaderboards**: Top performers across various categories
- **Real-time API**: RESTful API with fast response times

### 📊 Dashboard Features
- Interactive visualizations with Plotly
- Team logos and branding
- Player images
- Responsive design
- Caching for optimal performance
- Search and fuzzy matching
- Export capabilities

### 🔧 Technical Features
- FastAPI backend with automatic OpenAPI documentation
- Streamlit dashboard with modern UI
- Pandas-based analytics engine
- RESTful API design
- CORS enabled for cross-origin requests
- Vercel serverless deployment ready

## 🏗️ Architecture

```
PSL-Analytics-Hub/
├── api/                      # FastAPI Backend
│   ├── __init__.py
│   ├── index.py             # Vercel entry point
│   ├── app.py               # FastAPI application
│   ├── routes/              # API endpoints
│   │   ├── players.py
│   │   ├── bowlers.py
│   │   ├── teams.py
│   │   └── health.py
│   └── schemas.py           # Pydantic models
├── analytics/               # Analytics Engine
│   ├── batting.py
│   ├── bowling.py
│   ├── compare.py
│   └── team.py
├── services/                # Services Layer
│   └── data.py             # Data loading & caching
├── psl_dashboard/          # Streamlit Dashboard
│   ├── __init__.py
│   ├── config.py           # Configuration
│   ├── api_client.py       # API client
│   ├── utils.py            # UI components
│   ├── helpers.py          # Helper functions
│   └── tabs/               # Dashboard tabs
├── Data/                   # Dataset
│   └── PSL_Complete_Dataset_2016_2025.csv
├── images/                 # Team logos & assets
│   ├── psl_logo.png
│   ├── islamabad_united.png
│   ├── karachi_kings.png
│   ├── lahore_qalandars.png
│   ├── multan_sultans.png
│   ├── peshawar_zalmi.png
│   └── quetta_gladiators.png
├── app.py                  # Streamlit entry point
├── requirements.txt        # Python dependencies
└── vercel.json            # Vercel configuration
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip or uv

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/PSL-Analytics-Hub.git
cd PSL-Analytics-Hub
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the API (Development)**
```bash
uvicorn api.app:app --reload
```
API will be available at `http://127.0.0.1:8000`

4. **Run the Dashboard**
```bash
streamlit run app.py
```
Dashboard will be available at `http://localhost:8501`

### Using the Dashboard with Deployed API

If your API is already deployed on Vercel:
```bash
$env:PSL_API_BASE="https://your-api-url.vercel.app"
streamlit run app.py
```

## 📚 API Documentation

Once the API is running, visit:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### Key Endpoints

#### Players
- `GET /players` - List all players
- `GET /players/{name}/stats` - Get player statistics
- `GET /players/{name}/vs-team/{team}` - Player vs team statistics

#### Bowlers
- `GET /bowlers` - List all bowlers
- `GET /bowlers/{name}/stats` - Get bowler statistics
- `GET /bowlers/top?limit=10` - Top wicket takers
- `POST /bowlers/compare` - Compare two bowlers

#### Teams
- `GET /teams` - List all teams
- `GET /teams/{name}/stats` - Get team statistics
- `GET /teams/{name}/vs-team/{opponent}` - Head-to-head comparison

## 🎨 Dashboard

The Streamlit dashboard provides an interactive interface for exploring PSL statistics.

### Features
- **Home**: Overview and quick stats
- **Players**: Search and view player statistics
- **Bowlers**: Bowling analytics and comparisons
- **Teams**: Team performance and matchups
- **Compare**: Side-by-side player/team comparisons
- **Leaderboards**: Top performers across categories
- **API Docs**: Interactive API documentation

### Configuration

Edit `psl_dashboard/config.py` or set environment variables:

```python
# API Base URL
PSL_API_BASE="https://your-api.vercel.app"
```

## 📁 Project Structure

### Backend (`api/`)
- **app.py**: Main FastAPI application
- **index.py**: Vercel serverless handler
- **routes/**: API endpoint modules
- **schemas.py**: Pydantic data models

### Analytics (`analytics/`)
- **batting.py**: Batting statistics functions
- **bowling.py**: Bowling statistics functions
- **compare.py**: Comparison utilities
- **team.py**: Team analytics

### Dashboard (`psl_dashboard/`)
- **config.py**: Configuration and constants
- **api_client.py**: API communication
- **utils.py**: UI components
- **tabs/**: Individual dashboard tabs

## ⚙️ Configuration

### Environment Variables

```bash
# API Base URL (for dashboard)
PSL_API_BASE=https://your-api.vercel.app

# For local development
PSL_API_BASE=http://127.0.0.1:8000
```

### Team Logos

Place team logos in the `images/` directory:
- `islamabad_united.png`
- `karachi_kings.png`
- `lahore_qalandars.png`
- `multan_sultans.png`
- `peshawar_zalmi.png`
- `quetta_gladiators.png`
- `psl_logo.png`

## 🚀 Deployment

### Vercel Deployment (API)

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Deploy**
```bash
vercel
```

3. **Configure**
Ensure `vercel.json` is present:
```json
{
  "version": 2
}
```

### Streamlit Cloud (Dashboard)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy from your repository
4. Set `PSL_API_BASE` environment variable in settings

## 📊 Dataset

The project uses the **PSL Complete Dataset (2016-2025)** containing:
- 40,000+ ball-by-ball records
- Player statistics
- Match outcomes
- Team performance data
- Dismissal information

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Pakistan Super League for the amazing cricket
- FastAPI and Streamlit communities
- All contributors to this project

## 📧 Contact

Project Link: [https://github.com/yourusername/PSL-Analytics-Hub](https://github.com/yourusername/PSL-Analytics-Hub)

---

**Built with ❤️ using FastAPI, Streamlit, and Pandas**