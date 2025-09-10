#!/usr/bin/env python3
"""
Test script for the README updater
Run this locally to test the functionality before pushing to GitHub
"""

import os
import sys
from update_readme import extract_current_sentence, get_word_extension

def test_sentence_extraction():
    """Test if we can extract the sentence correctly"""
    
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    sentence = extract_current_sentence(content)
    print(f"Extracted sentence: {sentence}")
    
    return sentence

def test_api_call():
    """Test the OpenRouter API call"""
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("Please set OPENROUTER_API_KEY environment variable for testing")
        return False
    
    test_sentence = "I'm Koorosh, a Data Engineering Intern in TomTom's MAAP team, and I've been amazed by this company since the day I joined because"
    
    print("Testing API call...")
    new_words = get_word_extension(test_sentence, api_key)
    
    if new_words:
        print(f"API returned: '{new_words}'")
        return True
    else:
        print("API call failed")
        return False

def main():
    """Run tests"""
    
    print("=== Testing README Updater ===\n")
    
    print("1. Testing sentence extraction...")
    sentence = test_sentence_extraction()
    print()
    
    print("2. Testing API call...")
    api_success = test_api_call()
    print()
    
    if api_success:
        print("SUCCESS: All tests passed! The script should work in GitHub Actions.")
    else:
        print("ERROR: API test failed. Check your OPENROUTER_API_KEY.")
    
    print("\nTo test the full script locally:")
    print("export OPENROUTER_API_KEY='your-key-here'")
    print("python update_readme.py")

if __name__ == "__main__":
    main()
