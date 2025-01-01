#phase 2 topic genration

import google.generativeai as genai
import json
import time
import os
from dotenv import load_dotenv

def setup_environment():
  
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KYE')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    
    # Setup Gemini
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def handle_rate_limit(func):
    """Decorator to handle rate limit errors"""
    def wrapper(*args, **kwargs):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 30  # 30s, 60s, 120s
                    print(f"Rate limit hit. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print(f"Error: {e}")
                    return None
    return wrapper

@handle_rate_limit
def generate_topics(model, category, subcategory):
    """Generate topics and subtopics using Gemini"""

    prompt = f"""Generate topics and subtopics for category '{category}', subcategory '{subcategory}'. Return JSON:
{{"topics":[{{"topic":"name","subtopics":["sub1","sub2"]}}]}}"""
    
    
    response = model.generate_content(prompt)
    response_text = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(response_text)

def process_json_file(input_file, output_file, model):
    """Process JSON file and update with generated topics"""
    try:
        # Read input file
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        # Process each category and subcategory
        for category in data['categories']:
            for sub_category in category['sub_categories']:
                print(f"Processing: {category['category']} -> {sub_category['sub_category']}")
                
                # Generate topics and subtopics
                generated_content = generate_topics(
                    model,
                    category['category'],
                    sub_category['sub_category']
                )
                
                if generated_content:
                    # Update JSON structure
                    sub_category['topics'] = []
                    for topic_data in generated_content['topics']:
                        topic_entry = {
                            "topic": topic_data['topic'],
                            "sub_topic": topic_data['subtopics']
                        }
                        sub_category['topics'].append(topic_entry)
                
                # Add delay to avoid rate limits
                time.sleep(2)
        
        # Save updated JSON
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Successfully updated {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {input_file}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    try:
        # Setup environment and model
        model = setup_environment()
        
        # Process files
        input_file = r'C:\Users\janhv\python_programs\technology_category_interview_question\Question-Generation\python.json'
        output_file = 'python_question_structure.json'
        
        process_json_file(input_file, output_file, model)
        
    except ValueError as e:
        print(f"Setup error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()







