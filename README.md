Data Weather Application

Description
It’s a weather application that helps the user to get up-to-date information on weather conditions for any location around the world

Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
Prerequisites
Installing Docker Desktop : you can install it through this link https://www.docker.com/products/docker-desktop/ 
Installing
Clone this repository: git clone https://github.com/zeinebzayet/Weather_App.git 
Navigate to the project directory: cd Weather_App
Usage
Start the Docker containers: docker-compose up
Access the MongoDB container: docker exec -it mongodb bash
Access the Python container: docker exec -it python bash
Navigate to the workspace: cd workspace
Install the required dependencies: pip install -r requirements.txt
Access the  Kafka interface: http://localhost:8080/topics
Access the  Mongodb interface: http://localhost:8070
Run the application: python router.py
Access the home page: http://localhost:5005/index

Authors
Nada BEN TAARIT
Feriel BEN RJEB
Zeineb Zayet
Zeineb CHERNI
Aya RIDENE

Acknowledgments
This project was realized within the framework of an academic project for the Software Development Engineering speciality in the institute ISI - Ariana
