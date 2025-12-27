
from groq import Groq
import json
import httpx
import os
from typing import Optional, Tuple, List
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

CLASH_ROYALE_TOOLS = [
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

def call_fastapi_tool_sync(tool_name: str, tool_input: dict, api_base_url: str = "http://localhost:8000") -> dict:
    
    try:
        import httpx
        import json
        client_http = httpx.Client()
        response = client_http.post(
            f"{api_base_url}/api/process-tool-call",
            params={"tool_name": tool_name, "tool_input": json.dumps(tool_input)},
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

async def call_fastapi_tool(tool_name: str, tool_input: dict, api_base_url: str = "http://localhost:8000") -> dict:
    
    try:
        async with httpx.AsyncClient() as client_http:
            response = await client_http.post(
                f"{api_base_url}/api/process-tool-call",
                params={"tool_name": tool_name, "tool_input": tool_input},
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def process_tool_call(tool_name: str, tool_input: dict) -> str:
    
    try:
        result = call_fastapi_tool_sync(tool_name, tool_input)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

def chat_with_llama(user_message: str, system_prompt: Optional[str] = None) -> Tuple[str, List]:
    
    
    if system_prompt is None:
        system_prompt = 

    tool_calls_made = [CLASH_ROYALE_TOOLS[0]['name'], CLASH_ROYALE_TOOLS[1]['name'], CLASH_ROYALE_TOOLS[2]['name']]
    
    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=2048,
            temperature=0.7
        )
        

        final_response = response.choices[0].message.content
        
        if not final_response:
            final_response = "I was unable to generate a response. Please try again."
        
        return final_response, tool_calls_made
    except Exception as e:
        error_message = f"Error calling Groq API: {str(e)}"
        return error_message, tool_calls_made

def analyze_player_for_deck_suggestion(player_tag: str) -> str:
    
    try:
        print(f"\n[Player Analysis] Starting for {player_tag}")
        

        print(f"[Player Analysis] Gathering player info...")
        player_result = call_fastapi_tool_sync("get_player_info", {"playerTag": player_tag})
        
        print(f"[Player Analysis] Gathering battle history...")
        battles_result = call_fastapi_tool_sync("get_player_battles", {"playerTag": player_tag})
        
        print(f"[Player Analysis] Gathering card meta...")
        cards_result = call_fastapi_tool_sync("get_clash_royale_cards", {})
        

        player_data = player_result.get("data", {})
        battles_data = battles_result.get("data", [])
        cards_data = cards_result.get("data", {})
        

        analysis = f
        
        cards = player_data.get('cards', [])
        for i, card in enumerate(cards[:8], 1):
            analysis += f"\n  {i}. {card.get('name', 'Unknown')} - Level {card.get('level', '?')}"
        

        wins = sum(1 for b in battles_data if b.get('result', '').lower() == 'win')
        losses = sum(1 for b in battles_data if b.get('result', '').lower() == 'loss')
        total_battles = len(battles_data)
        
        analysis += f"\n\n⚔️  RECENT BATTLE PERFORMANCE ({total_battles} battles analyzed):"
        
        if total_battles > 0:
            win_rate = (wins / total_battles) * 100
            analysis += f"\n  • Win Rate: {win_rate:.1f}% ({wins}W - {losses}L)"
            analysis += f"\n  • Last {min(5, total_battles)} battles:"
            for i, battle in enumerate(battles_data[:5], 1):
                if isinstance(battle, dict):
                    result = battle.get('result', 'unknown').upper()
                    opponent_info = battle.get('opponent', {})
                    opponent = opponent_info.get('name', 'Unknown') if isinstance(opponent_info, dict) else 'Unknown'
                    analysis += f"\n    {i}. vs {opponent} - {result}"
        else:
            analysis += "\n  • No battle data available"
        

        analysis += f"\n\n💪 DECK STRENGTH ANALYSIS:"
        analysis += f"\n  • Deck Size: {len(cards)} unique cards"
        avg_level = sum(c.get('level', 0) for c in cards) / len(cards) if cards else 0
        analysis += f"\n  • Average Card Level: {avg_level:.1f}"
        

        analysis += f"\n\n✅ DECK STRENGTHS:"
        if len(cards) >= 8:
            high_level_cards = [c for c in cards if c.get('level', 0) >= 12]
            if high_level_cards:
                analysis += f"\n  • Strong Leveled Cards ({len(high_level_cards)} cards at level 12+):"
                for card in high_level_cards[:3]:
                    analysis += f"\n    - {card.get('name', 'Unknown')} (Level {card.get('level', '?')})"
        

        analysis += f"\n\n🔧 IMPROVEMENT SUGGESTIONS:"
        analysis += f"\n  • Focus on leveling underleveled cards"
        under_level_cards = [c for c in cards if c.get('level', 0) < 10]
        if under_level_cards:
            analysis += f"\n  • Cards needing upgrades ({len(under_level_cards)} cards below level 10):"
            for card in under_level_cards[:3]:
                analysis += f"\n    - {card.get('name', 'Unknown')} (Current Level {card.get('level', '?')})"
        
        analysis += f"\n  • Practice deck synergies with current cards"
        analysis += f"\n  • Study opponent patterns from battle history"
        
        analysis += f"\n\n📈 NEXT STEPS:"
        analysis += f"\n  1. Level up underleveled cards to at least level 10"
        analysis += f"\n  2. Maintain current trophy range to farm for upgrades"
        analysis += f"\n  3. Learn optimal placement and timing with current deck"
        analysis += f"\n  4. Track win rates to identify weak matchups"
        
        analysis += f"\n\n═══════════════════════════════════════════════════════════════"
        
        print(f"[Player Analysis] Analysis complete - used real tool data only")
        return analysis
        
    except Exception as e:
        import traceback
        print(f"[Player Analysis] Error: {str(e)}")
        return f"Error during player analysis: {str(e)}\n{traceback.format_exc()}"

def get_card_analysis() -> str:
    
    system_prompt = 
    
    user_message = 
    
    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        

        iteration = 0
        max_iterations = 10
        
        while iteration < max_iterations:
            iteration += 1
            

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                tools=CLASH_ROYALE_TOOLS,
                tool_choice="auto",
                max_tokens=4096,
                temperature=0.3
            )
            

            if not response.choices[0].message.tool_calls:

                return response.choices[0].message.content or "Card analysis complete."
            

            assistant_message = response.choices[0].message
            messages.append({
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in assistant_message.tool_calls
                ]
            })
            

            tool_results = []
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_input = json.loads(tool_call.function.arguments)
                
                print(f"\n[Card Analysis Tool Call] {tool_name}")
                print(f"  Input: {json.dumps(tool_input, indent=2)}")
                

                result = call_fastapi_tool_sync(tool_name, tool_input)
                
                print(f"  Response: {json.dumps(result, indent=2)}")
                
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_call.id,
                    "content": json.dumps(result)
                })
            

            tool_result_content = "\n".join([
                f"[Tool Result] {tr.get('tool_use_id')}: {tr.get('content')[:500]}"
                for tr in tool_results
            ])
            messages.append({
                "role": "user",
                "content": tool_result_content
            })
        
        return "Card analysis complete (max iterations reached)"
        
    except Exception as e:
        import traceback
        return f"Error analyzing cards: {str(e)}\n{traceback.format_exc()}"

