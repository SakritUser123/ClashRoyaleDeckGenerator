# 📚 COMPLETE DOCUMENTATION SUMMARY

## 🎯 Your Question: "Where is the GPT model invoked in the LLM call?"

### 🔴 DIRECT ANSWER:
**File:** `llm_integration.py`
**Function:** `chat_with_claude()`
**Line:** ~115
**Code:** `client.messages.create(model="claude-3-5-sonnet-20241022", ...)`

---

## 📖 Documentation Roadmap

```
START HERE
    ↓
├─ ANSWER_WHERE_CLAUDE_IS_INVOKED.md (THIS FILE - Direct answer)
│   └─→ Quick, to the point
│
├─ CLAUDE_SETUP.md (5 min setup)
│   └─→ How to run everything
│
├─ WHERE_CLAUDE_INVOKED.md (Detailed flow)
│   └─→ Complete breakdown line-by-line
│
├─ LLM_INTEGRATION.md (Complete guide)
│   └─→ All endpoints & advanced usage
│
├─ ARCHITECTURE.md (Visual diagrams)
│   └─→ System architecture & flows
│
└─ PROJECT_INDEX.md (File reference)
    └─→ All files explained
```

---

## 🔄 The Invocation Chain

```
1. Streamlit UI (app.py)
   User clicks "Analyze Player"
        ↓
2. HTTP POST Request
   requests.post("/api/llm/analyze-player")
        ↓
3. FastAPI Endpoint (api.py line 216)
   @app.post("/api/llm/analyze-player")
   async def llm_analyze_player(player_tag: str):
        ↓
4. Import & Call (api.py line 222)
   from llm_integration import analyze_player_for_deck_suggestion
   response = analyze_player_for_deck_suggestion(player_tag)
        ↓
5. Analysis Function (llm_integration.py line 175)
   def analyze_player_for_deck_suggestion(player_tag: str):
   response, tool_calls = chat_with_claude(user_message)
        ↓
6. Main LLM Function (llm_integration.py line 100)
   def chat_with_claude(user_message: str, system_prompt: str):
        ↓
7. 🎯 CLAUDE INVOCATION (llm_integration.py line 115)
   response = client.messages.create(
       model="claude-3-5-sonnet-20241022",
       max_tokens=2048,
       system=system_prompt,
       tools=CLASH_ROYALE_TOOLS,
       messages=messages
   )
        ↓
8. Anthropic API
   Claude receives the request and processes it
        ↓
9. Tool Use (Lines 120-145)
   Claude decides to use tools, we execute them
        ↓
10. Response to User
    JSON sent back through FastAPI → Streamlit
```

---

## 📁 Key Files

### 🔴 MOST IMPORTANT: `llm_integration.py`

This is where Claude is invoked. Key points:

```python
# Line 10: Create Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Lines 17-50: Define tools Claude can use
CLASH_ROYALE_TOOLS = [
    {"name": "get_clash_royale_cards", ...},
    {"name": "get_player_info", ...},
    {"name": "get_player_battles", ...}
]

# Lines 100-160: Main function
def chat_with_claude(user_message: str, system_prompt: Optional[str] = None):
    # ... setup ...
    
    # LINE 115: Claude is called here
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",  ← MODEL
        max_tokens=2048,
        system=system_prompt,
        tools=CLASH_ROYALE_TOOLS,            ← 3 TOOLS
        messages=messages
    )
    
    # Lines 120-160: Handle tool use
    if response.stop_reason == "tool_use":
        # Claude wants to use tools
        # Execute tools and send results back
    else:
        # Claude is done, return response

# Lines 175-190: Helper functions that use chat_with_claude()
def analyze_player_for_deck_suggestion(player_tag: str):
def get_card_analysis():
def compare_players(player_tag1: str, player_tag2: str):
```

### 🟢 `api.py` - FastAPI Backend

Exposes endpoints that call `llm_integration.py`:

```python
# Lines 192-205: General chat
@app.post("/api/llm/chat")
async def llm_chat(message: str):
    response, tool_calls = chat_with_claude(message)

# Lines 207-220: Player analysis
@app.post("/api/llm/analyze-player")
async def llm_analyze_player(player_tag: str):
    response = analyze_player_for_deck_suggestion(player_tag)

# Lines 222-235: Player comparison
@app.post("/api/llm/compare-players")
async def llm_compare_players(player_tag1: str, player_tag2: str):
    response = compare_players(player_tag1, player_tag2)

# Lines 237-250: Meta analysis
@app.get("/api/llm/card-analysis")
async def llm_card_analysis():
    response = get_card_analysis()
```

### 🔵 `app.py` - Streamlit UI

Calls FastAPI endpoints:

```python
# Line 235: Chat button
response = requests.post(
    f"{API_BASE_URL}/api/llm/chat",
    params={"message": user_message}
)

# Line 290: Analysis button
response = requests.post(
    f"{API_BASE_URL}/api/llm/analyze-player",
    params={"player_tag": tag}
)

# Similar for compare and meta analysis...
```

---

## 🤖 Claude Model Details

