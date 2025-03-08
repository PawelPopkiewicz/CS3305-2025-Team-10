# Busig
> AI-Powered Bus Predictions

Busig is an app which aims to provide a seamless, smooth and simple way to access bus time data, such as the location of buses, stops, schedules and mainly predictions. It was developed mainly because me (Radek Zajicek) and Liam Cotter commute every workday and we found the existing solutions not satisfactory. 

The main issues include cluttered, out of date, "laggy" interface which would be extra frustrating to use for example while holding a cup of coffee and waiting for a bus stop, or when running late to a bus, etc. This frustration guided our front end development and design, instead of for example providing a path finding algorithm to find the route from place A to place B, we already figured google maps does a good enough job and most commuters already know perfectly which bus they would like to take and where. So instead we focused on the daily commuters who already are accustomed to the city. This led to minimal and simple GUI, focus on performance of the map and small number of pages. 

Another issues where the absurdly inaccurate predictions given to users. I am sure many people know what we are talking about, but for the lucky among our readers, here is a typical experience: You want to go to work in the morning from a satellite town which should have regular buses every 20 minutes into the city centre, however that is never true and there are many mornings when there is a one hour gap or more. Secondly when you look at the app the most you can hope for is that it will show you that a bus exists and will eventually arrive, if you are lucky anyway, sometimes they do not exist, sometimes they do exist but they start skipping stops, and mainly, they arrive way later than predicted, we are talking "Arrival in 5 minutes" but actually you wait for 30 minutes. This problem with unpredictable buses is driving the daily commuters away from mass transport, as many studies have shown. Overall the reasons to look for better predictions and provide them to the public are very relevant and needed.

This led us to mainly focus on our data and predictions we could make with it. Instead of focusing on routing algorithms, payments of tickets through the app, etc. our predictions our front stage and center. We needed to dedicate different components just for these predictions and train our own Encoder Decoder AI model. In the end we have managed to get our predictions working and provide them to the user in a nice simple GUI. 

# Overall Architecture

Our architecture is following the latest trend of micro-services, because we realized our program is easy to modularize. This means we would put our code in Docker containers which would then talk to each other through http restful API implemented in flask. In the future when our app would be available for the wider public we could use Kubernetes to organize and deploy a cluster of the containers, ensuring scalability, elasticity and robustness. Especially if we would choose a cloud solution such a Google Kubernetes Engine. For now however all of the containers are orchestrated using the docker compose functionality. Implemented in the docker-compose.yaml file. This takes care of setting up a shared network among the containers, building them, adding variables to their environments, persisting data using docker volumes which maps a part of the local file space to the space in the container and more. Instead of cloud our app currently runs on a home ubuntu server which is enough for development needs. 

Later we will showcase different parts of our system and go through the containers one by one, however to give a sense of the overall architecture, I will list them here first:
- Bus Model
    - Maintains the current state of the bus data
    - Responsible for providing the up to date data to the gateway
    - Currently fetches the real-time and static data itself
    - Fetches and stores the static data in PostgreSQL
- Gateway
    - Connects the model to the clients
    - Answers the requests from the client
    - Serves as a proxy to decouple the front facing responsibility from the bus model
- Training Data Collection
    - Receives the json real-time data from Bus model after it is fetched
    - Processes the data and stores it in mongodb container
    - Provides API to return the contents of the mongodb, mainly to Inference container
- Inference
    - Handles preprocessing the training data 
    - Converts the training data to csv files to train on
    - Loads the model for inference
    - Carries out inference with data provided by the API
- Front-End
    - Fetches data from the gateway
    - Displays the live data to the user 
    - Implements a map to show data with ease

We mainly fetch from the TFI API which provides us with real-time updates on buses and potentially other vehicles in Ireland. This is important to mention because we have ran into some troubles when it comes to the data consistency, which has set us back, you can keep this in mind when some of our code seems a bit too much, for example rebuilding the database every day, etc. 

In the future, we would like to introduce Redis to cache the bus data, use asynchronous calls to inference for predictions and introduce a new container which would handle the fetching of data and put it inside a data processing pipeline before ultimately sending the data to the bus model.

# Bad Data

One of the main issues we had to deal with was inconsistent data. The inconsistency comes from the static data mainly. Of course real-time can report a bus which is off-route, not scheduled, etc., but that is to be expected and can be filtered out. However static data is provided as a zip file in csv formatted text files online. This is okay as we can simply download the file, unzip it, process the csv data, turn it into a relational tables and use it. However the main issue is that id fields which are used as primary keys CHANGE. And they change frequently and without a notification. This means a route id for the route "220" might change overnight with no reason to, trip id changes as well, but at a different rate, etc. 

The way to combat this was to build the PostgreSQL periodically, let's say every day to prevent out of data ids. This means the creation of the tables needed to be optimized for speed, because there are millions of rows to process, filter out, index, etc. This was eventually achieved by constructing optimized filter queries, using pandas and constructing indexes for fast lookups. 

A second issue now is that the training data can become stale, since there is a lot of preprocessing that needs to be done to get from a set of coordinates and timestamps associated with a trip id to a set of stops and time they were passed at, we need the PostgreSQL database for preprocessing as well, however the data in the "up-to-date" database might not be compatible with the collected data week ago. We are still working to resolve this, we will start storing snapshots of the database each time it is updated and also convert the raw json data into csv datasets because the datasets are actually static data agnostic, meaning they do not rely on static data and thus do not go stale. 

## Bus model
## Inference
Inference is the container which takes care of the AI predictions. This means the inference itself, in other words using the already trained model to predict new times. But also it handles preprocessing the raw json data into the csv files, which is quite a complex task. You might ask where does this model come from? Well it is not really represented in our architecture, because it was prototyped and trained in google colab.

To make sense of the workflow, the model and the usage of the model, let me split this section into multiple parts: at first I will walk you through the data preprocessing needed to train the model. After we are familiar with the data I will explain the model itself, its architecture, the reasons behind choosing such architecture, the training, results and troubleshooting. When you know where this model came from I will explain how it is deployed and queried in the inference container. 

### Preprocessing
### Model Architecture and Training
### Deployment
## Training data collection
## Front end (maybe divided into more chapters)
## Flow (Events triggering changes in the architecture)
# Summary
# Lessons learned
# Contributions
## Radek
## Liam
## Pawel
## Alex
