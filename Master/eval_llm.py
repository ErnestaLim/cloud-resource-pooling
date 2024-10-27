from dask.distributed import Client
import subprocess, os, glob, json

# Config
output_dir = "output/EleutherAI__pythia-160m"

# Connect to the Dask scheduler
client = Client('localhost:8786')

# Define a sample task (e.g., a simple computation)
def compute_task():
    # Run a command and capture its output
    command = "lm_eval --model hf --model_args pretrained=EleutherAI/pythia-160m,trust_remote_code=True --tasks tinyMMLU --device cuda:0 --output_path output"  # Example command, you can replace it with any command you need
    result = subprocess.run(command, shell=True, check=True)

    # Find the latest JSON file in the output/EleutherAI/pythia-160m directory
    json_files = glob.glob(os.path.join(output_dir, "*.json"))
    
    if not json_files:
        return {
            'message': "No JSON files found in the directory."
        }

    # Get the latest JSON file based on modification time
    latest_json_file = max(json_files, key=os.path.getmtime)

    # Read the content of the JSON file
    with open(latest_json_file, 'r') as f:
        json_content = json.load(f)

    # Return both the computation result and the JSON content
    return {
        'message': "Successfully evaluated LLM.",
        'json_content': json_content
    }

def save_result_to_file(result, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Define the file path for saving the result
    output_file_path = os.path.join(output_dir, "result_output.json")

    # Save the result to a JSON file
    with open(output_file_path, 'w') as f:
        json.dump(result, f, indent=4)

    print(f"Result saved to {output_file_path}")

# Submit the task to the scheduler
future = client.submit(compute_task)

# Get the result once the worker completes the task
result = future.result()
save_result_to_file(result["json_content"], output_dir)

print("Result:", result["message"])