# Architecture & Flow Diagrams

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLASH ROYALE AI SYSTEM                   │
└─────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER (Port 8501)            │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Streamlit Frontend (app.py)                         │  │
│  │  ┌──────────┬──────────┬─────────┬──────────────┐   │  │
│  │  │ Player   │   Card   │ Battle  │ AI Assistant │   │  │
│  │  │ Search   │   Info   │ History │ (NEW!)       │   │  │
│  │  └──────────┴──────────┴─────────┴──────────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
                           ↕ HTTP (requests)
┌────────────────────────────────────────────────────────────┐
│                    BUSINESS LAYER (Port 8000)               │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FastAPI Backend (api.py)                            │  │
│  │  ┌─────────────┬──────────────────┬──────────────┐  │  │
│  │  │  Data API   │  Tool Processing │  LLM Routes  │  │  │
│  │  │  endpoints  │  endpoints       │  (NEW!)      │  │  │
│  │  │             │                  │              │  │  │
│  │  │ • /cards    │ • /process-tool  │ • /chat      │  │  │
│  │  │ • /player   │   -call          │ • /analyze   │  │  │
│  │  │ • /battles  │                  │ • /compare   │  │  │
│  │  │ • /tools    │                  │ • /meta      │  │  │
│  │  └─────────────┴──────────────────┴──────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                         ↓ imports                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  LLM Integration (llm_integration.py) - NEW!          │  │
│  │  ┌──────────────────────────────────────────────────┐ │  │
│  │  │  chat_with_claude()                              │ │  │
│  │  │  - Sends user message                            │ │  │
│  │  │  - Defines 3 tools for Claude                    │ │  │
│  │  │  - Calls Anthropic API                           │ │  │
│  │  │  - Handles tool use responses                    │ │  │
│  │  │  - Returns analysis                              │ │  │
│  │  └──────────────────────────────────────────────────┘ │  │
│  │                      ↕ HTTP                            │  │
│  │  ┌──────────────────────────────────────────────────┐ │  │
│  │  │  Tool Execution (back to /process-tool-call)    │ │  │
│  │  │  - get_clash_royale_cards()                      │ │  │
│  │  │  - get_player_info()                             │ │  │
│  │  │  - get_player_battles()                          │ │  │
│  │  └──────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
                    ↓ HTTP (httpx)        ↓ HTTP (httpx)
        ┌──────────────────────┐  ┌──────────────────────┐
        │  Anthropic API       │  │  Clash Royale API    │
        │  (Claude models)     │  │  (Card/Player data)  │
        └──────────────────────┘  └──────────────────────┘
