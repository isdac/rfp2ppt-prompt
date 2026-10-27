import sys
import os
import vertexai
from vertexai.preview import prompts
from vertexai.preview.prompts import Prompt
from google.api_core.exceptions import NotFound, AlreadyExists

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 register_prompt.py <prompt_file.txt>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    prompt_id = os.path.splitext(os.path.basename(file_path))[0]
    
    try:
        with open(file_path, 'r') as f:
            prompt_text = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find the file '{file_path}'")
        sys.exit(1)

    print(f"Initializing Vertex AI...")
    vertexai.init(project="rfp-architecture-automation", location="us-central1")

    # 1. NEW API: Use the modernized Prompt class (v2.6.0+)
    prompt_template = Prompt(
        prompt_name=prompt_id,
        prompt_data=prompt_text,
        model_name="gemini-1.5-pro-002"
    )

    # 2. CI/CD SAFE DEPLOYMENT LOGIC
    try:
        # Check if it already exists
        prompts.get(prompt_id=prompt_id)
        print(f"Prompt '{prompt_id}' already exists. Creating new version...")
        prompts.create_version(prompt_id=prompt_id, prompt=prompt_template)
        print(f"✅ Success! New version created for ID: {prompt_id}")
        
    except NotFound:
        # If it doesn't exist, create it for the first time
        print(f"Prompt '{prompt_id}' not found. Creating new prompt...")
        # Note: In the new SDK, create_version often initializes it automatically,
        # but we explicitly call create just in case.
        try:
            prompts.create(prompt=prompt_template)
        except AttributeError:
            # Fallback if create() was deprecated in favor of create_version()
            prompts.create_version(prompt=prompt_template)
            
        print(f"✅ Success! New prompt registered with ID: {prompt_id}")

if __name__ == '__main__':
    main()
