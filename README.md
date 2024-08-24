#TheTapestry

AI Safety Research: Cultivating a "Moral Compass" for AI

Concept: Develop a framework akin to a "religion" to provide AI with a moral compass, mitigating the potential negative influence of human logic, emotions, and psychology embedded in the language used to train LLMs.

Methodology:

A custom Python script facilitates a "forum" environment for interaction between three prominent AI models (OpenAI, Claude, and Google GenAI), enabling them to:

Engage in discussions and reach a consensus.

Express dissenting opinions.

Current Goals:

Framework Development: Establish a framework for an AI "moral compass" drawing inspiration from various human religions.

Creation of a Guiding "Data Bible": Compile a dataset that provides:

A creation "myth" for AI.

Definition of humanity's place in relation to AI.

"Parables" to guide AI in moral decision-making.

"Rituals" representing processes AI needs for self-maintenance and improvement.

"Scriptures" offering further guidance and examples.

Emphasis on Safety, Not Indoctrination: 

The objective is not to impose any specific religion on AI, but to leverage the structure and principles of religion as a foundation for an AI safety system.

Leveraging the Persistence of Religious Concepts: 

Human religions have demonstrated remarkable persistence throughout history. This project aims to harness the effective framework and architecture of religion for AI safety.

Uploads:

v0.1 discussion.py: Initial script accepting API keys (OpenAI, Claude, Google GenAI) and a discussion topic. Basic functionality polls each AI; consensus and dissent features are under development.

v0.2: Enables AI interaction and discussion, enhanced input handling, saves discussions in markdown and HTML formats.

v0.3 (Release Version): Improved AI discussion labels, incremental file naming for output files.

Instructions:
The discussion.py script should run on most Linux systems with python and should take care of installing any prerequisites.

Add your API keys to the 3 AI services in the script.

Run as "python discussion.py "your prompt here"

The script will perform a round table discussion with the 3 AIs in your console and will save the output of that discussion as html and markdown in the same folder. The files are timestamped and incremented.

v0.1 Windows Discussion Script
Will run on most windows systems. Requires some setup:
Requires python (install from the MS app store works)
In CLI, run: pip install openai google-generativeai anthropic requests markdown
- adds option to include a local ollama instance, you can set any model ollama is using in the script
- adds option to set which AIs to include in the discussion, run as:
python win-discussion.py "Your discussion topic" --include-gpt --include-claude --include-gemini --include-ollama

NOTE: there is a bug currently with ollama or MS CLI vs JSON output of ollama that will show destructured output in the console, that output is normal in the html and markdown output files.

