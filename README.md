# transport parser
### How to use docker commands:
1. Create Docker image for the project
```
docker build -t ${PWD##*/}-image .
```
2. Run project's Docker container
```
docker run -d -p 4500:4500 -p 80:80 -p 6800:6800 -p 6900:6900 -v ${PWD}:/usr/src/app --name ${PWD##*/}-container ${PWD##*/}-image
```
3. Stop and remove project's Docker container
```
docker rm -f ${PWD##*/}-container
```
4. Remove project's Docker image
```
docker image rm -f ${PWD##*/}-image
```