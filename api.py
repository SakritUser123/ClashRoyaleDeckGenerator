
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import httpx
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
from pydantic import BaseModel
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Clash Royale API", version="1.0.0")

CLASH_ROYALE_API_BASE = "https://api.clashroyale.com/v1"
API_TOKEN = os.getenv("CLASH_ROYALE_API_TOKEN", "")

if not API_TOKEN:
    print("⚠️  WARNING: CLASH_ROYALE_API_TOKEN not set. Set it in .env file or environment variables.")
    print("   Get your token from: https://developer.clashroyale.com/")

MOCK_PLAYER_DATA = {
    "tag": "#LUJY98PRC",
    "name": "DemoPlayer",
    "expLevel": 13,
    "trophies": 6500,
    "bestTrophies": 7200,
    "wins": 2150,
    "losses": 890,
    "cards": [
        {"name": "Hog Rider", "level": 13},
        {"name": "Royal Giant", "level": 11},
        {"name": "Goblin Barrel", "level": 13},
        {"name": "Fireball", "level": 13},
        {"name": "Musketeer", "level": 12},
        {"name": "Cannon", "level": 13},
        {"name": "Skeletons", "level": 13},
        {"name": "The Log", "level": 5}
    ],
    "clan": {"name": "Demo Clan", "tag": "#CLAN123"},
    "arena": {"name": "Legendary Arena"}
}

MOCK_BATTLE_LOG = [
    {"battleTime": "20250101T120000.000Z", "type": "PvP", "result": "win", "opponent": {"name": "Player1"}},
    {"battleTime": "20250101T100000.000Z", "type": "PvP", "result": "win", "opponent": {"name": "Player2"}},
    {"battleTime": "20250101T080000.000Z", "type": "PvP", "result": "loss", "opponent": {"name": "Player3"}},
    {"battleTime": "20250101T060000.000Z", "type": "PvP", "result": "win", "opponent": {"name": "Player4"}},
]

MOCK_CARDS = [
    {"name": "Hog Rider", "id": 26000001, "rarity": "Rare"},
    {"name": "Royal Giant", "id": 26000037, "rarity": "Rare"},
    {"name": "Goblin Barrel", "id": 27000030, "rarity": "Rare"},
    {"name": "Fireball", "id": 28000027, "rarity": "Rare"},
    {"name": "The Log", "id": 27000022, "rarity": "Legendary"},
    {"name": "Mega Knight", "id": 26000040, "rarity": "Legendary"},
]

class GetCardsResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None

class GetPlayerResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None

class GetPlayerBattlesResponse(BaseModel):
    success: bool
    data: Optional[list] = None
    error: Optional[str] = None

class LLMTool(BaseModel):
    type: str = "function"
    function: dict

def get_headers():
    return {
        "Content-Type": "application/json"
    }

async def make_api_request(endpoint: str):
    

    pass

@app.get("/")
async def root():
    
    return {
        "name": "Clash Royale AI API",
        "version": "1.0.0",
        "endpoints": [
            "/api/tools - Get LLM tools definition",
            "/api/cards - Get all cards",
            "/api/player/{playerTag} - Get player info",
            "/api/player/{playerTag}/battles - Get player battles"
        ]
    }

@app.get("/api/tools")
async def get_llm_tools():
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_clash_royale_cards",
                "description": "Get all available Clash Royale cards with their stats, abilities, and rarities",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_player_info",
                "description": "Get detailed information about a Clash Royale player including stats, cards, and achievements",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "playerTag": {
                            "type": "string",
                            "description": "The player tag (e.g., '#Y92P0L2'). Include the # symbol."
                        }
                    },
                    "required": ["playerTag"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_player_battles",
                "description": "Get recent battle history for a Clash Royale player",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "playerTag": {
                            "type": "string",
                            "description": "The player tag (e.g., '#Y92P0L2'). Include the # symbol."
                        }
                    },
                    "required": ["playerTag"]
                }
            }
        }
    ]
    return JSONResponse(content={"tools": tools})

@app.get("/api/cards")
async def get_cards() -> GetCardsResponse:
    
    try:
        if not API_TOKEN:
            return GetCardsResponse(success=False, error="API_TOKEN not configured. Set CLASH_ROYALE_API_TOKEN in .env")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{CLASH_ROYALE_API_BASE}/cards",
                headers={"Authorization": f"Bearer {API_TOKEN}"},
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return GetCardsResponse(success=True, data=data)
            else:
                return GetCardsResponse(success=False, error=f"API Error: {response.status_code} - {response.text}")
                
    except Exception as e:
        return GetCardsResponse(success=False, error=f"Error: {str(e)}")

