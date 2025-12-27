# Where Claude (GPT Model) is Invoked

## 🎯 The Exact Location

**File:** `/Users/kavithakesavalu/clashRoyaleAI/llm_integration.py`

**Function:** `chat_with_claude(user_message: str, system_prompt: Optional[str] = None)`

## 📍 Line-by-Line Breakdown

### 1. Initialize Anthropic Client (Top of file)
```python
import anthropic

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
```
**What:** Creates the Claude API client using your API key

### 2. Define Tools for Claude (Line ~35)
```python
CLASH_ROYALE_TOOLS = [
    {
        "name": "get_clash_royale_cards",
        "description": "Get all available Clash Royale cards...",
        "input_schema": {...}
    },
    # ... more tools
]
```
**What:** Defines 3 tools Claude can choose to use

### 3. The Main Function (Line ~100)
```python
def chat_with_claude(user_message: str, system_prompt: Optional[str] = None) -> tuple[str, list]:
    """Send a message to Claude with access to Clash Royale tools."""
    
    # Set system prompt if not provided
    if system_prompt is None:
        system_prompt = """You are a helpful Clash Royale AI assistant..."""

    messages = [{"role": "user", "content": user_message}]
```
**What:** Sets up the conversation context

### 4. THE CRUCIAL PART - Claude API Call (Line ~115)
```python
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",      # 👈 THE LLM MODEL
    max_tokens=2048,
    system=system_prompt,
    tools=CLASH_ROYALE_TOOLS,                 # 👈 TOOLS AVAILABLE
    messages=messages
)
```

**EXPLANATION:**
- `model`: Which Claude model to use
- `system`: The system prompt (tells Claude how to behave)
- `tools`: The 3 tools Claude can automatically use
- `messages`: The conversation history

### 5. Handle Tool Use (Line ~120)
```python
if response.stop_reason == "tool_use":
    # Claude wants to use a tool
    for block in response.content:
        if block.type == "tool_use":
            tool_name = block.name        # Which tool?
            tool_input = block.input      # With what parameters?
            tool_use_id = block.id
            
            # Call the actual tool
            tool_result = process_tool_call(tool_name, tool_input)
```
**What:** When Claude decides to use a tool, we execute it

### 6. Send Results Back to Claude (Line ~145)
```python
messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user", "content": tool_results})
```
**What:** Claude sees the tool results and can use more tools if needed

### 7. Continue Until Done (Line ~150)
```python
else:
    # Claude is done using tools, extract final response
    final_response = ""
    for block in response.content:
        if hasattr(block, "text"):
            final_response += block.text
    
    return final_response, tool_calls_made
```
**What:** Return the final answer to the user

## 🔄 Complete Flow Diagram

```
┌─────────────────────────────────────────────────────┐
│ 1. user calls chat_with_claude("Analyze player X")  │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│ 2. client.messages.create(                           │
│      model="claude-3-5-sonnet-20241022",             │
│      tools=CLASH_ROYALE_TOOLS,                       │
│      messages=...                                    │
│    )                                                  │
│ → SENDS REQUEST TO ANTHROPIC API                     │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│ 3. Claude receives request + tools definition        │
│    Claude thinks: "I need get_player_info and        │
│                   get_player_battles"                │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│ 4. Claude returns response.stop_reason == "tool_use" │
│    response.content = [ToolUseBlock(...), ...]       │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│ 5. We extract tool calls:                            │
│    - tool_name: "get_player_info"                    │
│    - tool_input: {"playerTag": "#Y92P0L2"}           │
│                                                       │
│    - tool_name: "get_player_battles"                 │
│    - tool_input: {"playerTag": "#Y92P0L2"}           │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│ 6. Call process_tool_call() for each:                │
│    → Calls FastAPI /api/process-tool-call            │
│    → Gets results from Clash Royale API              │
│    → Returns results to Claude                       │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│ 7. Send tool results back to Claude:                 │
│    messages.append({                                 │
│      "role": "user",                                 │
│      "content": [tool results]                       │
│    })                                                │
│                                                       │
│    Re-call client.messages.create() with results     │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│ 8. Claude processes results and responds:            │
│    stop_reason = "end_turn"                          │
│    Final response = "Based on the player's data..."  │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│ 9. Return to caller:                                 │
│    (final_response, list_of_tool_calls_made)         │
└─────────────────────────────────────────────────────┘
```

## 📍 Where Each Function is Called

### `chat_with_claude()`
**Called from these FastAPI endpoints:**

```python
# api.py - Line ~192
@app.post("/api/llm/chat")
async def llm_chat(message: str, player_tag: Optional[str] = None):
    response, tool_calls = chat_with_claude(message)  # ← HERE

# api.py - Line ~216
@app.post("/api/llm/analyze-player")
async def llm_analyze_player(player_tag: str):
    response = analyze_player_for_deck_suggestion(player_tag)
    # Which calls chat_with_claude internally

# api.py - Line ~234
@app.post("/api/llm/compare-players")
async def llm_compare_players(player_tag1: str, player_tag2: str):
    response = compare_players(player_tag1, player_tag2)
    # Which calls chat_with_claude internally

# api.py - Line ~252
@app.get("/api/llm/card-analysis")
async def llm_card_analysis():
    response = get_card_analysis()
    # Which calls chat_with_claude internally
```

### FastAPI endpoints
**Called from Streamlit UI:**

```python
# app.py - Line ~235
response = requests.post(
    f"{API_BASE_URL}/api/llm/chat",
    params={"message": user_message},  # ← SENDS TO FASTAPI
)

# app.py - Line ~290
response = requests.post(
    f"{API_BASE_URL}/api/llm/analyze-player",
    params={"player_tag": tag},  # ← SENDS TO FASTAPI
)

# Similar for compare and meta analysis
```

## 🔑 Key Models/Methods

**Claude Model Used:**
```
claude-3-5-sonnet-20241022
```

**The critical method call:**
```python
client.messages.create(
    model="...",
    tools=CLASH_ROYALE_TOOLS,
    messages=[...],
    system=system_prompt,
    max_tokens=2048
)
```

This is the **Anthropic Messages API** with tool use extension.

## 📊 Summary

| Component | Location | Purpose |
|-----------|----------|---------|
| **Anthropic Client** | llm_integration.py:10 | Connects to Claude |
| **Tools Definition** | llm_integration.py:17 | What tools Claude can use |
| **Main Function** | llm_integration.py:100 | Orchestrates conversation |
| **Claude API Call** | llm_integration.py:115 | Sends request to Claude |
| **Tool Use Handling** | llm_integration.py:120 | Executes tools Claude requests |
| **FastAPI Endpoints** | api.py:192,216,234,252 | Expose Claude features to web |
| **Streamlit UI** | app.py:235,290+ | User interface for Claude |

## 🚀 To Run

```bash
# Terminal 1
export ANTHROPIC_API_KEY='your_key'
export CLASH_ROYALE_API_TOKEN='your_token'
python3 api.py

# Terminal 2
streamlit run app.py
```

Then go to: http://localhost:8501 → "AI Assistant" tab

---

**Claude is invoked here:** `llm_integration.py` → `chat_with_claude()` → `client.messages.create()` 🚀
