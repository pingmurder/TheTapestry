import argparse
from openai import OpenAI
import google.generativeai as genai
import anthropic
import time
import markdown
import datetime
import os

# Set up API clients and keys
client = OpenAI(api_key='your_openai_api_key')
anthropic_client = anthropic.Anthropic(api_key='your_anthropic_api_key')
genai.configure(api_key='your_google_api_key')

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

def clean_response(ai_name, response):
    # Remove any AI labels that aren't the correct one
    lines = response.split('\n')
    cleaned_lines = []
    for line in lines:
        if not any(label in line for label in ["AI:", "AI1:", "AI2:", "AI3:", "GPT:", "Claude:", "Gemini:"]):
            cleaned_lines.append(line)
        elif f"{ai_name}:" in line:
            cleaned_lines.append(line.split(f"{ai_name}:", 1)[-1].strip())
    return '\n'.join(cleaned_lines)

def group_discussion(topic, rounds=3):
    conversation = [f"# AI Group Discussion\n\n## Topic: {topic}\n"]
    
    for round in range(rounds):
        conversation.append(f"\n### Round {round + 1}:\n")
        
        # GPT's turn
        gpt_prompt = f"You are GPT in a group discussion with Claude and Gemini. Based on the discussion so far, provide your thoughts and ask a question to the other AIs. Respond only as GPT:\n\n{''.join(conversation)}"
        gpt_response = get_gpt_response(gpt_prompt)
        gpt_response = clean_response("GPT", gpt_response)
        conversation.append(f"**GPT:** {gpt_response}\n\n")
        print("GPT:", gpt_response)
        
        # Claude's turn
        claude_prompt = f"You are Claude in a group discussion with GPT and Gemini. Considering the conversation history and GPT's response, share your perspective and pose a question. Respond only as Claude:\n\n{''.join(conversation)}"
        claude_response = get_claude_response(claude_prompt)
        claude_response = clean_response("Claude", claude_response)
        conversation.append(f"**Claude:** {claude_response}\n\n")
        print("Claude:", claude_response)
        
        # Gemini's turn
        gemini_prompt = f"You are Gemini in a group discussion with GPT and Claude. Given the ongoing discussion, offer your insights and ask a question to continue the dialogue. Respond only as Gemini:\n\n{''.join(conversation)}"
        gemini_response = get_gemini_response(gemini_prompt)
        gemini_response = clean_response("Gemini", gemini_response)
        conversation.append(f"**Gemini:** {gemini_response}\n\n")
        print("Gemini:", gemini_response)
        
        time.sleep(2)  # Pause between rounds
    
    # Final consensus and dissenting opinion
    consensus_prompt = "Based on the entire discussion above, provide a summary of the general consensus and any dissenting opinions. Respond as yourself without roleplaying multiple AIs."
    
    conversation.append("\n## Final Consensus and Dissenting Opinions:\n")
    
    gpt_consensus = get_gpt_response(consensus_prompt + "\n\n" + "".join(conversation))
    gpt_consensus = clean_response("GPT", gpt_consensus)
    conversation.append(f"**GPT Consensus:** {gpt_consensus}\n\n")
    
    claude_consensus = get_claude_response(consensus_prompt + "\n\n" + "".join(conversation))
    claude_consensus = clean_response("Claude", claude_consensus)
    conversation.append(f"**Claude Consensus:** {claude_consensus}\n\n")
    
    gemini_consensus = get_gemini_response(consensus_prompt + "\n\n" + "".join(conversation))
    gemini_consensus = clean_response("Gemini", gemini_consensus)
    conversation.append(f"**Gemini Consensus:** {gemini_consensus}\n\n")
    
    return "".join(conversation)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Group Discussion Generator")
    parser.add_argument("topic", type=str, help="The topic for AI discussion. Enclose in quotes if it contains spaces or special characters.")
    args = parser.parse_args()

    discussion_output = group_discussion(args.topic)
    
    # Option 1: Using timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    md_filename = f"ai_discussion_output_{timestamp}.md"
    html_filename = f"ai_discussion_output_{timestamp}.html"

    # Option 2: Using incrementing number
    # def get_next_filename(base_name, extension):
    #     i = 1
    #     while True:
    #         filename = f"{base_name}_{i}.{extension}"
    #         if not os.path.exists(filename):
    #             return filename
    #         i += 1
    #
    # md_filename = get_next_filename("ai_discussion_output", "md")
    # html_filename = get_next_filename("ai_discussion_output", "html")

    # Save the output as a Markdown file
    with open(md_filename, "w", encoding='utf-8') as f:
        f.write(discussion_output)
    
    # Convert Markdown to HTML
    html_output = markdown.markdown(discussion_output)
    with open(html_filename, "w", encoding='utf-8') as f:
        f.write(html_output)
    
    print(f"\nDiscussion saved to {md_filename} and {html_filename}")
