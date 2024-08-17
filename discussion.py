import sys
import subprocess
import pkg_resources

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_requirements():
    # List of required packages
    required_packages = [
        'openai',
        'google-generativeai',
        'anthropic'
    ]

    # Check if pip is installed
    try:
        import pip
    except ImportError:
        print("pip is not installed. Please install pip first.")
        sys.exit(1)

    # Check each required package
    for package in required_packages:
        try:
            pkg_resources.get_distribution(package)
            print(f"{package} is already installed.")
        except pkg_resources.DistributionNotFound:
            print(f"{package} is not installed. Installing...")
            try:
                install(package)
                print(f"{package} has been successfully installed.")
            except Exception as e:
                print(f"An error occurred while installing {package}: {str(e)}")
                sys.exit(1)

    print("All required packages are installed.")

if __name__ == "__main__":
    check_and_install_requirements()

from openai import OpenAI
import google.generativeai as genai
import anthropic
import time
import json
import sys

# Set up API clients and keys
client = OpenAI(api_key='')
anthropic_client = anthropic.Anthropic(api_key='')
genai.configure(api_key='')

# Initialize AI models
gpt_model = "gpt-4"
claude_model = "claude-2"
gemini_model = genai.GenerativeModel('gemini-pro')

def get_gpt_response(prompt):
    response = client.chat.completions.create(
        model=gpt_model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def get_claude_response(prompt):
    response = anthropic_client.completions.create(
        model=claude_model,
        prompt=f"Human: {prompt}\n\nAssistant:",
        max_tokens_to_sample=300
    )
    return response.completion

def get_gemini_response(prompt):
    response = gemini_model.generate_content(prompt)
    return response.text

def group_discussion(topic, rounds=3):
    conversation = [f"Topic for discussion: {topic}"]
    
    for round in range(rounds):
        print(f"\nRound {round + 1}:")
        
        # Get responses from each AI
        gpt_response = get_gpt_response("\n".join(conversation))
        claude_response = get_claude_response("\n".join(conversation))
        gemini_response = get_gemini_response("\n".join(conversation))
        
        # Add responses to the conversation
        conversation.extend([
            f"GPT: {gpt_response}",
            f"Claude: {claude_response}",
            f"Gemini: {gemini_response}"
        ])
        
        # Print responses
        print("GPT:", gpt_response)
        print("Claude:", claude_response)
        print("Gemini:", gemini_response)
        
        time.sleep(2)  # Pause between rounds
    
    # Final consensus and dissenting opinion
    consensus_prompt = "Based on the discussion above, what is the general consensus? If there's a dissenting opinion, please state it as well."
    
    gpt_consensus = get_gpt_response("\n".join(conversation) + "\n" + consensus_prompt)
    claude_consensus = get_claude_response("\n".join(conversation) + "\n" + consensus_prompt)
    gemini_consensus = get_gemini_response("\n".join(conversation) + "\n" + consensus_prompt)
    
    print("\nFinal Consensus and Dissenting Opinions:")
    print("GPT Consensus:", gpt_consensus)
    print("Claude Consensus:", claude_consensus)
    print("Gemini Consensus:", gemini_consensus)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py 'Your discussion topic here'")
        sys.exit(1)
    
    topic = sys.argv[1]
    group_discussion(topic)
