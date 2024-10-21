docker build -t sit-distibuted-master .

docker run --network host -p 8786:8786 sit-distibuted-master