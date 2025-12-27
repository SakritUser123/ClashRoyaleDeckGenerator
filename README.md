# Clash Royale AI Setup Guide

## 📋 Prerequisites

- Python 3.8+
- Clash Royale API Token (get it from https://developer.clashroyale.com/)

## 🚀 Quick Start

### 1. Clone/Setup the Project
```bash
cd /Users/kavithakesavalu/clashRoyaleAI
```

### 2. Get Your API Token
1. Visit https://developer.clashroyale.com/
2. Sign up or login
3. Create an API token
4. Copy your token

### 3. Set Environment Variable
```bash
export CLASH_ROYALE_API_TOKEN='your_token_here'
```

### 4. Run Both Services
```bash
chmod +x run.sh
./run.sh
```

Or run them separately:

#### Terminal 1 - Start FastAPI Backend:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export CLASH_ROYALE_API_TOKEN='your_token_here'
python3 api.py
```

FastAPI will be available at: `http://localhost:8000`

#### Terminal 2 - Start Streamlit Frontend:
```bash
source venv/bin/activate
streamlit run app.py
```

Streamlit will be available at: `http://localhost:8501`

## 📚 API Documentation

### Available Endpoints

**FastAPI Backend (http://localhost:8000)**

- `GET /` - Root endpoint with API info
- `GET /health` - Health check
- `GET /api/cards` - Get all Clash Royale cards
- `GET /api/player/{playerTag}` - Get player info
- `GET /api/player/{playerTag}/battles` - Get player battle history
- `GET /api/tools` - Get LLM tool definitions
- `POST /api/process-tool-call` - Process LLM tool calls

### Example API Calls

**Get Cards:**
```bash
curl http://localhost:8000/api/cards
```

**Get Player Info:**
```bash
curl http://localhost:8000/api/player/%23Y92P0L2
```
(Note: URL-encode the # as %23)

**Get Battle History:**
```bash
curl http://localhost:8000/api/player/%23Y92P0L2/battles
```

**Get LLM Tools:**
```bash
curl http://localhost:8000/api/tools
```

## 🤖 Using with LLM

The `/api/tools` endpoint provides tool definitions compatible with Claude, ChatGPT, and other LLMs. You can use these tools in your LLM prompts to:

1. Get all available cards
2. Look up player information
3. Fetch player battle history

### Tool Definitions

Three tools are available:
- `get_clash_royale_cards` - No parameters needed
- `get_player_info` - Requires `playerTag` (e.g., "#Y92P0L2")
- `get_player_battles` - Requires `playerTag`

## 🏗️ Architecture

```
┌─────────────────┐
│  Streamlit App  │ (Port 8501)
│   (Frontend)    │
└────────┬────────┘
         │ HTTP requests
         │
┌────────▼────────────────┐
│   FastAPI Backend       │ (Port 8000)
│  - Cards API            │
│  - Player API           │
│  - Battles API          │
│  - LLM Tools            │
└────────┬────────────────┘
         │
┌────────▼────────────────┐
│  Clash Royale API       │
│  (api.clashroyale.com)  │
└─────────────────────────┘
```

## 🔑 API Token Safety

⚠️ **Never commit your API token to git!**

Add to `.gitignore`:
```
.env
*.env
.env.local
```

Use environment variables:
```bash
export CLASH_ROYALE_API_TOKEN='your_token'
```

Or create a `.env` file:
```
CLASH_ROYALE_API_TOKEN=your_token_here
```

And load it in your app with `python-dotenv`.

## 🐛 Troubleshooting

**Connection refused (FastAPI)**
- Make sure FastAPI is running: `python3 api.py`
- Check port 8000 is not in use: `lsof -i :8000`

**Streamlit can't connect to API**
- Ensure both services are running
- Check `API_BASE_URL = "http://localhost:8000"` in app.py

**401 Unauthorized from Clash Royale**
- Verify your API token is correct
- Check token hasn't expired
- Re-create token if needed

**Rate limiting**
- Clash Royale API has rate limits
- Add delays between requests if needed

## 📝 Next Steps

1. Integrate with your LLM of choice (Claude, ChatGPT, etc.)
2. Build deck generation logic based on player data
3. Add caching for frequently requested data
4. Implement error handling and retries
5. Add logging for debugging

---

Happy clash! 🏰🎯
