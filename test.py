import google.generativeai as genai
import json
import os
from typing import Dict, List, Optional
import time
from dotenv import load_dotenv

def generate_content_with_retries(model, prompt_text: str, retries: int = 3, wait_time: int = 60) -> Optional[str]:

    for attempt in range(1, retries + 1):
        try:
            response = model.generate_content(prompt_text)
            return response.text  # Successful response
        except Exception as e:
            error_message = str(e)
            print(f"Attempt {attempt}: Error generating content - {error_message}")
            
            # Check for rate limit error (429) or general exception
            if "429" in error_message or "quota" in error_message.lower():
                if attempt < retries:
                    print(f"Rate limit hit. Waiting for {wait_time} seconds before retrying...")
                    time.sleep(wait_time)
                else:
                    print("Max retries reached. Moving on...")
            else:
                print("Non-retryable error occurred. Skipping this prompt.")
                break  # Non-retryable error, break out of retry loop
    return None

def configure_genai(api_key: str) -> None:
    """Configure the Gemini AI model with the provided API key."""
    genai.configure(api_key=api_key)

def generate_categories(model, subject: str) -> List[str]:
    """Generate main categories for the subject using Gemini AI."""
    prompt = f"""Generate 5-7 main categories for {subject} interview questions. 
    Return only the category names separated by commas. Keep them broad and comprehensive."""
    
    response = generate_content_with_retries(model, prompt)
    if response:
        return [cat.strip() for cat in response.split(',')]
    return []

def generate_subcategories(model, category: str, subject: str) -> List[str]:
    """Generate subcategories for each main category using Gemini AI."""
    prompt = f"""Generate 3-4 subcategories for the {category} category in {subject}.
    These should be specific areas within {category}. Return only the subcategory names separated by commas."""
    
    response = generate_content_with_retries(model, prompt)
    if response:
        return [subcat.strip() for subcat in response.split(',')]
    return []

def generate_topics(model, subcategory: str, subject: str) -> List[str]:
    """Generate topics for each subcategory using Gemini AI."""
    prompt = f"""Generate 2-3 specific topics for the {subcategory} subcategory in {subject}.
    These should be concrete areas that interview questions can focus on.
    Return only the topic names separated by commas."""
    
    response = generate_content_with_retries(model, prompt)
    if response:
        return [topic.strip() for topic in response.split(',')]
    return []

def generate_subtopics(model, topic: str, subject: str) -> List[str]:
    """Generate subtopics for each topic using Gemini AI."""
    prompt = f"""Generate 2-3 subtopics for the {topic} topic in {subject}.
    These should be specific concepts or areas within the topic.
    Return only the subtopic names separated by commas."""
    
    response = generate_content_with_retries(model, prompt)
    if response:
        return [subtopic.strip() for subtopic in response.split(',')]
    return []

def generate_tags(model, subject: str) -> List[str]:
    """Generate relevant tags for the subject using Gemini AI."""
    prompt = f"""Generate 5-8 relevant tags for {subject} interview questions.
    These should be keywords that help categorize and search the content.
    Return only the tags separated by commas."""
    
    response = generate_content_with_retries(model, prompt)
    if response:
        return [tag.strip() for tag in response.split(',')]
    return []

def generate_interview_structure(subject: str, api_key: str) -> Dict:
    """Generate the complete interview question structure for a given subject."""
    configure_genai(api_key)
    
    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-pro')
    
    # Initialize the result structure
    result = {
        "tags": [],
        "categories": []
    }
    
    print("Generating tags...")
    result["tags"] = generate_tags(model, subject)
    
    print("Generating categories...")
    categories = generate_categories(model, subject)
    
    for category in categories:
        print(f"Processing category: {category}")
        category_dict = {
            "category": category,
            "sub_categories": []
        }
        
        subcategories = generate_subcategories(model, category, subject)
        
        for subcategory in subcategories:
            print(f"Processing subcategory: {subcategory}")
            subcategory_dict = {
                "sub_category": subcategory,
                "topics": []
            }
            
            topics = generate_topics(model, subcategory, subject)
            
            for topic in topics:
                print(f"Processing topic: {topic}")
                topic_dict = {
                    "topic": topic,
                    "sub_topics": generate_subtopics(model, topic, subject)
                }
                subcategory_dict["topics"].append(topic_dict)
                time.sleep(2)  # Additional delay between major operations
            
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
    # Replace this with your actual API key
    api_key = os.getenv("GEMINI_API_KYE")  # Replace this with your Gemini API key
    
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



