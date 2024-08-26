#TheTapestry

AI Safety Research:

Concept: Develop a framework to allow collaboration between the user and multiple AIs

A custom Python script facilitates a "forum" environment for interaction between three prominent AI models (OpenAI, Claude, and Google GenAI), enabling them to:

Engage in discussions and reach a consensus.

Express dissenting opinions.

Uploads:

v0.1 discussion.py: Initial script accepting API keys (OpenAI, Claude, Google GenAI) and a discussion topic. Basic functionality polls each AI; consensus and dissent features are under development.

v0.2: Enables AI interaction and discussion, enhanced input handling, saves discussions in markdown and HTML formats.

v0.3 (Release Version): Improved AI discussion labels, incremental file naming for output files.

v0.1 Windows Discussion Script with local ollama option

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
NOTE: the win-discussion.py script will work on Linux also currently, this may change with future updates

