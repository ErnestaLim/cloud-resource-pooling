docker build -t sit-distributed-slave .

docker run -p 51592:51592 --gpus=all --restart=on-failure sit-distributed-slave --ip 192.168.1.5 --port 30000 --storage_ip 192.168.1.5 --storage_port 51592
docker run -p 51593:51592 --gpus=all --restart=on-failure sit-distributed-slave --ip 192.168.1.5 --port 30000 --storage_ip 192.168.1.5 --storage_port 51593

docker run -p 51594:51592 --gpus=all --restart=on-failure sit-distributed-slave --ip 192.168.1.5 --port 30000 --storage_ip 192.168.1.5 --storage_port 51594
docker run -p 51595:51592 --gpus=all --restart=on-failure sit-distributed-slave --ip 192.168.1.5 --port 30000 --storage_ip 192.168.1.5 --storage_port 51595
docker run -p 51596:51592 --gpus=all --restart=on-failure sit-distributed-slave --ip 192.168.1.5 --port 30000 --storage_ip 192.168.1.5 --storage_port 51596
docker run -p 51597:51592 --gpus=all --restart=on-failure sit-distributed-slave --ip 192.168.1.5 --port 30000 --storage_ip 192.168.1.5 --storage_port 51597

lm_eval --model hf --model_args pretrained=EleutherAI/pythia-160m,trust_remote_code=True --tasks tinyMMLU --device cuda:0 --output_path output