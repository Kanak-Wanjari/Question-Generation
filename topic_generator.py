import google.generativeai as genai
import json
import os
from typing import Dict, List, Optional
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

def generate_structure(model, item_type: str, context: str, subject: str, count: str) -> List[str]:
    """Generic function to generate structure items."""
    prompt = f"""Generate {count} {item_type} for {context} in {subject}. 
                Return only the names separated by commas."""
    return generate_content(model, prompt)

def generate_interview_structure(subject: str, api_key: str) -> Dict:
    """Generate the complete interview question structure."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    result = {"tags": [], "categories": []}
    
    print("Generating tags...")
    result["tags"] = generate_content(model, 
        f"Generate 5-8 relevant tags for {subject} interview questions. Return only tags separated by commas.")
    
    print("Generating categories...")
    categories = generate_structure(model, "categories", subject, subject, "5-7")
    
    for category in categories:
        print(f"Processing category: {category}")
        category_dict = {"category": category, "sub_categories": []}
        
        subcategories = generate_structure(model, "subcategories", category, subject, "3-4")
        
        for subcategory in subcategories:
            print(f"Processing subcategory: {subcategory}")
            subcategory_dict = {"sub_category": subcategory, "topics": []}
            
            topics = generate_structure(model, "topics", subcategory, subject, "2-3")
            
            for topic in topics:
                print(f"Processing topic: {topic}")
                subtopics = generate_structure(model, "subtopics", topic, subject, "2-3")
                subcategory_dict["topics"].append({
                    "topic": topic,
                    "sub_topics": subtopics
                })
                time.sleep(2)
            
            category_dict["sub_categories"].append(subcategory_dict)
        
        result["categories"].append(category_dict)
    
    return result

def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KYE")
    subject = input("Enter the subject for interview questions (e.g., Python, Machine Learning): ")
    
    print(f"Generating interview structure for {subject}...")
    result = generate_interview_structure(subject, api_key)
    
    filename = f"{subject.lower().replace(' ', '_')}_interview_structure.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"Interview structure has been saved to {filename}")

if __name__ == "__main__":
    main()