@app.get("/api/player/{playerTag}")
async def get_player(playerTag: str) -> GetPlayerResponse:
    
    try:
        if not API_TOKEN:
            return GetPlayerResponse(success=False, error="API_TOKEN not configured. Set CLASH_ROYALE_API_TOKEN in .env")
        

        encoded_tag = playerTag.replace("#", "%23")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{CLASH_ROYALE_API_BASE}/players/{encoded_tag}",
                headers={"Authorization": f"Bearer {API_TOKEN}"},
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return GetPlayerResponse(success=True, data=data)
            elif response.status_code == 404:
                return GetPlayerResponse(success=False, error=f"Player {playerTag} not found")
            else:
                return GetPlayerResponse(success=False, error=f"API Error: {response.status_code} - {response.text}")
                
    except Exception as e:
        return GetPlayerResponse(success=False, error=f"Error: {str(e)}")

@app.get("/api/player/{playerTag}/battles")
async def get_player_battles(playerTag: str) -> GetPlayerBattlesResponse:
    
    try:
        if not API_TOKEN:
            return GetPlayerBattlesResponse(success=False, error="API_TOKEN not configured. Set CLASH_ROYALE_API_TOKEN in .env")
        

        encoded_tag = playerTag.replace("#", "%23")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{CLASH_ROYALE_API_BASE}/players/{encoded_tag}/battlelog",
                headers={"Authorization": f"Bearer {API_TOKEN}"},
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return GetPlayerBattlesResponse(success=True, data=data)
            elif response.status_code == 404:
                return GetPlayerBattlesResponse(success=False, error=f"Player {playerTag} not found")
            else:
                return GetPlayerBattlesResponse(success=False, error=f"API Error: {response.status_code} - {response.text}")
                
    except Exception as e:
        return GetPlayerBattlesResponse(success=False, error=f"Error: {str(e)}")

@app.post("/api/process-tool-call")
async def process_tool_call(tool_name: str = Query(...), tool_input: Optional[str] = Query(None)):
    
    try:
        import json

        if tool_input and isinstance(tool_input, str):
            parsed_input = json.loads(tool_input) if tool_input.strip() else {}
        else:
            parsed_input = tool_input or {}
        
        if tool_name == "get_clash_royale_cards":
            result = await get_cards()
            return JSONResponse(content=result.model_dump())
        
        elif tool_name == "get_player_info":
            playerTag = parsed_input.get("playerTag")
            if not playerTag:
                return JSONResponse(
                    content={"success": False, "error": "playerTag is required"},
                    status_code=400
                )
            result = await get_player(playerTag)
            return JSONResponse(content=result.model_dump())
        
        elif tool_name == "get_player_battles":
            playerTag = parsed_input.get("playerTag")
            if not playerTag:
                return JSONResponse(
                    content={"success": False, "error": "playerTag is required"},
                    status_code=400
                )
            result = await get_player_battles(playerTag)
            return JSONResponse(content=result.model_dump())
        
        else:
            return JSONResponse(
                content={"success": False, "error": f"Unknown tool: {tool_name}"},
                status_code=400
            )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=500
        )

@app.post("/api/llm/chat")
async def llm_chat(message: str = Query(...), player_tag: Optional[str] = Query(None)):
    
    try:
        from llm_integration import chat_with_llama
        
        if player_tag:
            message = f"{message}\n\nFocus on player: {player_tag}"
        

        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            response, tool_calls = await loop.run_in_executor(executor, chat_with_llama, message)
        
        return JSONResponse(content={
            "success": True,
            "response": response,
            "model": "Llama 3.3 70B (via Groq)",
            "tool_calls": tool_calls,
            "tools_used": len(tool_calls)
        })
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=500
        )

@app.post("/api/llm/analyze-player")
async def llm_analyze_player(player_tag: str = Query(...)):
    
    try:
        from llm_integration import analyze_player_for_deck_suggestion
        

        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            response = await loop.run_in_executor(executor, analyze_player_for_deck_suggestion, player_tag)
        
        return JSONResponse(content={
            "success": True,
            "player_tag": player_tag,
            "analysis": response
        })
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=500
        )

@app.post("/api/llm/compare-players")
async def llm_compare_players(player_tag1: str = Query(...), player_tag2: str = Query(...)):
    
    try:
        from llm_integration import compare_players
        

        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            response = await loop.run_in_executor(executor, compare_players, player_tag1, player_tag2)
        
        return JSONResponse(content={
            "success": True,
            "players": [player_tag1, player_tag2],
            "comparison": response
        })
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=500
        )

@app.get("/api/llm/card-analysis")
async def llm_card_analysis():
    
    try:
        from llm_integration import get_card_analysis
        

        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            response = await loop.run_in_executor(executor, get_card_analysis)
        
        return JSONResponse(content={
            "success": True,
            "analysis": response
        })
    except Exception as e:
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=500
        )

@app.get("/health")
async def health_check():
    
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
