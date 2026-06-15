import os
import re
import requests

def get_ai_insight():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "> ⚠️ *Error: GEMINI_API_KEY missing from repository secrets.*"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    # Custom prompt tailored to your background
    prompt = (
        "You are A.P.E.X. (The Digital Race Engineer), an autonomous AI Agent running inside "
        "Shubham Kumar's GitHub profile. Shubham is a Full Stack Developer, ML/Data Science enthusiast, and AI-Agent builder from Bangalore. "
        "Write a concise, ultra-futuristic 'Daily Telemetry Log' (max 3 sentences). "
        "It should contain a fascinating micro-insight about Machine Learning, Data Science, autonomous AI agents, "
        "or high-performance software architecture. Use F1 racing metaphors (like telemetry, downforce, apex, pit stops, tire degradation) combined with tech concepts. "
        "Keep the tone sharp, sci-fi/cyberpunk, and highly technical. "
        "Do not use markdown headers, just the blockquote quote text."
    )

    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        insight = data['candidates'][0]['content']['parts'][0]['text'].strip()
        return f"> 🤖 **AGENT_LOG //** {insight}"
    except Exception as e:
        return f"> ⚠️ *Agent telemetry offline: Unable to parse AI stream.*"

def update_readme():
    with open("README.md", "r", encoding="utf-8") as file:
        content = file.read()

    new_insight = get_ai_insight()
    
    # Construct the replacement payload
    new_log_block = f"\n### ✦ SYSTEM_LOG: DAILY_AI_AGENT_INSIGHT ✦\n\n{new_insight}\n"
    
    # Regex to find everything between our two tags and replace it
    pattern = r".*?"
    updated_content = re.sub(pattern, new_log_block, content, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as file:
        file.write(updated_content)

if __name__ == "__main__":
    update_readme()