```

## 🔄 Claude LLM Invocation Flow

```
USER INPUT (Streamlit)
        │
        ↓
    ┌────────────────────────────────────────┐
    │ Streamlit sends HTTP POST to FastAPI   │
    │ /api/llm/chat                          │
    │ /api/llm/analyze-player                │
    │ /api/llm/compare-players               │
    │ /api/llm/card-analysis                 │
    └────────────────────────────────────────┘
        │
        ↓
    ┌────────────────────────────────────────┐
    │ FastAPI endpoint function              │
    │ Calls llm_integration.py functions     │
    └────────────────────────────────────────┘
        │
        ↓
    ┌────────────────────────────────────────┐
    │ chat_with_claude(message)              │
    │ Sets up system prompt & message list   │
    └────────────────────────────────────────┘
        │
        ↓
    ╔════════════════════════════════════════╗
    ║  client.messages.create(               ║
    ║    model="claude-3-5-sonnet-...",      ║
    ║    system=system_prompt,               ║
    ║    tools=CLASH_ROYALE_TOOLS,  ←────┐  ║
    ║    messages=messages                   ║
    ║  )                                     ║
    ║  🎯 CLAUDE IS INVOKED HERE!            ║
    ╚════════════════════════════════════════╝
        │
        ↓
    ┌────────────────────────────────────────┐
    │ Claude receives:                       │
    │ - User question                        │
    │ - System prompt (behavior guide)       │
    │ - 3 available tools:                   │
    │   • get_clash_royale_cards             │
    │   • get_player_info                    │
    │   • get_player_battles                 │
    └────────────────────────────────────────┘
        │
        ↓
    ┌────────────────────────────────────────┐
    │ Claude decides: "I need tools"         │
    │ response.stop_reason = "tool_use"      │
    └────────────────────────────────────────┘
        │
        ↓
    ┌────────────────────────────────────────┐
    │ Extract tool calls from response:      │
    │ [                                      │
    │   {tool: "get_player_info",            │
    │    input: {playerTag: "#Y92P0L2"}},    │
    │   {tool: "get_player_battles",         │
    │    input: {playerTag: "#Y92P0L2"}},    │
    │   ...                                  │
    │ ]                                      │
    └────────────────────────────────────────┘
        │
        ↓
    ┌────────────────────────────────────────┐
    │ For each tool call:                    │
    │ call process_tool_call(tool_name,      │
    │                        tool_input)     │
    └────────────────────────────────────────┘
        │
        ├─→ get_player_info() → Clash Royale API
        │
        ├─→ get_player_battles() → Clash Royale API
        │
        └─→ get_clash_royale_cards() → Clash Royale API
        │
        ↓
    ┌────────────────────────────────────────┐
    │ Collect all tool results:              │
    │ [                                      │
    │   {tool_id: "123", result: {...}},     │
    │   {tool_id: "456", result: {...}},     │
    │   ...                                  │
    │ ]                                      │
    └────────────────────────────────────────┘
        │
        ↓
    ┌────────────────────────────────────────┐
    │ Send results back to Claude:           │
    │ messages.append({                      │
    │   "role": "user",                      │
    │   "content": [tool results]            │
    │ })                                     │
    │                                        │
    │ Re-call client.messages.create()       │
    │ 🎯 CLAUDE IS INVOKED AGAIN!            │
    └────────────────────────────────────────┘
        │
        ↓
    ┌────────────────────────────────────────┐
    │ Claude analyzes tool results           │
    │ response.stop_reason = "end_turn"      │
    │ Generates final response                │
    └────────────────────────────────────────┘
        │
        ↓
    ┌────────────────────────────────────────┐
    │ Return from chat_with_claude():        │
    │ (final_response, tool_calls_made)      │
    └────────────────────────────────────────┘
        │
        ↓
    ┌────────────────────────────────────────┐
    │ FastAPI returns JSON response:         │
    │ {                                      │
    │   "success": true,                     │
    │   "response": "Based on the data...",  │
    │   "tool_calls": [...],                 │
    │   "tools_used": 3                      │
    │ }                                      │
    └────────────────────────────────────────┘
        │
        ↓
    ┌────────────────────────────────────────┐
    │ Streamlit displays response            │
    │ Shows Claude's analysis                │
    │ Shows tools used (expandable)          │
    └────────────────────────────────────────┘
        │
        ↓
    USER SEES RESULT
```

## 🎯 Tool Use Sequence

```
┌─────────────────────┐
│  User Question:     │
│  "Analyze player    │
│   #Y92P0L2"         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────────────┐
│  Claude Thought Process:                    │
│  "To analyze this player, I need:           │
│   1. Their profile info (trophies, level)   │
│   2. Their recent battles                   │
│   3. Card information (to understand deck)  │
│                                              │
│   I'll use all 3 available tools"           │
└─────────────────────┬───────────────────────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │Tool Call:│ │Tool Call:│ │Tool Call:│
    │get_player│ │get_player│ │get_clash │
    │_info     │ │_battles  │ │_royale   │
    │          │ │          │ │_cards    │
    │Input:    │ │Input:    │ │          │
    │playerTag:│ │playerTag:│ │No params │
    │#Y92P0L2  │ │#Y92P0L2  │ │          │
    └────┬─────┘ └────┬─────┘ └────┬─────┘
         │            │            │
         ▼            ▼            ▼
    ┌──────────────────────────────────┐
    │  Execute via FastAPI             │
    │  /api/process-tool-call          │
    └──────────────────────────────────┘
         │            │            │
         ▼            ▼            ▼
    ┌──────────────────────────────────┐
    │  Clash Royale API Calls          │
    │  (via httpx)                     │
    └──────────────────────────────────┘
         │            │            │
         ▼            ▼            ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │Player    │ │Battles   │ │All Cards │
    │Data:     │ │Data:     │ │Data:     │
    │- name    │ │- 20 games│ │- 100+    │
    │- trophies│ │- results │ │  cards   │
    │- level   │ │- decks   │ │- stats   │
    │- cards   │ │- opponents
    │- stats   │ │- replay  │
    └────┬─────┘ └────┬─────┘ └────┬─────┘
         │            │            │
         └────────────┼────────────┘
                      │
                      ▼
    ┌─────────────────────────────────────┐
    │  Send all results back to Claude    │
    └────────────┬────────────────────────┘
                 │
                 ▼
    ┌─────────────────────────────────────┐
    │  Claude Analyzes:                   │
    │  - Player is level 12, 5000 trophies
    │  - 60% win rate (12 wins, 8 losses)
    │  - Uses Hog Rider + Tornado deck
    │  - Strong at countering ground swarm
    │  - Weak to air-based decks         │
    │                                     │
    │  Final Response:                    │
    │  "Player #Y92P0L2 is a skilled...   │
    │   Based on their battles, I suggest │
    │   adding... The meta suggests..."   │
    └─────────────────────────────────────┘
