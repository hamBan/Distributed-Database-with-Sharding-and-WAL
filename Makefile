# Checking if network exists
check_network:
	if [ -z "$$(sudo docker network ls -q -f name=my_network)" ]; then \
		echo "Network my_network does not exist. Creating..."; \
		sudo docker network create my_network; \
	else \
		echo "Network my_network already exists."; \
	fi


# Building and running the containers
run: check_network
	sudo docker build -t my-server-app ./Server
	sudo docker build -t loadbalancer ./loadBalancer
	sudo docker run -p 5000:5000 --privileged=true -v /var/run/docker.sock:/var/run/docker.sock --name my_loadbalancer_app --network my_network -it loadbalancer

# Building and running the containers using docker-compose
run_compose: check_network
	sudo docker-compose build
	sudo docker-compose up load_balancer

# Testing 
run_DB_Server: check_network
	sudo docker build -t database ./database
	sudo docker run -d --network my-network --name DB database
	sudo docker build -t my-server-app ./Server
	sudo docker run -d -p 5000:5000 -e "SERVER_ID=123456" -e "MYSQL_HOST=DB" --network my-network  --name server1 my-server-app

# For DB
run_DB: check_network
	sudo docker build -t database ./database
	sudo docker run -d --network my-network --name DB1 database
	sudo docker run -d --network my-network --name DB2 database

# For Server
run_Server: check_network
	sudo docker build -t my-server-app ./Server
	sudo docker run -d -p 5000:5000 -e "SERVER_ID=123456" -e "MYSQL_HOST=DB1" --network my-network  --name server1 my-server-app
	sudo docker run -d -p 5001:5000 -e "SERVER_ID=123457" -e "MYSQL_HOST=DB2" --network my-network  --name server2 my-server-app

# Delete all
run_delete:
	sudo docker stop $$(sudo docker ps -a -q)
	sudo docker rm $$(sudo docker ps -a -q)
	sudo docker rmi $$(sudo docker images -q)
	sudo docker network rm my_network

# # For Server
# run_Server: check_network
# 	sudo docker build -t my-server-app ./Server
# 	sudo docker run -p 5000:5000 -e "SERVER_ID=123456" -e "MYSQL_HOST=DB1" --network my-network  --name server1 my-server-app
# 	sudo docker run -p 5001:5000 -e "SERVER_ID=123457" -e "MYSQL_HOST=DB2" --network my-network  --name server2 my-server-app