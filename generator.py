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

def generate_with_retry(model, topic, subtopic):
    """Generate content with rate limit handling."""
    retry_delays = [1, 2, 4, 8, 16]
    
    for delay in retry_delays:
        try:
            # Make the prompt more explicit about JSON format
            formatted_prompt = f"""
            Generate 10 interview questions about {subtopic} (which is a subtopic of {topic}).
            For each question, provide:
            1. A detailed question
            2. 3-5 relevant tags specific to the question
            3. An appropriate time limit (1-5 minutes)
            4. A point value (5-10 points based on complexity)
            5. A difficulty level (Easy, Medium, or Hard)

            Return ONLY a JSON array in this exact format, nothing else:
            [
                {{
                    "question_text": "Detailed question here",
                    "tags": "tag1, tag2, tag3",
                    "time_limit": "X minutes",
                    "point_value": Y,
                    "difficulty_level": "Difficulty"
                }},
                ...
            ]
            """
            response = model.generate_content(formatted_prompt)
            
            # Clean and parse response
            text = response.text.strip()
            text = text.replace('```json', '').replace('```', '').strip()
            
            return json.loads(text)
                
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
        questions = generate_with_retry(model, prompt_data["topic"], prompt_data["sub_topic"])
        
        # If no questions were generated, create a placeholder
        if not questions:
            questions = [{
                "question_text": f"Failed to generate question about {prompt_data['sub_topic']}",
                "tags": "error, failed",
                "time_limit": "1 minute",
                "point_value": 5,
                "difficulty_level": "N/A"
            }]
        
        # Format each question with all required fields
        formatted_questions = []
        for q in questions:
            formatted_question = {
                # Fields from input JSON
                "category": prompt_data["category"],
                "sub_category": prompt_data["sub_category"],
                "topic": prompt_data["topic"],
                "sub_topic": prompt_data["sub_topic"],
                
                # AI-generated fields
                "question_text": q["question_text"],
                "tags": q["tags"],
                "time_limit": q["time_limit"],
                "point_value": q["point_value"],
                "difficulty_level": q["difficulty_level"],
                
                # Constant fields
                "language_specific": "Computer Networks",
                "interview_category": "Technical"
            }
            formatted_questions.append(formatted_question)
        
        return formatted_questions
        
    except Exception as e:
        print(f"Error processing {prompt_data['sub_topic']}: {str(e)}")
        return []

def main():
    # Get API key from .env
    api_key = os.getenv('GEMINI_API_KYE')
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env file")
        return

    # Setup input/output files with raw strings for Windows paths
    input_file = r"C:\Users\janhv\python_programs\technology_category_interview_question\Question-Generation\prompt_jsons\CN_generated_Prompts.json"
    output_file = r"C:\Users\janhv\python_programs\technology_category_interview_question\Question-Generation\generated_questions\CN_generated_Questions.json"
    
    try:
        with open(input_file, 'r') as f:
            prompts = json.load(f)
        
        model = setup_gemini(api_key)
        all_questions = []
        total = len(prompts)
        
        for i, prompt_data in enumerate(prompts, 1):
            print(f"Processing {i}/{total}: {prompt_data['sub_topic']}")
            questions = process_prompt(model, prompt_data)
            all_questions.extend(questions)
            
            # Save after each successful generation
            with open(output_file, 'w') as f:
                json.dump(all_questions, f, indent=4)
            
            time.sleep(1)
        
        print(f"Successfully generated {len(all_questions)} questions and saved to {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Could not find file {input_file}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()



