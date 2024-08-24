import argparse
import datetime
import os
import time
import json
import requests
import markdown
from openai import OpenAI
import google.generativeai as genai
import anthropic

# Set up API clients and keys
client = OpenAI(api_key='your api key here')
anthropic_client = anthropic.Anthropic(api_key='your api key here')
genai.configure(api_key='your api key here')
# Initialize AI models
gpt_model = "gpt-4"
claude_model = "claude-2"
gemini_model = genai.GenerativeModel('gemini-pro')
ollama_model = "llama3.1"  # You can change this to any model available in your Ollama instance

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

def get_ollama_response(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": ollama_model,
        "prompt": prompt
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        response_text = response.text
        print(f"Ollama response text: {response_text}")  # Debugging: print the entire response text
        
        # Initialize a list to hold the concatenated response parts
        complete_response = []
        
        # Split the response text by newlines and parse each JSON object
        for line in response_text.splitlines():
            try:
                json_response = json.loads(line)
                if isinstance(json_response, dict) and 'response' in json_response:
                    complete_response.append(json_response['response'])
                else:
                    print(f"Unexpected JSON format: {json_response}")
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print(f"Response line: {line}")
        
        # Join the response parts to form the complete response
        return ''.join(complete_response)
        
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return "Error: Unable to get response from Ollama"

def clean_response(ai_name, response):
    lines = response.split('\n')
    cleaned_lines = []
    for line in lines:
        if not any(label in line for label in ["AI:", "AI1:", "AI2:", "AI3:", "GPT:", "Claude:", "Gemini:", "Ollama:"]):
            cleaned_lines.append(line)
        elif f"{ai_name}:" in line:
            cleaned_lines.append(line.split(f"{ai_name}:", 1)[-1].strip())
    return '\n'.join(cleaned_lines)

def group_discussion(topic, rounds=3, include_gpt=True, include_claude=True, include_gemini=True, include_ollama=False):
    conversation = [f"# AI Group Discussion\n\n## Topic: {topic}\n"]
    participants = []
    if include_gpt:
        participants.append("GPT")
    if include_claude:
        participants.append("Claude")
    if include_gemini:
        participants.append("Gemini")
    if include_ollama:
        participants.append("Ollama")
    
    for round in range(rounds):
        conversation.append(f"\n### Round {round + 1}:\n")
        
        for participant in participants:
            prompt = f"You are {participant} in a group discussion with {', '.join([p for p in participants if p != participant])}. Based on the discussion so far, provide your thoughts and ask a question to the other AIs. Respond only as {participant}:\n\n{''.join(conversation)}"
            
            if participant == "GPT":
                response = get_gpt_response(prompt)
            elif participant == "Claude":
                response = get_claude_response(prompt)
            elif participant == "Gemini":
                response = get_gemini_response(prompt)
            elif participant == "Ollama":
                response = get_ollama_response(prompt)
            
            response = clean_response(participant, response)
            conversation.append(f"**{participant}:** {response}\n\n")
            print(f"{participant}:", response)
        
        time.sleep(2)  # Pause between rounds
    
    # Final consensus and dissenting opinion
    consensus_prompt = "Based on the entire discussion above, provide a summary of the general consensus and any dissenting opinions. Respond as yourself without roleplaying multiple AIs."
    
    conversation.append("\n## Final Consensus and Dissenting Opinions:\n")
    
    for participant in participants:
        if participant == "GPT":
            consensus = get_gpt_response(consensus_prompt + "\n\n" + "".join(conversation))
        elif participant == "Claude":
            consensus = get_claude_response(consensus_prompt + "\n\n" + "".join(conversation))
        elif participant == "Gemini":
            consensus = get_gemini_response(consensus_prompt + "\n\n" + "".join(conversation))
        elif participant == "Ollama":
            consensus = get_ollama_response(consensus_prompt + "\n\n" + "".join(conversation))
        
        consensus = clean_response(participant, consensus)
        conversation.append(f"**{participant} Consensus:** {consensus}\n\n")
    
    return "".join(conversation)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Group Discussion Generator")
    parser.add_argument("topic", type=str, help="The topic for AI discussion. Enclose in quotes if it contains spaces or special characters.")
    parser.add_argument("--include-gpt", action="store_true", help="Include GPT in the discussion")
    parser.add_argument("--include-claude", action="store_true", help="Include Claude in the discussion")
    parser.add_argument("--include-gemini", action="store_true", help="Include Gemini in the discussion")
    parser.add_argument("--include-ollama", action="store_true", help="Include Ollama in the discussion")
    parser.add_argument("--rounds", type=int, default=3, help="Number of discussion rounds (default: 3)")
    args = parser.parse_args()

    if not (args.include_gpt or args.include_claude or args.include_gemini or args.include_ollama):
        print("Error: At least one AI must be included in the discussion.")
        exit(1)

    discussion_output = group_discussion(
        args.topic,
        rounds=args.rounds,
        include_gpt=args.include_gpt,
        include_claude=args.include_claude,
        include_gemini=args.include_gemini,
        include_ollama=args.include_ollama
    )
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    md_filename = f"ai_discussion_output_{timestamp}.md"
    html_filename = f"ai_discussion_output_{timestamp}.html"

    with open(md_filename, "w", encoding='utf-8') as f:
        f.write(discussion_output)
    
    html_output = markdown.markdown(discussion_output)
    with open(html_filename, "w", encoding='utf-8') as f:
        f.write(html_output)
    
    print(f"\nDiscussion saved to {md_filename} and {html_filename}")
