#!/usr/bin/env python3
"""
Quick test to verify all components are properly installed
"""
import sys

def test_imports():
    print("🔍 Testing imports...\n")
    
    try:
        import anthropic
        print(f"✅ anthropic {anthropic.__version__}")
    except ImportError as e:
        print(f"❌ anthropic: {e}")
        return False
    
    try:
        import fastapi
        print(f"✅ fastapi")
    except ImportError as e:
        print(f"❌ fastapi: {e}")
        return False
    
    try:
        import streamlit
        print(f"✅ streamlit")
    except ImportError as e:
        print(f"❌ streamlit: {e}")
        return False
    
    try:
        import httpx
        print(f"✅ httpx")
    except ImportError as e:
        print(f"❌ httpx: {e}")
        return False
    
    try:
        import pydantic
        print(f"✅ pydantic")
    except ImportError as e:
        print(f"❌ pydantic: {e}")
        return False
    
    try:
        import requests
        print(f"✅ requests")
    except ImportError as e:
        print(f"❌ requests: {e}")
        return False
    
    return True

def test_environment():
    print("\n🔑 Checking environment variables...\n")
    
    import os
    
    clash_royale_token = os.getenv("CLASH_ROYALE_API_TOKEN")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    if clash_royale_token:
        print(f"✅ CLASH_ROYALE_API_TOKEN is set")
    else:
        print(f"⚠️  CLASH_ROYALE_API_TOKEN not set (needed for API calls)")
    
    if anthropic_key:
        print(f"✅ ANTHROPIC_API_KEY is set")
    else:
        print(f"⚠️  ANTHROPIC_API_KEY not set (needed for Claude)")
    
    return clash_royale_token and anthropic_key

def test_llm_integration():
    print("\n🤖 Testing LLM integration module...\n")
    
    try:
        from llm_integration import CLASH_ROYALE_TOOLS, chat_with_claude
        print(f"✅ llm_integration module imports correctly")
        print(f"✅ Found {len(CLASH_ROYALE_TOOLS)} tools defined")
        for tool in CLASH_ROYALE_TOOLS:
            print(f"   - {tool['name']}")
        return True
    except Exception as e:
        print(f"❌ llm_integration: {e}")
        return False

if __name__ == "__main__":
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║           CLASH ROYALE AI - SETUP VERIFICATION                 ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    imports_ok = test_imports()
    env_ok = test_environment()
    llm_ok = test_llm_integration()
    
    print("\n" + "═" * 70)
    
    if imports_ok and llm_ok:
        print("\n✅ All systems ready!")
        print("\n�� To start the application:")
        print("   Terminal 1: python3 api.py")
        print("   Terminal 2: streamlit run app.py")
        print("\n📍 Access at: http://localhost:8501")
        
        if not env_ok:
            print("\n⚠️  Remember to set API keys:")
            print("   export ANTHROPIC_API_KEY='your_key'")
            print("   export CLASH_ROYALE_API_TOKEN='your_token'")
    else:
        print("\n❌ Some components are missing. Please run:")
        print("   pip install -r requirements.txt")
        sys.exit(1)

