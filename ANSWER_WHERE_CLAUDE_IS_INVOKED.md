# ⭐ THE ANSWER: Where Claude (GPT Model) is Invoked

## 🎯 Direct Answer

**Claude is invoked in:** `llm_integration.py` → `chat_with_claude()` function → `client.messages.create()`

**Exact Line:** ~115 in `llm_integration.py`

```python
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",  # ← This is the Claude model
    max_tokens=2048,
    system=system_prompt,
    tools=CLASH_ROYALE_TOOLS,            # ← With these 3 tools available
    messages=messages                    # ← And this conversation history
)
# 🎯 CLAUDE IS CALLED HERE
```

## 📍 Call Stack

```
Streamlit UI (app.py)
    ↓ User clicks button
requests.post("/api/llm/chat")
    ↓ HTTP to FastAPI
FastAPI handler (api.py line 192+)
    ↓ Calls function
llm_integration.chat_with_claude()
    ↓ Creates API request
Anthropic client.messages.create()
    ↓ 🎯 CLAUDE IS HERE
```

## 🔑 Key Code Section

**File:** `llm_integration.py`

**Function:** `chat_with_claude()` (starts ~line 100)

**The Invocation:**
```python
def chat_with_claude(user_message: str, system_prompt: Optional[str] = None) -> tuple[str, list]:
    # ... setup code ...
    
    messages = [{"role": "user", "content": user_message}]
    tool_calls_made = []
    
    # This is the agentic loop
    while True:
        # 🎯 CLAUDE API CALL - HERE IS WHERE CLAUDE IS INVOKED:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",     # Claude model
            max_tokens=2048,
            system=system_prompt,
            tools=CLASH_ROYALE_TOOLS,              # 3 tools available
            messages=messages
        )
        
        # Process Claude's response...
        if response.stop_reason == "tool_use":
            # Claude wants to use tools
            for block in response.content:
                if block.type == "tool_use":
                    # Execute the tool Claude requested
                    tool_result = process_tool_call(block.name, block.input)
                    # Send back to Claude...
        else:
            # Claude is done, return final response
            return final_response, tool_calls_made
```

## 🚀 How to Find It

**Step 1:** Open `llm_integration.py`
**Step 2:** Look for: `client.messages.create(`
**Step 3:** That's where Claude is invoked!

## 📊 The Tools Claude Can Use

When Claude is invoked, it has access to 3 tools:

```python
CLASH_ROYALE_TOOLS = [
    {
        "name": "get_clash_royale_cards",
        "description": "Get all available Clash Royale cards..."
    },
    {
        "name": "get_player_info",
        "description": "Get detailed player information..."
    },
    {
        "name": "get_player_battles",
        "description": "Get recent battle history..."
    }
]
```

Claude automatically decides which tools to use based on the user's question.

## 🎯 Example

**User asks:** "Analyze player #Y92P0L2"

**What happens:**
1. Streamlit calls FastAPI endpoint
2. FastAPI calls `chat_with_claude()`
3. `chat_with_claude()` calls `client.messages.create()`
4. **Claude is invoked** with the user's message + 3 tools
5. Claude thinks: "I need player info, battles, and cards"
6. Claude calls all 3 tools
7. Results come back to Claude
8. Claude analyzes and responds
9. Response returned to Streamlit

## 💡 Key Points

✅ **Model:** `claude-3-5-sonnet-20241022` (Anthropic's Claude)

✅ **SDK:** `anthropic` Python package

✅ **Method:** `client.messages.create()` with `tools` parameter

✅ **Tool Use:** Claude automatically decides which tools to use

✅ **Location:** `llm_integration.py` line ~115

✅ **Called From:** FastAPI endpoints in `api.py`

✅ **UI:** Streamlit UI in `app.py`

## 🔍 Files to Look At

| File | Purpose | Claude Invocation |
|------|---------|-------------------|
| `llm_integration.py` | LLM integration | YES - `client.messages.create()` |
| `api.py` | FastAPI backend | No - calls llm_integration |
| `app.py` | Streamlit UI | No - calls FastAPI |

## 📚 Documentation

- **Quick Start:** `CLAUDE_SETUP.md`
- **Detailed:** `WHERE_CLAUDE_INVOKED.md`
- **Complete:** `LLM_INTEGRATION.md`
- **Architecture:** `ARCHITECTURE.md`

## ✨ Summary

Claude (Anthropic's GPT model) is invoked in `llm_integration.py` using the Anthropic Python SDK:

```python
client.messages.create(
    model="claude-3-5-sonnet-20241022",
    tools=CLASH_ROYALE_TOOLS,
    messages=messages,
    system=system_prompt,
    max_tokens=2048
)
```

This happens automatically when:
1. User uses the AI Assistant tab in Streamlit
2. FastAPI endpoint calls a function from `llm_integration.py`
3. Function calls `chat_with_claude()` 
4. `chat_with_claude()` invokes Claude via the Anthropic API

**That's it!** Simple, clean, and powerful. 🚀
