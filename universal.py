def voteInput(USER_INPUT):

    with open('outputs/gemini.txt', 'r') as gemini_output:
        GEMINI_OUTPUT = gemini_output.read()

    with open('outputs/deepseek.txt', 'r') as deepseek_output_file:
        DEEPSEEK_OUTPUT = deepseek_output_file.read()

    with open('outputs/phi.txt', 'r') as phi_output_file:
        PHI_OUTPUT = phi_output_file.read()

    return (f"""
I asked the question "{USER_INPUT}" and got these responses from a few different AI models. Which do you think is the best?

Here is the first one:
{GEMINI_OUTPUT}
If you think that is the best, please only respond with the number "1".

The second one I got was:
{DEEPSEEK_OUTPUT}
If you think that is the best, please only respond with the number "2".

Here is the third responce:
{PHI_OUTPUT}
If you think this one is the best, please only respond with the number "3".
""")