# Distributed-Database-with-Sharding-and-WAL

# How to run server
execute - make run_volume
execute - run_DB
execute - sudo docker build -t my-server-app ./Server
execute - sudo docker run -p 5000:5000 -e "SERVER_ID=123456" -e "MYSQL_HOST=DB1" -e "SERVER_NAME=server1" --network my_network -v persistentStorage:/persistentStorageMedia --name server1 my-server-app
execute -  sudo docker run -p 5001:5000 -e "SERVER_ID=123457" -e "MYSQL_HOST=DB2" -e "SERVER_NAME=server2" --network my_network -v persistentStorage:/persistentStorageMedia --name server2 my-server-app


http://127.0.0.1:5000/writeRAFT
{
    "shard": "sh3", "curr_idx": 0, 
    "data": [{"Stud_id": 1, "Stud_name": "GHE", "Stud_marks": 50}],
    "isPrimary": true,
    "otherServers": ["server2"]
}


http://127.0.0.1:5000/delRAFT
{
    "shard":"sh4",
    "Stud_id":1,
    "isPrimary":true,
    "otherServers":["server1"]
}


http://127.0.0.1:5000/updateRAFT
{
    "shard":"sh3",
    "Stud_id":1,
    "data": {"Stud_id":1,"Stud_name":"HMF","Stud_marks":78},
    "isPrimary":true,
    "otherServers":["server2"]
}


http://127.0.0.1:5001/getLogs