# transport parser
### How to use docker commands:
1. Create Docker image for the project
```
docker build -t ${PWD##*/}-image .
```
2. Run project's Docker container
```
docker run -d -p 4500:4500 -p 80:80 -v ${PWD}:/usr/src/app --name ${PWD##*/}-container ${PWD##*/}-image
```
3. Stop and remove project's Docker container
```
docker rm -f ${PWD##*/}-container
```
4. Remove project's Docker image
```
docker image rm -f ${PWD##*/}-image
```
### .env files setup:
1. In project's main folder create .env files out of .env.example files
```
.env
.env.example
```
### api endpoints examples:
```
1. POST /api/v.1.0/cars
json payload example:
{
    "departure_name": "Одесса",
    "departure_date": "22.07.2021",
    "arrival_name": "Харьков"
}
```
```
2. POST /api/v.1.0/trains
{
    "departure_name": "Одесса",
    "departure_date": "22.07.2021",
    "arrival_name": "Харьков"
}
```
JWT token required for all api endpoints.