# Quick Start - Claude LLM Integration

## What Changed?

Added **Claude AI** (Anthropic's GPT model) integration to your Clash Royale app with tool use capabilities.

## Files Added/Updated

- ✅ **llm_integration.py** - NEW! Claude integration with tool use
- ✅ **api.py** - Added 4 new LLM endpoints
- ✅ **app.py** - Added AI Assistant tab with 4 sub-features
- ✅ **requirements.txt** - Added `anthropic` package
- ✅ **LLM_INTEGRATION.md** - Complete documentation

## 🚀 Quick Setup (5 minutes)

### 1. Get API Keys
```
Clash Royale: https://developer.clashroyale.com/
Claude (Anthropic): https://console.anthropic.com/
```

### 2. Set Environment Variables
```bash
export CLASH_ROYALE_API_TOKEN='your_token'
export ANTHROPIC_API_KEY='your_key'
```

### 3. Install & Run
```bash
pip install anthropic  # or run: pip install -r requirements.txt

# Terminal 1
python3 api.py

# Terminal 2
streamlit run app.py
```

### 4. Use AI Assistant Tab
Go to http://localhost:8501 → "AI Assistant" tab

## 🤖 How It Works

Claude has **3 tools** it can automatically use:

1. **get_clash_royale_cards** - Get all cards with stats
2. **get_player_info** - Get player data by tag
3. **get_player_battles** - Get player's recent battles

### Example Flow:
```
You: "Analyze player #Y92P0L2"
  ↓
Claude: "I need player info and battles"
  ↓
Claude calls: get_player_info() + get_player_battles() + get_clash_royale_cards()
  ↓
Claude analyzes and responds: "Based on their data, here's what I found..."
  ↓
You see: Response + which tools Claude used
```

## 📍 Where is Claude Called?

**File:** `llm_integration.py`

**Key Function:**
```python
def chat_with_claude(user_message: str, system_prompt: Optional[str] = None):
    """Send a message to Claude with access to tools"""
    # Uses client.messages.create() with tools parameter
    # Claude automatically decides which tools to use
    # Returns final response + list of tool calls made
```

**Called From:** `api.py` in these endpoints:
- `POST /api/llm/chat` - General chat
- `POST /api/llm/analyze-player` - Player analysis
- `POST /api/llm/compare-players` - Compare 2 players  
- `GET /api/llm/card-analysis` - Meta analysis

**Invoked From:** Streamlit UI in `app.py` Tab 4: "AI Assistant"

## 🔗 The Chain

```
Streamlit UI (app.py)
    ↓ HTTP POST/GET
FastAPI (api.py)
    ↓ imports & calls
llm_integration.py (chat_with_claude)
    ↓ uses Anthropic client
Claude API (Anthropic)
    ↓ Claude decides to use tools
FastAPI tool endpoints (api.py)
    ↓ calls Clash Royale API
Clash Royale API
    ↓ returns data
Claude (processes results)
    ↓ generates response
Streamlit (displays result)
```

## 📋 LLM Endpoints

All in `api.py`:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/llm/chat` | POST | General chat with Claude |
| `/api/llm/analyze-player` | POST | Analyze a player |
| `/api/llm/compare-players` | POST | Compare 2 players |
| `/api/llm/card-analysis` | GET | Meta analysis |

## 🎯 Try It Now

1. Start both services (FastAPI + Streamlit)
2. Go to Streamlit → "AI Assistant" tab
3. Try one of these:
   - **Chat**: "What's the best Hog Rider counter?"
   - **Player Analysis**: Paste any player tag
   - **Player Comparison**: Compare 2 players
   - **Meta Analysis**: Click the button

## ⚙️ Configuration

Set environment variables:
```bash
ANTHROPIC_API_KEY=sk-ant-...          # Required for Claude
CLASH_ROYALE_API_TOKEN=...            # Required for CR data
```

Default model: `claude-3-5-sonnet-20241022`

To change: Edit `llm_integration.py` line ~95:
```python
model="claude-3-5-sonnet-20241022",  # Change this
```

Other models:
- `claude-3-opus-20250219` (most powerful)
- `claude-3-sonnet-20240229` (balanced)
- `claude-3-haiku-20240307` (fastest, cheapest)

## 📚 Full Documentation

See `LLM_INTEGRATION.md` for:
- Detailed architecture
- All API endpoints
- Example tool use flows
- Troubleshooting
- Security notes
- Integration with other LLMs

## 🆘 Quick Debug

**Claude not responding?**
```bash
echo $ANTHROPIC_API_KEY  # Check it's set
```

**Tools not being called?**
- Check Claude model supports tool use (all claude-3 models do)
- Look at error logs
- Make sure FastAPI is running

**Data not returned?**
- Check Clash Royale API token
- Check player tag is valid (e.g., #Y92P0L2)

---

You're all set! The model is Claude, invoked via `llm_integration.py`, with automatic tool use. 🚀
