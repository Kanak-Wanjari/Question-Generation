import google.generativeai as genai
import json
import os
from typing import Dict, List
import time
from dotenv import load_dotenv

def configure_genai(api_key: str) -> None:

    genai.configure(api_key=api_key)
    
def generate_categories(model, subject: str) -> List[str]:
   
    prompt = f"""Generate 5-7 main categories for {subject} interview questions. 
    Return only the category names separated by commas. Keep them broad and comprehensive."""
    
    response = model.generate_content(prompt)
    categories = [cat.strip() for cat in response.text.split(',')]
    return categories

def generate_subcategories(model, category: str, subject: str) -> List[str]:
  
    prompt = f"""Generate 3-4 subcategories for the {category} category in {subject}.
    These should be specific areas within {category}. Return only the subcategory names separated by commas."""
    
    response = model.generate_content(prompt)
    subcategories = [subcat.strip() for subcat in response.text.split(',')]
    return subcategories

def generate_topics(model, subcategory: str, subject: str) -> List[str]:
  
    prompt = f"""Generate 2-3 specific topics for the {subcategory} subcategory in {subject}.
    These should be concrete areas that interview questions can focus on.
    Return only the topic names separated by commas."""
    
    response = model.generate_content(prompt)
    topics = [topic.strip() for topic in response.text.split(',')]
    return topics

def generate_subtopics(model, topic: str, subject: str) -> List[str]:

    prompt = f"""Generate 2-3 subtopics for the {topic} topic in {subject}.
    These should be specific concepts or areas within the topic.
    Return only the subtopic names separated by commas."""
    
    response = model.generate_content(prompt)
    subtopics = [subtopic.strip() for subtopic in response.text.split(',')]
    return subtopics

def generate_tags(model, subject: str) -> List[str]:
   
    prompt = f"""Generate 5-8 relevant tags for {subject} interview questions.
    These should be keywords that help categorize and search the content.
    Return only the tags separated by commas."""
    
    response = model.generate_content(prompt)
    tags = [tag.strip() for tag in response.text.split(',')]
    return tags

def generate_interview_structure(subject: str, api_key: str) -> Dict:
    
    configure_genai(api_key)
    
    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Initialize the result structure
    result = {
        "tags": [],
        "categories": []
    }
    
    # Generate tags
    result["tags"] = generate_tags(model, subject)
    
    # Generate categories and their hierarchical structure
    categories = generate_categories(model, subject)
    
    for category in categories:
        category_dict = {
            "category": category,
            "sub_categories": []
        }
        
        subcategories = generate_subcategories(model, category, subject)
        
        for subcategory in subcategories:
            subcategory_dict = {
                "sub_category": subcategory,
                "topics": []
            }
            
            topics = generate_topics(model, subcategory, subject)
            
            for topic in topics:
                topic_dict = {
                    "topic": topic,
                    "sub_topics": generate_subtopics(model, topic, subject)
                }
                subcategory_dict["topics"].append(topic_dict)
                time.sleep(1)  # Rate limiting
            
            category_dict["sub_categories"].append(subcategory_dict)
        
        result["categories"].append(category_dict)
    
    return result

def save_to_json(data: Dict, subject: str) -> str:
    """Save the generated structure to a JSON file."""
    filename = f"{subject.lower().replace(' ', '_')}_interview_structure.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filename

def main():
    
    load_dotenv()
    # Get the API key from environment variable
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("Please set the GOOGLE_API_KEY environment variable")
    
    # Get subject from user
    subject = input("Enter the subject for interview questions (e.g., Python, Machine Learning, Web Development): ")
    
    # Generate the structure
    print(f"Generating interview structure for {subject}...")
    result = generate_interview_structure(subject, api_key)
    
    # Save to file
    filename = save_to_json(result, subject)
    print(f"Interview structure has been saved to {filename}")

if __name__ == "__main__":
    main()