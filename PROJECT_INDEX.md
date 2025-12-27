# 📚 Clash Royale AI - Complete Project Index

## Project Structure

```
clashRoyaleAI/
├── 🐍 Core Application Files
│   ├── app.py                          Streamlit UI (Frontend) - Port 8501
│   ├── api.py                          FastAPI Backend - Port 8000
│   └── llm_integration.py              Claude AI Integration with Tool Use
│
├── 📖 Documentation
│   ├── README.md                       Main setup guide
│   ├── CLAUDE_SETUP.md                 Quick start for Claude (5 min)
│   ├── LLM_INTEGRATION.md              Complete LLM documentation
│   ├── WHERE_CLAUDE_INVOKED.md         Detailed explanation of Claude invocation
│   └── PROJECT_INDEX.md                This file
│
├── ⚙️ Configuration
│   ├── requirements.txt                Python dependencies
│   ├── run.sh                          Automated startup script
│   └── .env.example                    Environment variables template
│
└── 📁 Generated (if you run)
    └── venv/                          Virtual environment (created by run.sh)
```

## 🚀 Quick Navigation

### For First-Time Setup
👉 **Start here:** `CLAUDE_SETUP.md` (5 minutes)

### For Detailed LLM Understanding
👉 **Read:** `WHERE_CLAUDE_INVOKED.md` (complete Claude flow)

### For Advanced Integration
👉 **Read:** `LLM_INTEGRATION.md` (full API docs)

### For API Reference
👉 **Check:** API endpoints in `api.py`

## 📋 File Purposes

### 🐍 Python Files

| File | Purpose | Key Exports |
|------|---------|------------|
| `app.py` | Streamlit frontend UI | Web UI with AI tabs |
| `api.py` | FastAPI backend server | REST API endpoints |
| `llm_integration.py` | Claude AI integration | `chat_with_claude()`, analysis functions |

### 📖 Documentation Files

| File | For Whom | Read Time |
|------|----------|-----------|
| `CLAUDE_SETUP.md` | Everyone | 5 min |
| `WHERE_CLAUDE_INVOKED.md` | Developers | 10 min |
| `LLM_INTEGRATION.md` | Advanced users | 20 min |
| `README.md` | Setup reference | 10 min |

## 🎯 Where is Claude Called?

**Quick Answer:**
```
llm_integration.py → chat_with_claude() → client.messages.create()
                                          ↑
                                     This is where Claude is invoked
```

**Detailed Flow:**
```
Streamlit (app.py)
    ↓ HTTP POST
FastAPI (api.py /api/llm/*)
    ↓ imports from
llm_integration.py
    ↓ calls
Anthropic API (Claude)
    ↓ Claude uses tools
Clash Royale API
    ↓ returns data
Claude (analyzes)
    ↓ sends response
Streamlit displays
```

## 🔧 Main APIs

### FastAPI Endpoints (Port 8000)

**Data Endpoints:**
- `GET /api/cards` - All Clash Royale cards
- `GET /api/player/{playerTag}` - Player info
- `GET /api/player/{playerTag}/battles` - Battle history
- `GET /api/tools` - LLM tool definitions

**LLM Endpoints:** ⭐
- `POST /api/llm/chat` - Chat with Claude
- `POST /api/llm/analyze-player` - Analyze a player
- `POST /api/llm/compare-players` - Compare 2 players
- `GET /api/llm/card-analysis` - Meta analysis

**Utility:**
- `GET /health` - Health check

### Streamlit UI (Port 8501)

**Tabs:**
1. **Player Search** - Look up player by tag
2. **Card Info** - View all cards
3. **Battle History** - See player battles
4. **AI Assistant** ⭐ - Talk to Claude
   - Chat with Claude
   - Player Analysis
   - Player Comparison
   - Meta Analysis

## 🤖 Claude Integration Summary

**Model:** `claude-3-5-sonnet-20241022`

**Tools Claude Can Use:**
1. `get_clash_royale_cards()` - Get all cards
2. `get_player_info(playerTag)` - Get player data
3. `get_player_battles(playerTag)` - Get battle history

**How It Works:**
1. You ask Claude something
2. Claude decides which tools to use
3. Tools are automatically called
4. Claude analyzes results
5. Claude responds with insights

## 📊 Dependencies

