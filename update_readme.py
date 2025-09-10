#!/usr/bin/env python3
"""
Daily README updater using OpenRouter's Llama model
Adds one or two words to the ongoing sentence about TomTom
"""

import os
import re
import json
import requests
import sys
from datetime import datetime


def extract_current_sentence(readme_content):
    """Extract the current sentence that needs to be extended"""
    human_pattern = r"\*\*I'm Koorosh, a Data Engineering Intern in TomTom's MAAP team, and I've been amazed by this company since the day I joined because\*\*"
    
    ai_pattern = r"> \*🤖 AI continues the story daily:\*\s*\n> \*\*(.*?)\*\*"
    
    ai_match = re.search(ai_pattern, readme_content, re.DOTALL)
    
    base_sentence = "I'm Koorosh, a Data Engineering Intern in TomTom's MAAP team, and I've been amazed by this company since the day I joined because"
    
    if ai_match and ai_match.group(1).strip():
        ai_content = ai_match.group(1).strip()
        return f"{base_sentence} {ai_content}"
    else:
        return base_sentence


def get_word_extension(current_sentence, api_key):
    """Get 1-2 words to extend the sentence using OpenRouter"""
    
    prompt = f"""You are helping to extend a sentence about someone's experience at TomTom (the mapping/navigation company). 

Current sentence: "{current_sentence}"

Add exactly 1-2 words that would naturally continue this sentence. Make it positive and professional, relating to technology, mapping, navigation, data engineering, or team culture at TomTom.

Respond with ONLY the 1-2 words to add (no punctuation, no explanation, no quotes). The words should flow naturally from the existing sentence."""

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": "meta-llama/llama-3.1-405b-instruct:free",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 10,
                "temperature": 0.7
            }),
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            new_words = result['choices'][0]['message']['content'].strip()
            new_words = re.sub(r'[^\w\s]', '', new_words).strip()
            return new_words
        else:
            print(f"Unexpected API response: {result}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Failed to parse API response: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def update_readme(readme_path, current_sentence, new_words):
    """Update the README file with the extended sentence"""
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract just the AI part (everything after "because")
    base_sentence = "I'm Koorosh, a Data Engineering Intern in TomTom's MAAP team, and I've been amazed by this company since the day I joined because"
    
    if current_sentence.startswith(base_sentence):
        current_ai_part = current_sentence[len(base_sentence):].strip()
        new_ai_part = f"{current_ai_part} {new_words}".strip()
    else:
        new_ai_part = new_words
    
    ai_pattern = r"(> \*🤖 AI continues the story daily:\*\s*\n> \*\*)(.*?)(\*\*)"
    
    def replacement(match):
        return f"{match.group(1)}{new_ai_part}{match.group(3)}"
    
    new_content = re.sub(ai_pattern, replacement, content, flags=re.DOTALL)
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return f"{base_sentence} {new_ai_part}"


def main():
    """Main function to orchestrate the README update"""
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set")
        sys.exit(1)
    
    readme_path = 'README.md'
    
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found")
        sys.exit(1)
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    current_sentence = extract_current_sentence(readme_content)
    print(f"Current sentence: {current_sentence}")
    
    print("Requesting word extension from OpenRouter...")
    new_words = get_word_extension(current_sentence, api_key)
    
    if not new_words:
        print("Failed to get word extension from API")
        sys.exit(1)
    
    print(f"Got new words: '{new_words}'")
    
    new_sentence = update_readme(readme_path, current_sentence, new_words)
    print(f"Updated sentence: {new_sentence}")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"README updated successfully at {timestamp}")
    print(f"Added words: '{new_words}'")


if __name__ == "__main__":
    main()
