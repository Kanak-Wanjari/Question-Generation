import json
import google.generativeai as genai
import uuid
import re
import time

# Configure the Gemini API
genai.configure(api_key="AIzaSyDASsvvspdyZyGoX_CV2VF7Go-SFaF7MZY") #insert API key here
model = genai.GenerativeModel("gemini-1.5-flash")

prompts_file = "./json-files/Generated_Prompts.json" #Generated_Prompts.json

# Load prompts from JSON file
with open(prompts_file, "r") as file:
    prompts = json.load(file)

# Initialize an empty list to store the formatted results
formatted_results = []

# Function to handle API calls with retry mechanism
def generate_content_with_retries(prompt_text, retries=3, wait_time=60):
    for attempt in range(1, retries + 1):
        try:
            response = model.generate_content(prompt_text)
            return response.text  # Successful response
        except Exception as e:
            error_message = str(e)
            print(f"Attempt {attempt}: Error generating content - {error_message}")
            
            # Check for rate limit error (429) or general exception
            if "429" in error_message or "quota" in error_message.lower():
                print(f"Rate limit hit. Waiting for {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                print("Non-retryable error occurred. Skipping this prompt.")
                break  # Non-retryable error, break out of retry loop
    return None  # Return None if all attempts fail

# Loop through each prompt and generate questions
for prompt in prompts:
    topic = prompt["topic"]
    sub_topic = prompt["sub_topic"]
    question_prompt = prompt["question_prompt"]

    print(f"Generating content for: {topic} - {sub_topic}")
    try:
        # Call the API with retries
        response_text = generate_content_with_retries(question_prompt)
        
        if response_text:
            # Clean the response text (remove Markdown formatting, if any)
            cleaned_response = re.sub(r'```(json)?', '', response_text).strip()

            # Parse JSON response
            questions = json.loads(cleaned_response)

            # Process the questions
            for question in questions:
                formatted_results.append({
                    "id": str(uuid.uuid4()),  # Generate a unique UUID for each question
                    "category": "Technical",
                    "topic": topic,
                    "sub_topic": sub_topic,
                    "question": question.get("question", "not available"),
                    "answer": question.get("answer", "not available"),
                    "difficulty_level": question.get("difficulty", "not available"),
                    "is_active": True
                })
        else:
            print(f"Skipping prompt '{question_prompt}' due to repeated failures.")
    except Exception as e:
        print(f"Unexpected error while processing '{question_prompt}': {e}")

# Save the results to a JSON file
output_file = r"Master_Interview_Questions.json" #Master_Interview_Questions
with open(output_file, "w") as file:
    json.dump(formatted_results, file, indent=4)

print(f"Questions have been saved to {output_file}")