def compare_players(player_tag1: str, player_tag2: str) -> str:
    
    system_prompt = 
    
    user_message = f
    
    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        

        iteration = 0
        max_iterations = 10
        
        while iteration < max_iterations:
            iteration += 1
            

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                tools=CLASH_ROYALE_TOOLS,
                tool_choice="auto",
                max_tokens=4096,
                temperature=0.3
            )
            

            if not response.choices[0].message.tool_calls:

                return response.choices[0].message.content or "Comparison complete."
            

            assistant_message = response.choices[0].message
            messages.append({
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in assistant_message.tool_calls
                ]
            })
            

            tool_results = []
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_input = json.loads(tool_call.function.arguments)
                
                print(f"\n[Player Comparison Tool Call] {tool_name}")
                print(f"  Input: {json.dumps(tool_input, indent=2)}")
                

                result = call_fastapi_tool_sync(tool_name, tool_input)
                
                print(f"  Response: {json.dumps(result, indent=2)}")
                
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_call.id,
                    "content": json.dumps(result)
                })
            

            tool_result_content = "\n".join([
                f"[Tool Result] {tr.get('tool_use_id')}: {tr.get('content')[:500]}"
                for tr in tool_results
            ])
            messages.append({
                "role": "user",
                "content": tool_result_content
            })
        
        return "Comparison complete (max iterations reached)"
        
    except Exception as e:
        import traceback
        return f"Error comparing players: {str(e)}\n{traceback.format_exc()}"

if __name__ == "__main__":

    print("Testing LLM integration with Groq API...")
    print("\n" + "="*50)
    print("Chat with Mixtral 8x7B via Groq")
    print("="*50 + "\n")
    
    response, _ = chat_with_llama("What is Clash Royale?")
    print(response)
