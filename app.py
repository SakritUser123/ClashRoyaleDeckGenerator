import streamlit as st
import time
from urllib.request import urlopen
from urllib.parse import quote
from PIL import Image
import requests
import json

st.set_page_config(page_title="Clash Royale App", layout="centered")

API_BASE_URL = "http://localhost:8000"

splash = st.empty()

with splash.container():
    st.markdown(, unsafe_allow_html=True)

time.sleep(3.5)

splash.empty()

st.header("Clash Royale Deck Generator AI")

tab1, tab2, tab3, tab4 = st.tabs(["Player Search", "Card Info", "Battle History", "AI Assistant"])

with tab1:
    st.subheader("Search Player")
    playerID = st.text_input("Enter Player ID (with or without #):", key="player_search")
    
    if st.button("Get Player Info"):
        if playerID:
            try:

                tag = playerID if playerID.startswith("#") else f"#{playerID}"

                encoded_tag = quote(tag, safe='')
                
                with st.spinner("Fetching player data..."):
                    response = requests.get(
                        f"{API_BASE_URL}/api/player/{encoded_tag}",
                        timeout=10
                    )
                    response.raise_for_status()
                    result = response.json()
                
                if result.get("success"):
                    player_data = result.get("data", {})
                    st.success("✅ Player found!")
                    

                    st.session_state.player_data = player_data
                    st.session_state.current_player_tag = tag
                    

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Name", player_data.get("name", "N/A"))
                    with col2:
                        st.metric("Trophies", player_data.get("trophies", "N/A"))
                    with col3:
                        st.metric("Level", player_data.get("expLevel", "N/A"))
                    

                    col4, col5, col6 = st.columns(3)
                    with col4:
                        st.metric("Wins", player_data.get("wins", "N/A"))
                    with col5:
                        st.metric("Losses", player_data.get("losses", "N/A"))
                    with col6:
                        st.metric("Clan", player_data.get("clan", {}).get("name", "N/A"))
                    

                    try:
                        with st.spinner("Fetching battle history..."):
                            battle_response = requests.get(
                                f"{API_BASE_URL}/api/player/{encoded_tag}/battles",
                                timeout=10
                            )
                            battle_response.raise_for_status()
                            battle_result = battle_response.json()
                        
                        if battle_result.get("success"):
                            battles = battle_result.get("data", [])
                            st.session_state.battle_history = battles
                            st.session_state.player_tag = tag
                            
                            if battles:
                                st.markdown("### Recent Battles")
                                battle_list = []
                                for i, battle in enumerate(battles, 1):

                                    if isinstance(battle, dict):
                                        battle_type = battle.get("type", "Unknown")
                                        battle_result = battle.get("result", "unknown")
                                        opponent_info = battle.get("opponent", {})
                                        opponent_name = opponent_info.get("name", "Unknown") if isinstance(opponent_info, dict) else "Unknown"
                                    else:
                                        battle_type = "Unknown"
                                        battle_result = "unknown"
                                        opponent_name = "Unknown"
                                    
                                    battle_list.append({
                                        "#": i,
                                        "Type": battle_type,
                                        "Result": f"{'🟢 Win' if battle_result == 'win' else '🔴 Loss'}",
                                        "Opponent": opponent_name,
                                    })
                                
                                st.dataframe(
                                    data=battle_list,
                                    use_container_width=True,
                                    hide_index=True
                                )
                    except Exception as e:
                        st.warning(f"Could not fetch battle history: {str(e)}")
                    

                    with st.expander("View Full Player Data"):
                        st.json(player_data)
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection error: {str(e)}")
                st.info("💡 Make sure the FastAPI backend is running on port 8000")
        else:
            st.warning("Please enter a player ID")

