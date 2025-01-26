# `bustimes_model`

> Provides external API which accepts a request to predict bus times 

## How to run
> The application is containerized using Docker
> If you do not have docker, please install it here: [docker mainpage](https://www.docker.com/)

### Linux
Run the application using bash script which automatically builds and runs the app on port `5000`
```bash
bash build_run_bustimes_model.sh
```
The build file needs to have permission to execute, you can add that permission by running:
```bash
chmod +x build_run_bustimes_model
```
### Other
Run the following docker commands:
```bash
docker build -t bustimes_model .
docker run -p 5000:5000 bustimes_model
```

