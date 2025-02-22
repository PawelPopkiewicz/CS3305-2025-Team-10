# Inference Container
> Provides inference service which predicts the arrival of a bus to the next bus stop

## API Endpoints
|Endpoint|Method|Note|
|--|--|--|
|`/report`|GET|returns a report about the model in use (latest) date of model creation + other models|
|`/predictions`|POST|send json with trip info and returns estimated time of arrival, uses latest model|
|`/predictions/<model_id>`|Use a specific model|
|`/training_jobs`|POST|start a training job, returns a `model_id`|
|`/training_jobs/<model_id>`|GET|Returns the status of the training job|