with tab2:
    st.subheader("All Clash Royale Cards")
    
    if st.button("Load Cards"):
        try:
            with st.spinner("Fetching card data..."):
                response = requests.get(
                    f"{API_BASE_URL}/api/cards",
                    timeout=10
                )
                response.raise_for_status()
                result = response.json()
            
            if result.get("success"):
                cards_data = result.get("data", {})
                

                if isinstance(cards_data, list):
                    cards = cards_data
                elif isinstance(cards_data, dict) and "items" in cards_data:
                    cards = cards_data["items"]
                else:
                    cards = cards_data
                
                if isinstance(cards, list):
                    st.success(f"✅ Loaded {len(cards)} cards")
                    

                    if cards and isinstance(cards[0], dict) and "rarity" in cards[0]:
                        rarities = sorted(set(card.get("rarity", "Unknown") for card in cards))
                        selected_rarity = st.selectbox("Filter by rarity:", ["All"] + rarities)
                        
                        if selected_rarity != "All":
                            cards = [c for c in cards if c.get("rarity") == selected_rarity]
                    

                    st.dataframe(
                        data=cards,
                        use_container_width=True,
                        height=400
                    )
                else:
                    st.json(cards)
            else:
                st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Connection error: {str(e)}")
            st.info("💡 Make sure the FastAPI backend is running on port 8000")

with tab3:
    st.subheader("Player Battle History")
    playerID_battles = st.text_input("Enter Player ID (with or without #):", key="battle_search")
    
    if st.button("Get Battle History"):
        if playerID_battles:
            try:

                tag_display = playerID_battles if playerID_battles.startswith("#") else f"#{playerID_battles}"
                tag_api = playerID_battles.lstrip("#")
                
                with st.spinner("Fetching battle history..."):
                    response = requests.get(
                        f"{API_BASE_URL}/api/player/{tag_api}/battles",
                        timeout=10
                    )
                    response.raise_for_status()
                    result = response.json()
                
                if result.get("success"):
                    battles_data = result.get("data", [])
                    

                    st.session_state.battle_history = battles_data
                    st.session_state.player_tag = tag_display
                    st.success(f"✅ Found {len(battles_data)} battles")
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection error: {str(e)}")
                st.info("💡 Make sure the FastAPI backend is running on port 8000")
        else:
            st.warning("Please enter a player ID")
    

    if "battle_history" in st.session_state and st.session_state.battle_history:
        battles_data = st.session_state.battle_history
        player_tag = st.session_state.get("player_tag", "Unknown")
        
        st.markdown(f"### Battle History for {player_tag}")
        

        col1, col2, col3 = st.columns(3)
        wins = sum(1 for b in battles_data if b.get("result") == "win")
        losses = sum(1 for b in battles_data if b.get("result") == "loss")
        total = len(battles_data)
        
        with col1:
            st.metric("Total Battles", total)
        with col2:
            st.metric("Wins", wins)
        with col3:
            st.metric("Losses", losses)
        

        st.markdown("#### Recent Battles")
        battle_list = []
        for i, battle in enumerate(battles_data, 1):

            if isinstance(battle, dict):
                battle_type = battle.get("type", "Unknown")
                battle_result = battle.get("result", "unknown")
                opponent_info = battle.get("opponent", {})
                opponent_name = opponent_info.get("name", "Unknown") if isinstance(opponent_info, dict) else "Unknown"
                battle_time = battle.get("battleTime", "Unknown")
            else:
                battle_type = "Unknown"
                battle_result = "unknown"
                opponent_name = "Unknown"
                battle_time = "Unknown"
            
            battle_list.append({
                "#": i,
                "Type": battle_type,
                "Result": f"{'🟢 Win' if battle_result == 'win' else '🔴 Loss'}",
                "Opponent": opponent_name,
                "Time": battle_time
            })
        
        st.dataframe(
            data=battle_list,
            use_container_width=True,
            height=400,
            hide_index=True
        )
        

        st.markdown("#### Battle Details")
        selected_battle_idx = st.slider("Select battle to view details:", 0, len(battles_data) - 1)
        if 0 <= selected_battle_idx < len(battles_data):
            battle = battles_data[selected_battle_idx]
            with st.expander(f"Battle {selected_battle_idx + 1} Details", expanded=True):
                st.json(battle)

