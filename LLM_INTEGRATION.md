# 🤖 Claude LLM Integration Guide

## Overview

Your Clash Royale AI now includes **Claude AI integration**! The system uses Claude (Anthropic's GPT model) with tool use to intelligently query the Clash Royale API.

## Architecture

```
┌─────────────────────────────────┐
│   Streamlit Frontend (8501)      │
│  - Player Search                 │
│  - Card Info                     │
│  - Battle History                │
│  - AI Assistant (NEW!)           │
└────────────┬────────────────────┘
             │
             ├─► FastAPI Backend (8000)
             │   - API endpoints for CR data
             │   - LLM endpoints
             │
             └─► api.py
                 - /api/cards
                 - /api/player/{tag}
                 - /api/player/{tag}/battles
                 - /api/llm/chat ⭐
                 - /api/llm/analyze-player ⭐
                 - /api/llm/compare-players ⭐
                 - /api/llm/card-analysis ⭐
                 │
                 └─► llm_integration.py
                     - chat_with_claude() ⭐
                     - Uses Claude with tool use
                     - Automatically calls CR API tools
```

## 🔑 Setup

### 1. Get API Keys

**Clash Royale API Token:**
- Visit: https://developer.clashroyale.com/
- Create an API token
- Save it

**Anthropic API Key (Claude):**
- Visit: https://console.anthropic.com/
- Create an API key
- Save it

### 2. Set Environment Variables

```bash
export CLASH_ROYALE_API_TOKEN='your_clash_royale_token'
export ANTHROPIC_API_KEY='your_anthropic_api_key'
```

Or create a `.env` file:
```
CLASH_ROYALE_API_TOKEN=your_clash_royale_token
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

**Terminal 1 - FastAPI Backend:**
```bash
export ANTHROPIC_API_KEY='your_key'
export CLASH_ROYALE_API_TOKEN='your_token'
python3 api.py
# FastAPI runs on http://localhost:8000
```

**Terminal 2 - Streamlit Frontend:**
```bash
streamlit run app.py
# Streamlit runs on http://localhost:8501
```

## 🤖 How Claude Integration Works

### The Tool Use Flow

1. **User submits a request** (e.g., "Analyze player #Y92P0L2")
2. **Streamlit sends request** to FastAPI `/api/llm/analyze-player`
3. **FastAPI calls `llm_integration.py`** → `chat_with_claude()`
4. **Claude receives the request + tool definitions**
5. **Claude decides which tools to use** (e.g., get_player_info, get_player_battles)
6. **Claude automatically invokes tools** and processes results
7. **Claude provides intelligent analysis** based on the data
8. **Response is sent back to Streamlit** and displayed

### Example: Player Analysis

When you ask Claude to analyze a player:

```
User: "Analyze player #Y92P0L2"
    ↓
Claude thinks: "I need player info and battle history"
    ↓
Claude calls tools:
  - get_player_info(playerTag="#Y92P0L2")
  - get_player_battles(playerTag="#Y92P0L2")
  - get_clash_royale_cards()
    ↓
Claude processes the data and provides:
  - Skill assessment
  - Deck analysis
  - Win rate insights
  - Improvement suggestions
    ↓
Result displayed in Streamlit
```

## 📚 Available LLM Features

### 1. **General Chat**
- Ask Claude anything about Clash Royale
- Claude automatically fetches relevant data
- See which tools Claude used

**Example prompts:**
- "What's the best meta right now?"
- "How do I counter PEKKA decks?"
- "What are the strongest cards?"

### 2. **Player Analysis**
- Get detailed analysis of a player's performance
- Deck recommendations
- Improvement suggestions

**Endpoint:** `POST /api/llm/analyze-player?player_tag=#Y92P0L2`

### 3. **Player Comparison**
- Compare two players head-to-head
- Playstyle analysis
- Skill assessment

**Endpoint:** `POST /api/llm/compare-players?player_tag1=#Y92P0L2&player_tag2=#Y92P0L3`

### 4. **Meta Analysis**
- Current card meta analysis
- Strong vs weak cards
- Meta trends

**Endpoint:** `GET /api/llm/card-analysis`

## 🛠️ Using the LLM Endpoints Directly

### General Chat

```bash
curl -X POST "http://localhost:8000/api/llm/chat" \
  -G \
  --data-urlencode "message=What is the best Hog Rider counter?"
```

### Player Analysis

```bash
curl -X POST "http://localhost:8000/api/llm/analyze-player" \
  -G \
  --data-urlencode "player_tag=#Y92P0L2"
```

### Player Comparison

```bash
curl -X POST "http://localhost:8000/api/llm/compare-players" \
  -G \
  --data-urlencode "player_tag1=#Y92P0L2" \
  --data-urlencode "player_tag2=#Y92P0L3"
```

### Card Meta Analysis

```bash
curl -X GET "http://localhost:8000/api/llm/card-analysis"
```

## 📝 How Tools Work

Claude has access to 3 tools:

### Tool 1: `get_clash_royale_cards`
- **Description:** Get all available Clash Royale cards
- **Parameters:** None
- **Returns:** List of all cards with stats

### Tool 2: `get_player_info`
- **Description:** Get player information
- **Parameters:** `playerTag` (string, e.g., "#Y92P0L2")
- **Returns:** Player data (name, trophies, level, cards, etc.)

### Tool 3: `get_player_battles`
- **Description:** Get recent battle history
- **Parameters:** `playerTag` (string)
- **Returns:** Last 20 battles with results, deck info, opponents

## 🔌 Integration with Your LLM

The `/api/tools` endpoint returns tool definitions compatible with any LLM:

```bash
curl http://localhost:8000/api/tools
```

This returns:
```json
{
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_clash_royale_cards",
        "description": "...",
        "parameters": {...}
      }
    },
    ...
  ]
}
```

You can use these tools with:
- Claude (via Anthropic API) ✅
- GPT-4 (via OpenAI API)
- Local LLMs (Ollama, LlamaIndex, etc.)

## 🎯 Example Usage Scenarios

### Scenario 1: Quick Meta Check
```
User: "Tell me about the current Clash Royale meta"
↓
Claude calls: get_clash_royale_cards()
↓
Claude provides: Meta analysis, top cards, strategies
```

### Scenario 2: Player Improvement
```
User: "How can I improve as a player? Analyze my account: #Y92P0L2"
↓
Claude calls:
  - get_player_info(#Y92P0L2)
  - get_player_battles(#Y92P0L2)
  - get_clash_royale_cards()
↓
Claude provides: Specific improvement advice based on your data
```

### Scenario 3: Deck Building
```
User: "Analyze my deck and suggest improvements"
↓
Claude calls: get_player_info() and get_clash_royale_cards()
↓
Claude provides: Deck analysis and synergy suggestions
```

## 🐛 Troubleshooting

### "ANTHROPIC_API_KEY not set"
```bash
export ANTHROPIC_API_KEY='your_key'
```

### "Connection refused" to FastAPI
- Make sure FastAPI is running: `python3 api.py`
- Check port 8000 is available: `lsof -i :8000`

### "Claude tool use failed"
- Check Anthropic API key is valid
- Check you have API quota available
- Look at the error message for details

### "Clash Royale API 401 Unauthorized"
- Verify your API token is correct
- Token may have expired - get a new one
- Check token has proper permissions

### Timeout errors
- Add the `timeout=60` parameter to requests
- Some analyses take time with multiple tool calls
- Claude may be rate limited

## 📊 Monitoring Tool Calls

In the Streamlit UI, you can see which tools Claude used:

```
Tools Used (3):
- Tool: get_player_info
  Input: {"playerTag": "#Y92P0L2"}
- Tool: get_player_battles
  Input: {"playerTag": "#Y92P0L2"}
- Tool: get_clash_royale_cards
  Input: {}
```

This helps you understand:
- What data Claude fetched
- Whether Claude made efficient tool calls
- If tools are working properly

## 🔐 Security Notes

⚠️ **Never commit API keys to git!**

Add to `.gitignore`:
```
.env
.env.local
*.env
__pycache__/
.python-version
```

Use environment variables or `.env` files (in .gitignore).

## 🚀 Next Steps

1. ✅ Run the application with Claude integration
2. ✅ Test the AI Assistant tab in Streamlit
3. ✅ Try different prompts to see Claude's tool use
4. Optional: Integrate with other LLMs (GPT-4, Llama, etc.)
5. Optional: Add more tools (clan data, tournaments, etc.)

## 📞 Support

- Claude Docs: https://docs.anthropic.com/
- Clash Royale API: https://developer.clashroyale.com/api-docs/
- Streamlit Docs: https://docs.streamlit.io/

---

Happy clashing! 🏰🤖