**Core:**
- `fastapi` - Web framework
- `streamlit` - UI framework
- `httpx` - Async HTTP client
- `anthropic` - Claude API client
- `requests` - HTTP requests
- `pydantic` - Data validation
- `python-dotenv` - Environment variables

**Install:**
```bash
pip install -r requirements.txt
```

## 🚀 Getting Started

### Step 1: Set API Keys
```bash
export CLASH_ROYALE_API_TOKEN='your_token'
export ANTHROPIC_API_KEY='your_key'
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Services

**Terminal 1 - Backend:**
```bash
python3 api.py
# Runs on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
streamlit run app.py
# Opens http://localhost:8501
```

### Step 4: Use AI Assistant
Go to "AI Assistant" tab in Streamlit and start chatting!

## 📚 Documentation Map

```
CLAUDE_SETUP.md
    ├─ Quick setup (5 min)
    └─ Basic understanding of Claude integration
        │
        └─→ Want more details?
                ↓
            WHERE_CLAUDE_INVOKED.md
                ├─ Exact Claude invocation
                ├─ Complete code flow
                └─ Line-by-line breakdown
                    │
                    └─→ Want complete guide?
                            ↓
                        LLM_INTEGRATION.md
                            ├─ Architecture
                            ├─ All endpoints
                            ├─ Tool definitions
                            ├─ Examples
                            └─ Troubleshooting

README.md (General setup reference)
```

## 🎓 Learning Path

**Beginner:** 
1. Read `CLAUDE_SETUP.md`
2. Run the application
3. Use AI Assistant tab

**Intermediate:**
1. Read `WHERE_CLAUDE_INVOKED.md`
2. Trace code flow in editor
3. Modify system prompts in `llm_integration.py`

**Advanced:**
1. Read `LLM_INTEGRATION.md`
2. Add custom tools to Claude
3. Integrate with other LLMs
4. Deploy to cloud

## 🔍 File Quick Reference

### If you want to... → See this file

| Task | File | Lines |
|------|------|-------|
| Understand Claude invocation | `WHERE_CLAUDE_INVOKED.md` | All |
| Start using Claude | `CLAUDE_SETUP.md` | Top |
| Add new LLM endpoint | `api.py` | 192+ |
| Change Claude model | `llm_integration.py` | 115 |
| Add UI for new feature | `app.py` | 230+ |
| See tool definitions | `llm_integration.py` | 17-50 |
| Configure APIs | `.env.example` | All |
| Setup everything | `run.sh` | All |

## 🆘 Troubleshooting

**Claude not responding?**
→ Check `LLM_INTEGRATION.md` → Troubleshooting section

**Tools not being called?**
→ Check `WHERE_CLAUDE_INVOKED.md` → Debug section

**Setup issues?**
→ Check `CLAUDE_SETUP.md` → Quick Setup section

**API errors?**
→ Check `README.md` → Troubleshooting section

## 📞 Key Contacts

- **Claude Documentation:** https://docs.anthropic.com/
- **Clash Royale API:** https://developer.clashroyale.com/api-docs/
- **Streamlit Docs:** https://docs.streamlit.io/
- **FastAPI Docs:** https://fastapi.tiangolo.com/

## 🎯 Project Statistics

| Metric | Value |
|--------|-------|
| Python Files | 3 |
| Documentation Files | 4 |
| Total Lines of Code | ~600 |
| LLM Endpoints | 4 |
| Claude Tools | 3 |
| UI Tabs | 4 |
| API Endpoints | 10+ |

## ✨ Features

✅ Clash Royale API Integration
✅ Claude AI with Automatic Tool Use
✅ Player Analysis & Comparison
✅ Meta Analysis
✅ Interactive Streamlit UI
✅ FastAPI Backend
✅ Async HTTP Requests
✅ Environment Variable Configuration
✅ Comprehensive Documentation

## 🚀 Next Steps

1. Follow `CLAUDE_SETUP.md`
2. Run the app
3. Test Claude features
4. Read `WHERE_CLAUDE_INVOKED.md` for deep dive
5. Explore `LLM_INTEGRATION.md` for advanced usage

---

**You're all set! Everything is documented and ready to go.** 🎉

For the most common question "Where is Claude invoked?" → See **`WHERE_CLAUDE_INVOKED.md`**