with tab4:
    st.subheader("🤖 AI Assistant")
    st.info("Chat with Claude AI about Clash Royale. The AI can analyze player data, suggest decks, and provide meta analysis.")
    

    ai_tab1, ai_tab2, ai_tab3, ai_tab4 = st.tabs(
        ["Chat", "Player Analysis", "Player Comparison", "Meta Analysis"]
    )
    

    with ai_tab1:
        st.subheader("Chat with Claude")
        
        user_message = st.text_area(
            "Ask anything about Clash Royale:",
            placeholder="e.g., What's the best meta right now? How do I counter PEKKA decks?"
        )
        
        if st.button("Send to Claude", key="chat_button"):
            if user_message:
                try:
                    with st.spinner("Claude is thinking..."):
                        response = requests.post(
                            f"{API_BASE_URL}/api/llm/chat",
                            params={"message": user_message},
                            timeout=30
                        )
                        response.raise_for_status()
                        result = response.json()
                    
                    if result.get("success"):
                        st.success("✅ Claude's Response:")
                        st.markdown(result.get("response", ""))
                        

                        tools_used = result.get("tools_used", 0)
                        if tools_used > 0:
                            with st.expander(f"🔧 Tools Used ({tools_used})"):
                                for tool_call in result.get("tool_calls", []):
                                    st.write(f"**Tool:** {tool_call['tool']}")
                                    st.json(tool_call['input'])
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection error: {str(e)}")
                    st.info("💡 Make sure the FastAPI backend is running on port 8000")
            else:
                st.warning("Please enter a message")
    

    with ai_tab2:
        st.subheader("AI Player Analysis")
        
        player_tag = st.text_input(
            "Enter Player ID for analysis:",
            placeholder="e.g., Y92P0L2 or #Y92P0L2",
            key="analysis_player"
        )
        
        if st.button("Analyze with Claude", key="analyze_button"):
            if player_tag:
                try:

                    tag = player_tag if player_tag.startswith("#") else f"#{player_tag}"
                    
                    with st.spinner("Claude is analyzing the player..."):
                        response = requests.post(
                            f"{API_BASE_URL}/api/llm/analyze-player",
                            params={"player_tag": tag},
                            timeout=30
                        )
                        response.raise_for_status()
                        result = response.json()
                    
                    if result.get("success"):
                        st.success(f"✅ Analysis for {tag}:")
                        st.markdown(result.get("analysis", ""))
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection error: {str(e)}")
                    st.info("💡 Make sure the FastAPI backend is running on port 8000")
            else:
                st.warning("Please enter a player ID")
    

    with ai_tab3:
        st.subheader("Compare Two Players")
        
        col1, col2 = st.columns(2)
        with col1:
            player1 = st.text_input("Player 1:", placeholder="e.g., Y92P0L2", key="compare_player1")
        with col2:
            player2 = st.text_input("Player 2:", placeholder="e.g., Y92P0L3", key="compare_player2")
        
        if st.button("Compare Players", key="compare_button"):
            if player1 and player2:
                try:

                    tag1 = player1 if player1.startswith("#") else f"#{player1}"
                    tag2 = player2 if player2.startswith("#") else f"#{player2}"
                    
                    with st.spinner("Claude is comparing the players..."):
                        response = requests.post(
                            f"{API_BASE_URL}/api/llm/compare-players",
                            params={"player_tag1": tag1, "player_tag2": tag2},
                            timeout=30
                        )
                        response.raise_for_status()
                        result = response.json()
                    
                    if result.get("success"):
                        st.success(f"✅ Comparison: {tag1} vs {tag2}")
                        st.markdown(result.get("comparison", ""))
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection error: {str(e)}")
                    st.info("💡 Make sure the FastAPI backend is running on port 8000")
            else:
                st.warning("Please enter both player IDs")
    

    with ai_tab4:
        st.subheader("Current Meta Analysis")
        
        st.write("Get Claude's analysis of the current Clash Royale meta and card economy.")
        
        if st.button("Analyze Current Meta", key="meta_button"):
            try:
                with st.spinner("Claude is analyzing the meta..."):
                    response = requests.get(
                        f"{API_BASE_URL}/api/llm/card-analysis",
                        timeout=30
                    )
                    response.raise_for_status()
                    result = response.json()
                
                if result.get("success"):
                    st.success("✅ Current Meta Analysis:")
                    st.markdown(result.get("analysis", ""))
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection error: {str(e)}")
                st.info("💡 Make sure the FastAPI backend is running on port 8000")