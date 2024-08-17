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
        'anthropic',
        'markdown'
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
    
import argparse    
from openai import OpenAI
import google.generativeai as genai
import anthropic
import time
import sys
import markdown

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
    conversation = [f"# AI Group Discussion\n\n## Topic: {topic}\n"]
    
    for round in range(rounds):
        conversation.append(f"\n### Round {round + 1}:\n")
        
        # GPT's turn
        gpt_prompt = f"Based on the discussion so far, provide your thoughts and ask a question to the other AIs:\n\n{''.join(conversation)}"
        gpt_response = get_gpt_response(gpt_prompt)
        conversation.append(f"**GPT:** {gpt_response}\n\n")
        print("GPT:", gpt_response)
        
        # Claude's turn
        claude_prompt = f"Considering the conversation history and GPT's response, share your perspective and pose a question:\n\n{''.join(conversation)}"
        claude_response = get_claude_response(claude_prompt)
        conversation.append(f"**Claude:** {claude_response}\n\n")
        print("Claude:", claude_response)
        
        # Gemini's turn
        gemini_prompt = f"Given the ongoing discussion, offer your insights and ask a question to continue the dialogue:\n\n{''.join(conversation)}"
        gemini_response = get_gemini_response(gemini_prompt)
        conversation.append(f"**Gemini:** {gemini_response}\n\n")
        print("Gemini:", gemini_response)
        
        time.sleep(2)  # Pause between rounds
    
    # Final consensus and dissenting opinion
    consensus_prompt = "Based on the entire discussion above, what is the general consensus? If there are any dissenting opinions, please state them as well."
    
    conversation.append("\n## Final Consensus and Dissenting Opinions:\n")
    
    gpt_consensus = get_gpt_response(consensus_prompt + "\n\n" + "".join(conversation))
    conversation.append(f"**GPT Consensus:** {gpt_consensus}\n\n")
    
    claude_consensus = get_claude_response(consensus_prompt + "\n\n" + "".join(conversation))
    conversation.append(f"**Claude Consensus:** {claude_consensus}\n\n")
    
    gemini_consensus = get_gemini_response(consensus_prompt + "\n\n" + "".join(conversation))
    conversation.append(f"**Gemini Consensus:** {gemini_consensus}\n\n")
    
    return "".join(conversation)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Group Discussion Generator")
    parser.add_argument("topic", type=str, help="The topic for AI discussion. Enclose in quotes if it contains spaces or special characters.")
    args = parser.parse_args()

    discussion_output = group_discussion(args.topic)
    
    # Save the output as a Markdown file
    with open("ai_discussion_output.md", "w", encoding='utf-8') as f:
        f.write(discussion_output)
    
    # Convert Markdown to HTML (optional)
    html_output = markdown.markdown(discussion_output)
    with open("ai_discussion_output.html", "w", encoding='utf-8') as f:
        f.write(html_output)
    
    print("\nDiscussion saved to ai_discussion_output.md and ai_discussion_output.html")
