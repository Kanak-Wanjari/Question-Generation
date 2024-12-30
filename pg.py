import json

def read_json_file(input_file):

    try:
        with open(input_file, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading file: {e}")
        return {}

def generate_prompt(category, subcategory, topic, subtopic):
    """Create a single prompt dictionary."""
    return {
        "category": category,
        "sub_category": subcategory,
        "topic": topic,
        "sub_topic": subtopic,
        "question_prompt": f"Generate 10 questions about {subtopic} with their difficulty level. List the question followed by its difficulty level (e.g., Easy, Medium, Hard). only list the question and difficulty level. in json"
    }

def generate_all_prompts(input_file):
    """Generate prompts from JSON structure."""
    data = read_json_file(input_file)
    prompts = []
    
    for category_obj in data.get('categories', []):
        category = category_obj['category']
        for subcategory_obj in category_obj.get('sub_categories', []):
            subcategory = subcategory_obj['sub_category']
            for topic_obj in subcategory_obj.get('topics', []):
                topic = topic_obj['topic']
                for subtopic in topic_obj.get('sub_topics', []):
                    prompt = generate_prompt(category, subcategory, topic, subtopic)
                    prompts.append(prompt)
    
    return prompts

def save_prompts(output_file, prompts):
    """Save prompts to JSON file."""
    try:
        with open(output_file, 'w') as file:
            json.dump(prompts, file, indent=4)
        print(f"Saved prompts to {output_file}")
    except Exception as e:
        print(f"Error saving file: {e}")

def main():
    input_file = r"C:\Users\janhv\python_programs\technology_category_interview_question\Question-Generation\java_complete_structure.json"
    output_file = "_generated_Prompts.json"
    
    prompts = generate_all_prompts(input_file)
    if prompts:
        save_prompts(output_file, prompts)
    else:
        print("No prompts were generated")

if __name__ == "__main__":
    main()
