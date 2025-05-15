from openai import OpenAI
from dotenv import load_dotenv
import os
from universal import voteInput
import re
load_dotenv()

OPENROUTER_API = os.getenv('PHI_API')
OPENROUTER_MODEL = os.getenv('PHI_MODEL')
client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = OPENROUTER_API,
    )

def phiOutput(USER_INPUT):
    completion = client.chat.completions.create(
    model = OPENROUTER_MODEL,
    messages = [
        {
        "role": "user",
        "content": USER_INPUT
        }
        ]
    )
    with open('outputs/phi.txt', 'w') as phi_output_file:
        phi_output_file.write(completion.choices[0].message.content)

def phiVote(USER_INPUT):

    VOTE_INPUT = voteInput(USER_INPUT)

    completion = client.chat.completions.create(
    model = OPENROUTER_MODEL,
    messages = [
        {
        "role": "user",
        "content": (f"{VOTE_INPUT}\nYou may not vote option 3!")
        }
        ]
    )
    
    response_content = completion.choices[0].message.content
    
    match = re.search(r'\d+', response_content)
    
    vote_to_write = ""
    if match:
        vote_to_write = match.group(0)

    with open('vote.txt', 'a') as phi_vote:
        if vote_to_write:
            phi_vote.write(vote_to_write + "\n")
        else:
            pass