docker build -t sit-distibuted-server .

docker run --network host -p 5000:5000 sit-distibuted-server