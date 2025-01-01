import google.generativeai as genai
import json
import os
from typing import Dict, List
import time
from dotenv import load_dotenv

def generate_content(model, prompt: str, retries: int = 3, wait_time: int = 60) -> List[str]:
    """Generate content with retry logic and return list of comma-separated items."""
    for attempt in range(1, retries + 1):
        try:
            response = model.generate_content(prompt)
            return [item.strip() for item in response.text.split(',')]
        except Exception as e:
            print(f"Attempt {attempt}: Error - {str(e)}")
            if "429" in str(e) or "quota" in str(e).lower():
                if attempt < retries:
                    print(f"Rate limit hit. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print("Max retries reached.")
            else:
                print("Non-retryable error. Skipping.")
                break
    return []

def enrich_with_topics(base_structure: Dict, subject: str, api_key: str) -> Dict:
    """Add topics and subtopics to the existing structure."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    # Iterate through the existing structure
    for category in base_structure["categories"]:
        for subcategory in category["sub_categories"]:
            print(f"Processing topics for subcategory: {subcategory['sub_category']}")
            
            # Generate topics
            topics = generate_content(model,
                f"Generate 2-3 specific topics for {subcategory['sub_category']} in {subject}. Return only topic names separated by commas.")
            
            # Generate subtopics for each topic
            for topic in topics:
                print(f"Processing subtopics for topic: {topic}")
                subtopics = generate_content(model,
                    f"Generate 2-3 subtopics for {topic} in {subject}. Return only subtopic names separated by commas.")
                
                topic_dict = {
                    "topic": topic,
                    "sub_topics": subtopics
                }
                subcategory["topics"].append(topic_dict)
                time.sleep(2)
            
            time.sleep(1)
    
    return base_structure

def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KYE")
    
    # Get the subject name from the user
    subject = input("Enter the subject name (should match the base structure): ")
    base_filename = f"{subject.lower().replace(' ', '_')}_base_structure.json"
    
    # Load the base structure
    try:
        with open(base_filename, 'r', encoding='utf-8') as f:
            base_structure = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find base structure file: {base_filename}")
        return
    
    print(f"Enriching structure with topics and subtopics...")
    enriched_structure = enrich_with_topics(base_structure, subject, api_key)
    
    # Save the enriched structure
    final_filename = f"{subject.lower().replace(' ', '_')}_complete_structure.json"
    with open(final_filename, 'w', encoding='utf-8') as f:
        json.dump(enriched_structure, f, indent=2, ensure_ascii=False)
    
    print(f"Complete structure has been saved to {final_filename}")

if __name__ == "__main__":
    main()