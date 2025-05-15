from openai import OpenAI
from dotenv import load_dotenv
import os
from universal import voteInput
import re
import json

load_dotenv()
agent_endpoint = os.getenv('DEEPSEEK_API_ENDPOINT') + "/api/v1/" 
agent_access_key = os.getenv('DEEPSEEK_API')

client = OpenAI(
    base_url = agent_endpoint,
    api_key = agent_access_key,
)

def deepseekOutput(USER_INPUT):

    response = client.chat.completions.create(
        model = "n/a",
        messages=[
            {"role": "user", "content": f"{USER_INPUT}"}
        ],
        temperature = 0.7
    )

    with open('outputs/deepseek.txt', 'w') as deepseek_output:
        deepseek_output.write(response.choices[0].message.content)

def deepseekVote(USER_INPUT):
    VOTE_INPUT = voteInput(USER_INPUT)

    response = client.chat.completions.create(
        model = "n/a",
        messages=[
            {"role": "user", "content": f"{VOTE_INPUT}\nYou may not vote option 2!"}
        ],
        temperature = 0.7
    )

    response_content = response.choices[0].message.content
    match = re.search(r'\d+', response_content)
    
    vote_to_write = ""
    if match:
        vote_to_write = match.group(0)

    with open('vote.txt', 'a') as deepseek_vote:
        if vote_to_write:
            deepseek_vote.write(vote_to_write + "\n")
        else:
            pass