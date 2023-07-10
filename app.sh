#!/usr/bin/env bash

build_image(){
	docker build --tag  demo-image:lastest .
}

start(){
	build_image
        docker-compose up -d 
}

stop(){
	docker-compose down
}

config(){
    cp conf/dev.yaml setting.yaml
}


if [ "$1" == "start" ]; then
	echo "Starting the application..."
	config
	start
	sleep 2
	
	# create database
	curl http://localhost/create_db &>/dev/null
	
	# fetch data 
	curl http://localhost/retrieve_raw_data &>/dev/null
	
elif [ "$1" == "stop" ]; then
	echo "Stopping the application..."
	stop
else
	echo "Usage: $0 {start|stop}"
	exit 1
fi
