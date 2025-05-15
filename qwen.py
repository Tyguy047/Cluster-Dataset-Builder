# Interacts with the Qwen LLM via LM Studio
# You need to have an LM Studio server running with Qwen3-0.6B installed in order for this part of the program to work!

import lmstudio as lms
from dotenv import load_dotenv
import os
import re
import universal

load_dotenv()
QWEN_MODEL = os.getenv('QWEN_MODEL')
MODEL = lms.llm(QWEN_MODEL)

def qwenOutput(USER_INPUT):

    result = MODEL.respond(USER_INPUT)

    with open('outputs/qwen.txt', 'w', encoding='utf-8') as qwen_output:
        qwen_output.write(str(result))


def qwenVote(USER_INPUT):
    # Pass USER_INPUT to the voteInput function
    VOTE_INPUT = universal.voteInput(USER_INPUT)

    # result = MODEL.respond(f"{VOTE_INPUT}\nYou may not vote option 3!")
    result = MODEL.respond(f"{VOTE_INPUT}")
    
    cleaned_result = re.sub(r'<think>.*?</think>', '', str(result), flags = re.DOTALL)
    vote_number = "".join(filter(str.isdigit, cleaned_result))

    with open('vote.txt', 'a', encoding='utf-8') as vote_file:
        vote_file.write(vote_number + '\n')