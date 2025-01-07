# This module should be run after running clean.py.
# Effectively, it prompts ChatGPT/Other LLM with data/Prompt.txt in order to get standardized results to be stored.
# Currently, this is a manual process since I don't have ChatGPT API nor do I want to set one up.
# I've experienced success by pasting Prompt.txt and copy/pasting 50 lines at a time.

def clean(input_dir, output_dir):
    pass


if __name__ == "__main__":
    clean("../generated/years_messages", "../generated/cleaned")
