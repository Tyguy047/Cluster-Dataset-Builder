from dotenv import load_dotenv
import os
from google import genai
import universal

load_dotenv()
GEMINI_API = os.getenv('GEMINI_API')
GEMINI_MODEL = os.getenv('GEMINI_MODEL')
client = genai.Client(api_key = GEMINI_API)

if not GEMINI_API:
    print("Error! You are missing your Gemini API key from the .env file")
    exit(1)

def geminiOutput(USER_INPUT):
    
    response = client.models.generate_content(
        model = GEMINI_MODEL,
        contents = USER_INPUT
    )

    with open('outputs/gemini.txt', 'w', encoding='utf-8') as gemini_output:
        gemini_output.write(response.text)

def geminiVote(USER_INPUT):

    VOTE_INPUT = universal.voteInput(USER_INPUT)
    response = client.models.generate_content(
        model = GEMINI_MODEL,
        contents = f"{VOTE_INPUT}\nYou may not vote option 1!"
        )
    with open('vote.txt', 'a', encoding='utf-8') as vote_file:
        vote_file.write(response.text)