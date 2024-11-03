import argparse
from cloudpooling import LLMEvalClient

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Client program to connect to a server.')
    parser.add_argument('--username', type=str, default="guest", help='Username to use for the task')
    parser.add_argument('--llm_name', type=str, default="EleutherAI/pythia-160m", help='LLM namespace from Hugging Face')
    args = parser.parse_args()
    
    client = LLMEvalClient('192.168.1.5', 8786)
    results = client.do_llm_eval(username=args.username, llm_name=args.llm_name)
    print("Evaluation Results:", results)
