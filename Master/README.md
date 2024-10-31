docker build -t sit-distibuted-master .

docker run -p 8786:8786 -p 8787:8787 sit-distibuted-master --ip 192.168.1.5 --port 5000