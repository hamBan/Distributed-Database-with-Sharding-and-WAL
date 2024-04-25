# Checking if network exists
check_network:
	if [ -z "$$(sudo docker network ls -q -f name=my_network)" ]; then \
		echo "Network my_network does not exist. Creating..."; \
		sudo docker network create my_network; \
	else \
		echo "Network my_network already exists."; \
	fi

# To create volume and provide it to the server container
# run_volume:
# 	sudo docker volume create persistentStorage

# Building and running the containers
run: check_network
	sudo docker volume create persistentStorage
	echo "1"
	sudo docker build -t server ./Server
	echo "2"
	sudo docker build -t database ./database
	sudo docker build -t loadbalancer ./loadbalancer
	sudo docker build -t shard_manager ./Shard_Manager
	sudo docker run -d -p 5000:5000 --privileged=true -v /var/run/docker.sock:/var/run/docker.sock --name my_loadbalancer_app --network my_network -it loadbalancer
	sudo docker run -d --privileged=true -v /var/run/docker.sock:/var/run/docker.sock --name shard_manager --network my_network -it shard_manager
	python3 spawner.py 
	

# # Building and running the containers using docker-compose
# run_compose: check_network
# 	sudo docker-compose build
# 	sudo docker-compose up load_balancer

# # Testing 
# run_DB_Server: check_network
# 	sudo docker build -t database ./database
# 	sudo docker run -d --network my_network --name DB database
# 	sudo docker build -t my-server-app ./Server
# 	sudo docker run -d -p 5000:5000 -e "SERVER_ID=123456" -e "MYSQL_HOST=DB" --network my_network  --name server1 my-server-app

# # For DB
# run_DB: check_network
# 	sudo docker build -t database ./database
# 	sudo docker run -d --network my_network --name DB1 database
# 	sudo docker run -d --network my_network --name DB2 database

# # For Server
# run_Server: check_network
# 	sudo docker build -t my-server-app ./Server
# 	sudo docker run -d -p 5000:5000 -e "SERVER_ID=123456" -e "MYSQL_HOST=DB1" -e "SERVER_NAME=server1" --network my_network -v persistentStorage:/persistentStorageMedia --name server1 my-server-app
# 	sudo docker run -d -p 5001:5000 -e "SERVER_ID=123457" -e "MYSQL_HOST=DB2" -e "SERVER_NAME=server2" --network my_network -v persistentStorage:/persistentStorageMedia --name server2 my-server-app

# # Delete all
# run_delete:
# 	sudo docker stop $$(sudo docker ps -a -q)
# 	sudo docker rm $$(sudo docker ps -a -q)
# 	sudo docker rmi $$(sudo docker images -q)
# 	sudo docker network rm my_network
# 	sudo docker volume rm persistentStorage

# # For Server
# run_Server: check_network
# 	sudo docker build -t my-server-app ./Server
# 	sudo docker run -p 5000:5000 -e "SERVER_ID=123456" -e "MYSQL_HOST=DB1" --network my-network  --name server1 my-server-app
# 	sudo docker run -p 5001:5000 -e "SERVER_ID=123457" -e "MYSQL_HOST=DB2" --network my-network  --name server2 my-server-app
	

# sudo docker run -p 5000:5000 -e "SERVER_ID=123456" -e "MYSQL_HOST=DB1" -e "SERVER_NAME=server1" --network my_network -v persistentStorage:/persistentStorageMedia --name server1 my-server-app
# sudo docker run -p 5001:5000 -e "SERVER_ID=123457" -e "MYSQL_HOST=DB2" -e "SERVER_NAME=server2" --network my_network -v persistentStorage:/persistentStorageMedia --name server2 my-server-app

docker build -t loadbalancer ./loadbalancer
docker build -t shard_manager ./Shard_Manager
docker build -t server ./Server
docker rm -f $(docker ps -aq)
docker run -p 5000:5000 --privileged=true --name my_loadbalancer_app --network my_network -it loadbalancer
docker run --privileged=true -v persistentStorage:/persistentStorageMedia --name shard_manager --network my_network -it shard_manager

docker run -p 5000:5000 --privileged=true --name my_loadbalancer_app --network my_network -it loadbalancer
docker run --privileged=true --mount source=persistentStorage,destination=/persistentStorageMedia,target=/persistentStorageMedia --name shard_manager --network my_network -it shard_manager

final:
docker rm -f $(docker ps -aq)
docker volume rm persistentStorage
docker build -t loadbalancer ./loadbalancer
docker build -t shard_manager ./Shard_Manager
docker build -t server ./Server
docker run -p 5000:5000 --privileged=true --name my_loadbalancer_app --network my_network -it loadbalancer
docker run --privileged=true -v persistentStorage:/persistentStorageMedia --name shard_manager --network my_network -it shard_manager
python spawner.py