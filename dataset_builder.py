import deepseek as ds
import gemini as gem
import phi
import json
from google import genai
import re
import os
from dotenv import load_dotenv
load_dotenv()

def askCluster():
    with open('asked.txt', 'r') as asked:
        ASKED = asked.read()

    GEMINI_API = os.getenv('GEMINI_API')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL')
    client = genai.Client(api_key = GEMINI_API)

    response = client.models.generate_content(
        model = GEMINI_MODEL,
        contents = f"Please output only a complex question that I will have answer. It must not apear in this list, since these are questions that are already answered (questisons and answers will be used to train an AI model for your every day user. Please questions that will be good for this use! Make sure theres no pattern tha the inputs folow they all need to be structured differently for good training!):\n{ASKED}"
    )

    INPUT = response.text

    with open('asked.txt', 'a', encoding='utf-8') as gemini_output:
        gemini_output.write(f"{INPUT}\n")
    return INPUT

def openOutputs():
    with open('outputs/gemini.txt', 'r') as gemini_file:
        global GEMINI_OUTPUT
        GEMINI_OUTPUT = gemini_file.read()

    with open('outputs/deepseek.txt', 'r') as deepseek_output:
        global DEEPSEEK_OUTPUT
        DEEPSEEK_OUTPUT = deepseek_output.read()

    with open('outputs/phi.txt', 'r') as phi_output:
        global PHI_OUTPUT
        PHI_OUTPUT = phi_output.read()

def winningVote():
    with open('vote.txt', 'r') as vote_file:
        votes = vote_file.read().strip()
    
    if not votes:
        return None

    vote_counts = {}
    for vote in votes:
        if vote.isdigit():
            vote_counts[vote] = vote_counts.get(vote, 0) + 1
    
    if not vote_counts:
        return None

    # Find the number with the highest count
    most_frequent_vote = max(vote_counts, key=vote_counts.get)
    return most_frequent_vote

if __name__ == '__main__':
    print()
    print("Starting Synthetic Dataset Generation...")
    print("-" * 40)
    while True:

        with open('outputs/gemini.txt', 'w') as gemini_clear:
            gemini_clear.write("")

        with open('outputs/deepseek.txt', 'w') as deepseek_clear:
            deepseek_clear.write("")

        with open('outputs/phi.txt', 'w') as phi_clear:
            phi_clear.write("")

        with open('vote.txt', 'w') as vote_file:
            vote_file.write("")

        with open('asked.txt', 'r') as asked_file:
            lines = asked_file.readlines()

        with open('asked.txt', 'w') as asked_file:
            for line in lines:
                if line.strip():
                    asked_file.write(line)

        USER_INPUT = askCluster() # For automated AI inputs
        # USER_INPUT = input('>>>: ') # For manual inputs

        print("Synthetic Input Generation By Gemini Complete!")
        print()
        gem.geminiOutput(USER_INPUT)
        print("Gemini Output Complete")
        ds.deepseekOutput(USER_INPUT)
        print("DeepSeek Output Complete")
        phi.phiOutput(USER_INPUT)
        print("Phi Output Complete")

        print()
        print("AI Responces Generated!")
        print()

        gem.geminiVote(USER_INPUT)
        print("Gemini Vote Complete")
        ds.deepseekVote(USER_INPUT)
        print("DeepSeek Vote Complete")
        phi.phiVote(USER_INPUT)
        print("Phi Vote Complete")
        print()
        print("Voting Complete!")
        print()
        
        openOutputs()
        OUTPUT = winningVote()

        print("-" * 40)
        if OUTPUT == '1':
            with open('new_dataset.jsonl', 'a') as dataset:
                dataset.write(json.dumps({"user_input": USER_INPUT, "output": GEMINI_OUTPUT}) + '\n')
                print("Gemini, has added to the dataset!")

        elif OUTPUT == '2':
            cleaned_deepseek_output = re.sub(r'<think>.*?</think>', '', DEEPSEEK_OUTPUT, flags=re.DOTALL).strip()
            with open('new_dataset.jsonl', 'a') as dataset:
                dataset.write(json.dumps({"user_input": USER_INPUT, "output": cleaned_deepseek_output}) + '\n')
            print("DeepSeek, has added to the dataset!")

        elif OUTPUT == '3':
            cleaned_phi_output = re.sub(r'<think>.*?</think>', '', PHI_OUTPUT, flags=re.DOTALL).strip()
            with open('new_dataset.jsonl', 'a') as dataset:
                dataset.write(json.dumps({"user_input": USER_INPUT, "output": cleaned_phi_output}) + '\n')
            print("Phi has added to the dataset!")

        else:
            print("No model added to the dataset!")

        print("-" * 40)