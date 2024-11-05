docker build -t sit-distibuted-master .

docker run -p 8786:8786 -p 8787:8787 sit-distibuted-master --ip 192.168.1.5 --port 30000

python send.py --llm_name EleutherAI/pythia-14m
python send.py --llm_name TinyLlama/TinyLlama-1.1B-Chat-v0.1
python send.py