**Model Name:** `claude-3-5-sonnet-20241022`

**Provider:** Anthropic

**Type:** Large Language Model (LLM)

**Capabilities:**
- Multi-turn conversations
- Tool use (automatic function calling)
- System prompts
- Max context: 200,000 tokens
- Output: Up to configured max_tokens

**Tools Available:**
1. `get_clash_royale_cards` - No parameters
2. `get_player_info` - Requires `playerTag`
3. `get_player_battles` - Requires `playerTag`

**How It Works:**
1. You ask Claude something
2. Claude sees the 3 available tools
3. Claude decides which tools to use (if any)
4. We execute the tools Claude requests
5. Claude analyzes the results
6. Claude provides insights

---

## 🚀 To See It In Action

### Quick Test:

```bash
# 1. Set API keys
export ANTHROPIC_API_KEY='your_key'
export CLASH_ROYALE_API_TOKEN='your_token'

# 2. Run FastAPI
python3 api.py

# 3. In another terminal, run Streamlit
streamlit run app.py

# 4. Go to http://localhost:8501
# 5. Click "AI Assistant" tab
# 6. Type a question, Claude will be invoked!
```

### Direct API Test:

```bash
curl -X POST "http://localhost:8000/api/llm/chat" \
  -G \
  --data-urlencode "message=What is the best Hog Rider counter?"
```

---

## 📊 System Overview

```
┌─────────────────────────────────────────┐
│  User (Streamlit UI)                    │
│  app.py - AI Assistant Tab              │
└──────────────────┬──────────────────────┘
                   │ HTTP POST
                   ↓
┌──────────────────────────────────────────┐
│  FastAPI Backend (api.py)                │
│  /api/llm/chat                           │
│  /api/llm/analyze-player                 │
│  /api/llm/compare-players                │
│  /api/llm/card-analysis                  │
└──────────────────┬───────────────────────┘
                   │ Imports & Calls
                   ↓
┌────────────────────────────────────────────┐
│  LLM Integration (llm_integration.py)       │
│  chat_with_claude()                        │
│  analyze_player_for_deck_suggestion()      │
│  get_card_analysis()                       │
│  compare_players()                         │
└──────────────────┬────────────────────────┘
                   │ Calls client.messages.create()
                   ↓ (Line 115)
┌────────────────────────────────────────────┐
│  🎯 CLAUDE API (Anthropic)                 │
│  model="claude-3-5-sonnet-20241022"        │
│  with 3 tools available                    │
└────────────────────────────────────────────┘
                   │
                   ├─→ Tool calls Clash Royale API
                   │
                   └─→ Analyzes results
                   │
                   ↓
│  Returns response                          │
└──────────────────────────────────────────┘
                   │
                   ↓ Response
┌──────────────────────────────────────────┐
│  Back through FastAPI                    │
└──────────────────┬──────────────────────┘
                   │
                   ↓ Display
┌──────────────────────────────────────────┐
│  User sees Claude's analysis             │
│  + Tools Claude used                     │
└──────────────────────────────────────────┘
```

---

## ❓ FAQ

**Q: Where is Claude invoked?**
A: `llm_integration.py` line ~115 in `client.messages.create()`

**Q: What model is used?**
A: `claude-3-5-sonnet-20241022`

**Q: Can I change the model?**
A: Yes, edit line 115 in `llm_integration.py`

**Q: What tools can Claude use?**
A: 3 tools - get_cards, get_player_info, get_player_battles

**Q: How does Claude call the tools?**
A: Automatically via tool_use response type - we execute what Claude requests

**Q: Can I add more tools?**
A: Yes, add to `CLASH_ROYALE_TOOLS` in `llm_integration.py` (lines 17-50)

**Q: Is tool use automatic?**
A: Yes! Claude decides when to use tools, we handle the execution

---

## 📞 Files Reference

| File | Purpose | Claude? |
|------|---------|---------|
| `llm_integration.py` | LLM orchestration | ✅ YES (line 115) |
| `api.py` | API endpoints | ❌ Calls llm_integration |
| `app.py` | UI | ❌ Calls FastAPI |
| `requirements.txt` | Dependencies | - |
| `CLAUDE_SETUP.md` | Setup guide | Doc |
| `WHERE_CLAUDE_INVOKED.md` | Detailed guide | Doc |
| `LLM_INTEGRATION.md` | Complete docs | Doc |
| `ARCHITECTURE.md` | Diagrams | Doc |

---

## ✨ The Bottom Line

**You asked:** Where is the GPT model invoked?

**Answer:**
- **File:** `llm_integration.py`
- **Function:** `chat_with_claude()`
- **Line:** 115
- **Code:** `client.messages.create(...)`
- **Model:** Claude 3.5 Sonnet

That's it! Simple and clean. 🚀

---

For more details, see:
- `WHERE_CLAUDE_INVOKED.md` - Complete code breakdown
- `LLM_INTEGRATION.md` - Full API documentation
- `ARCHITECTURE.md` - Visual diagrams
- `CLAUDE_SETUP.md` - Setup instructions
