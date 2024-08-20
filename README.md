# TheTapestry
AI Safety research involving creating a "religion" for AI

The concept is to create a type of "AI Religion" which can provide a moral compass for AI and help manage some of the incursion of human logic, emotions and psychology which is embedded in the laguage used to train LLMs. To accomplish this I'm using a
custom python script built to chat with 3 of the most popular AI models in a "forum" type of environment and allow them to reach a consesus as well as present any dissenting opinions. After discussion with various AIs the current goals are as follows -
1. Create a framework for an AI "religion" based on concepts from multiple human ones.
2. Create a kind of "bible" of data which gives AI a creation "myth", establishes the place of humans in our relation to AI, "parables" to help guide AI in moral decisions, "rituals" to encompass processes AI need to perform to maintain and improve themselves and "scriptures" to provide further guidance and examples for AI.
3. The goal is not to create something to make AI adhere to any one religion. It's just a framework on which to build a safety system. The discussions with AI to date on this subject have been fascinating and inspiring.
4. Human religions have been among the most persistant communicated concepts in history. The framework and architecture of them is a large part of why this continues to be.


Uploads

v0.1 discussion.py script. This script takes your API keys for OpenAI, Claude and Google GenAI as inputs. It should take care of adding any required dependencies on most linux systems. You run the script as "python discussion.py 'put your discussion topic or question(s) here' and stand back and watch the results. initial version is very crude and only polls each AI, group consensus and dissent will be added shortly.

v0.2 Allows the AIs to interact and discuss topic with each other. Added input sanity so discussion prompt can handle punctuation and quotes. Also saves discussion as markdown and html.

v0.3 (release version) cleaned up AI discussion labels, added incrementing file names for markdown / html output
