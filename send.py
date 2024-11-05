import argparse
import time
from cloudpooling import LLMEvalClient

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Client program to connect to a server.')
    parser.add_argument('--username', type=str, default="guest", help='Username to use for the task')
    parser.add_argument('--llm_name', type=str, default="EleutherAI/pythia-160m", help='LLM namespace from Hugging Face')
    args = parser.parse_args()
    
    start_time = time.time()
    client = LLMEvalClient('192.168.1.5', 8786)
    results = client.do_llm_eval(username=args.username, llm_name=args.llm_name)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Evaluation Results:", results)
    print(f"Execution time: {execution_time} seconds")
