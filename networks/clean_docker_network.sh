docker rm -f $(docker ps -a -q)
docker network rm test_subnet
