import json
import os
import time
import google.generativeai as genai
from typing import List, Dict
import logging
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def setup_gemini(api_key: str):
    """Initialize Gemini API."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def generate_questions(model, prompt: Dict) -> Dict:
    """Generate interview questions for a single prompt."""
    try:
        # Get response from Gemini
        response = model.generate_content(prompt["question_prompt"])
        
        # Parse the response text as JSON
        try:
            questions = json.loads(response.text)
        except json.JSONDecodeError:
            # If response isn't valid JSON, return it as raw text
            questions = response.text
        
        # Create result dictionary
        result = {
            "category": prompt["category"],
            "sub_category": prompt["sub_category"],
            "topic": prompt["topic"],
            "sub_topic": prompt["sub_topic"],
            "questions": questions
        }
        
        return result
    
    except Exception as e:
        logging.error(f"Error generating questions for {prompt['sub_topic']}: {str(e)}")
        return None

def process_prompts_in_chunks(prompts: List[Dict], api_key: str, 
                            chunk_size: int = 5, delay_seconds: int = 3):
    """Process prompts in chunks with rate limiting."""
    model = setup_gemini(api_key)
    results = []
    failed_prompts = []
    
    # Process prompts in chunks
    for i in range(0, len(prompts), chunk_size):
        chunk = prompts[i:i + chunk_size]
        logging.info(f"Processing chunk {i//chunk_size + 1} of {len(prompts)//chunk_size + 1}")
        
        # Process each prompt in the chunk
        for prompt in chunk:
            try:
                # Generate questions
                result = generate_questions(model, prompt)
                
                if result:
                    results.append(result)
                    logging.info(f"Generated questions for: {prompt['sub_topic']}")
                    
                    # Save progress after each successful generation
                    save_results(results, "generated_questions.json")
                else:
                    failed_prompts.append(prompt)
                    logging.warning(f"Failed to generate questions for: {prompt['sub_topic']}")
            
            except Exception as e:
                failed_prompts.append(prompt)
                logging.error(f"Error processing prompt: {str(e)}")
            
            # Small delay between individual prompts
            time.sleep(1)
        
        # Delay between chunks
        logging.info(f"Waiting {delay_seconds} seconds before next chunk...")
        time.sleep(delay_seconds)
    
    # Save failed prompts
    if failed_prompts:
        save_results(failed_prompts, "failed_prompts.json")
    
    return results, failed_prompts

def save_results(data: List[Dict], filename: str):
    """Save results to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Saved results to {filename}")
    except Exception as e:
        logging.error(f"Error saving to {filename}: {str(e)}")

def main():
    load_dotenv
    api_key = os.getenv('GEMINI_API_KYE')
    input_file = r'C:\Users\janhv\python_programs\technology_category_interview_question\Question-Generation\Generated_Prompts_new.json'
    # Load prompts from file
    try:
        with open(input_file, 'r') as f:
            prompts = json.load(f)
        logging.info(f"Loaded {len(prompts)} prompts")
    except Exception as e:
        logging.error(f"Error loading prompts: {str(e)}")
        return
    
    # Process prompts and generate questions
    results, failed = process_prompts_in_chunks(
        prompts=prompts,
        api_key=api_key,
        chunk_size=5,  # Process 5 prompts at a time
        delay_seconds=3  # Wait 3 seconds between chunks
    )
    
    # Final summary
    logging.info(f"Processing completed!")
    logging.info(f"Successfully generated questions: {len(results)}")
    logging.info(f"Failed prompts: {len(failed)}")

if __name__ == "__main__":
    main()