```

## 📊 Code Flow Diagram

```
app.py (Streamlit)
    │
    └─→ User clicks "Analyze Player"
        │
        └─→ requests.post(
            f"{API_BASE_URL}/api/llm/analyze-player",
            params={"player_tag": "#Y92P0L2"}
        )
            │
            ▼
api.py (FastAPI)
    │
    └─→ @app.post("/api/llm/analyze-player")
        async def llm_analyze_player(player_tag: str):
            │
            └─→ from llm_integration import analyze_player_for_deck_suggestion
                response = analyze_player_for_deck_suggestion(player_tag)
                    │
                    ▼
llm_integration.py
    │
    └─→ def analyze_player_for_deck_suggestion(player_tag: str):
        user_message = f"Please analyze player {player_tag}..."
        response, tool_calls = chat_with_claude(user_message)
            │
            └─→ def chat_with_claude(user_message: str, system_prompt: str):
                messages = [{"role": "user", "content": user_message}]
                    │
                    └─→ while True:
                        response = client.messages.create(  ◄─── CLAUDE INVOKED HERE!
                            model="claude-3-5-sonnet-20241022",
                            max_tokens=2048,
                            system=system_prompt,
                            tools=CLASH_ROYALE_TOOLS,
                            messages=messages
                        )
                            │
                            ├─→ if response.stop_reason == "tool_use":
                            │   │
                            │   └─→ for block in response.content:
                            │       if block.type == "tool_use":
                            │           tool_result = process_tool_call(
                            │               block.name,
                            │               block.input
                            │           )
                            │               │
                            │               └─→ requests to /api/process-tool-call
                            │                   (back to api.py)
                            │
                            └─→ else:  # Claude done with tools
                                final_response = extract_text(response)
                                return (final_response, tool_calls_made)
                    │
                    ▼
Returns to api.py
    │
    └─→ return JSONResponse({
            "success": True,
            "player_tag": player_tag,
            "analysis": response
        })
            │
            ▼
Returns to app.py
    │
    └─→ st.markdown(result.get("analysis", ""))
        (Display to user)
```

## 🔌 API Endpoint Hierarchy

```
FastAPI (api.py)
│
├── Data Endpoints
│   ├── GET /api/cards
│   ├── GET /api/player/{playerTag}
│   ├── GET /api/player/{playerTag}/battles
│   └── GET /api/tools
│
├── Tool Processing
│   └── POST /api/process-tool-call
│       (Called by llm_integration.py)
│
├── LLM Endpoints (NEW!) ⭐
│   ├── POST /api/llm/chat
│   │   └─→ llm_integration.py
│   │       └─→ chat_with_claude()
│   │           └─→ Anthropic API
│   │
│   ├── POST /api/llm/analyze-player
│   │   └─→ llm_integration.py
│   │       └─→ analyze_player_for_deck_suggestion()
│   │           └─→ chat_with_claude()
│   │               └─→ Anthropic API
│   │
│   ├── POST /api/llm/compare-players
│   │   └─→ llm_integration.py
│   │       └─→ compare_players()
│   │           └─→ chat_with_claude()
│   │               └─→ Anthropic API
│   │
│   └── GET /api/llm/card-analysis
│       └─→ llm_integration.py
│           └─→ get_card_analysis()
│               └─→ chat_with_claude()
│                   └─→ Anthropic API
│
└── Health
    └── GET /health
```

---

**Key Insight:** Claude is invoked via `client.messages.create()` in `llm_integration.py`, which is called from FastAPI endpoints, which are called from Streamlit UI. ✨
