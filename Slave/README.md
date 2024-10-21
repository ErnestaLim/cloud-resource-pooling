docker build -t sit-distributed-slave .

docker run --network host --gpus=all sit-distributed-slave

lm_eval --model hf --model_args pretrained=EleutherAI/pythia-160m,trust_remote_code=True --tasks tinyMMLU --device cuda:0 --output_path output