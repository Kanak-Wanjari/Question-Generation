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

def generate_base_structure(subject: str, api_key: str) -> Dict:
    """Generate the base structure with tags, categories, and subcategories."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    # Initialize the structure
    result = {
        "tags": [],
        "categories": [
                    {
                        "categorty": "Category1",
                        "sub_categories": [
                            {
                                "sub_category": "Subcategory1",
                                "topics": []
                            },
                            {
                                "sub_category": "Subcategory2",
                                "topics": [
                                    {
                                        "topic": "Topic1",
                                        "sub_topics": []
                                    }
                                ]
                            }
                        ]
                    }
        ]
    }
    

    
    # Generate tags
    print("Generating tags...")
    result["tags"] = generate_content(model, 
        f"Generate 5-8 relevant tags for {subject} interview questions. Return only tags separated by commas.")
    time.sleep(2)
    
    # Generate categories
    print("Generating categories...")
    categories = generate_content(model,
        f"Generate 5-7 main categories for {subject} interview questions. Return only category names separated by commas.")
    
    # Generate subcategories for each category
    for category in categories:
        print(f"Processing category: {category}")
        category_dict = {
            "category": category,
            "sub_categories": []
        }
        
        # Generate subcategories
        subcategories = generate_content(model,
            f"Generate 3-4 subcategories for {category} in {subject}. Return only subcategory names separated by commas.")
        
        for subcategory in subcategories:
            subcategory_dict = {
                "sub_category": subcategory,
                "topics": []  # Empty topics list to be filled by the second program
            }
            category_dict["sub_categories"].append(subcategory_dict)
            time.sleep(1)
        
        result["categories"].append(category_dict)
        time.sleep(2)
    
    return result

def save_structure(data: Dict, subject: str) -> str:
    """Save the structure to a JSON file."""
    filename = f"{subject.lower().replace(' ', '_')}_base_structure.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filename

def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KYE")
    
    subject = input("Enter the subject for interview questions: ")
    print(f"Generating base structure for {subject}...")
    
    result = generate_base_structure(subject, api_key)
    filename = save_structure(result, subject)
    print(f"Base structure has been saved to {filename}")

if __name__ == "__main__":
    main()