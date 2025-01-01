import google.generativeai as genai
import json
import time
import random
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def setup_gemini(api_key):
    """Initialize Gemini model."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def generate_with_retry(model, prompt):
    """Generate content with rate limit handling."""
    retry_delays = [1, 2, 4, 8, 16]
    
    for delay in retry_delays:
        try:
            # Make the prompt more explicit about JSON format
            formatted_prompt = f"""
            Generate 10 questions about {prompt} with their difficulty levels.
            Return ONLY a JSON array in this exact format, nothing else:
            [
                {{"question": "What is...", "difficulty": "Easy"}},
                {{"question": "Explain how...", "difficulty": "Medium"}},
                ...
            ]
            """
            response = model.generate_content(formatted_prompt)
            
            # Try to extract JSON from the response
            text = response.text.strip()
            
            # Remove any markdown code block indicators if present
            text = text.replace('```json', '').replace('```', '').strip()
            
            # Validate and return JSON
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                print(f"Invalid JSON response for {prompt}. Raw response: {text[:100]}...")
                return []
                
        except Exception as e:
            if "429" in str(e):
                time.sleep(delay + random.uniform(0, 1))
                continue
            print(f"Error generating content: {str(e)}")
            return []
    
    return []

def process_prompt(model, prompt_data):
    """Process a single prompt and generate questions."""
    try:
        # Generate questions
        questions = generate_with_retry(model, prompt_data["sub_topic"])
        
        # If no questions were generated, create a placeholder
        if not questions:
            questions = [{
                "question": f"Failed to generate question about {prompt_data['sub_topic']}",
                "difficulty": "N/A"
            }]
        
        # Return results with metadata
        return {
            "category": prompt_data["category"],
            "sub_category": prompt_data["sub_category"],
            "topic": prompt_data["topic"],
            "sub_topic": prompt_data["sub_topic"],
            "questions": questions
        }
    except Exception as e:
        print(f"Error processing {prompt_data['sub_topic']}: {str(e)}")
        return {**prompt_data, "questions": []}

def main():
    # Get API key from .env
    api_key = os.getenv('GEMINI_API_KYE')
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env file")
        return

    # Setup input/output files with raw strings for Windows paths
    input_file = r"C:\Users\janhv\python_programs\technology_category_interview_question\QG\json.json"
    output_file = r"C:\Users\janhv\python_programs\technology_category_interview_question\QG\Generated_Questions.json"
    
    try:
        with open(input_file, 'r') as f:
            prompts = json.load(f)
        
        model = setup_gemini(api_key)
        results = []
        total = len(prompts)
        
        for i, prompt_data in enumerate(prompts, 1):
            print(f"Processing {i}/{total}: {prompt_data['sub_topic']}")
            result = process_prompt(model, prompt_data)
            results.append(result)
            
            # Save after each successful generation to prevent losing progress
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=4)
            
            time.sleep(1)  # Increased delay to be safer with rate limits
        
        print(f"Successfully generated questions and saved to {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Could not find file {input_file}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
