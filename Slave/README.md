docker build -t sit-distributed-slave .

docker run --gpus=all --restart=on-failure sit-distributed-slave --ip 192.168.1.5 --port 5000
docker run -p 10101:51592 --gpus=all --restart=on-failure sit-distributed-slave --ip 192.168.1.5 --port 5000

lm_eval --model hf --model_args pretrained=EleutherAI/pythia-160m,trust_remote_code=True --tasks tinyMMLU --device cuda:0 --output_path output