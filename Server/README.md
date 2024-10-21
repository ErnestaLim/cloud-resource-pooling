docker build -t sit-distibuted-server .

docker run -p 5000:5000 -it sit-distibuted-server /bin/bash