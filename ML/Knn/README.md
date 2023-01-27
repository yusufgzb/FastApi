İnstall GCP VM instances 

sudo apt-get update

sudo apt-get upgrade

sudo apt-get install docker.io

sudo docker -v

sudo docker build . -t fast_api_image

sudo docker run -p 8080:8080 --name fast_api_container fast_api_image
