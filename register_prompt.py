import sys
import os
import vertexai
from vertexai.preview import prompts
from vertexai.preview.prompts import Prompt

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 register_prompt.py <prompt_file.txt>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    # This is your human-readable text name (e.g., 'generate_ppt_from_rfp')
    display_name = os.path.splitext(os.path.basename(file_path))[0]
    
    try:
        with open(file_path, 'r') as f:
            prompt_text = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find the file '{file_path}'")
        sys.exit(1)

    print(f"Initializing Vertex AI...")
    vertexai.init(project="rfp-architecture-automation", location="us-central1")

    prompt_template = Prompt(
        prompt_name=display_name,
        prompt_data=prompt_text,
        model_name="gemini-1.5-pro-002"
    )

    print(f"Searching for existing prompt named '{display_name}'...")
    existing_prompt_id = None
    
    try:
        # Search through existing prompts to find the real numeric ID
        for p in prompts.list():
            name = getattr(p, "display_name", getattr(p, "prompt_name", ""))
            if name == display_name:
                existing_prompt_id = p.prompt_id
                break
    except Exception as e:
        print(f"Note: Could not list prompts or registry is empty.")

    # CI/CD SAFE DEPLOYMENT LOGIC
    if existing_prompt_id:
        print(f"Prompt found! Internal ID is {existing_prompt_id}. Creating new version...")
        prompts.create_version(prompt_id=existing_prompt_id, prompt=prompt_template)
        print(f"✅ Success! New version created for prompt: {display_name}")
    else:
        print(f"Prompt not found. Registering as a new prompt...")
        new_prompt = prompts.create(prompt=prompt_template)
        # Extract the auto-assigned numeric ID
        assigned_id = getattr(new_prompt, "prompt_id", "Unknown ID")
        print(f"✅ Success! New prompt registered with Internal ID: {assigned_id}")

if __name__ == '__main__':
    main()
