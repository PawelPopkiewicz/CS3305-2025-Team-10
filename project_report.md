# Busig
> AI-Powered Bus Predictions

Busig is an app which aims to provide a seamless, smooth and simple way to access bus time data, such as the location of buses, stops, schedules and mainly predictions. It was developed mainly because me (Radek Zajicek) and Liam Cotter commute every workday and we found the existing solutions not satisfactory.

The main issues include cluttered, out of date, "laggy" interface which would be extra frustrating to use for example while holding a cup of coffee and waiting for a bus stop, or when running late to a bus, etc. This frustration guided our front end development and design, instead of for example providing a path finding algorithm to find the route from place A to place B, we already figured google maps does a good enough job and most commuters already know perfectly which bus they would like to take and where. So instead we focused on the daily commuters who already are accustomed to the city. This led to minimal and simple GUI, focus on performance of the map and small number of pages.

Another issues where the absurdly inaccurate predictions given to users. I am sure many people know what we are talking about, but for the lucky among our readers, here is a typical experience: You want to go to work in the morning from a satellite town which should have regular buses every 20 minutes into the city centre, however that is never true and there are many mornings when there is a one hour gap or more. Secondly when you look at the app the most you can hope for is that it will show you that a bus exists and will eventually arrive, if you are lucky anyway, sometimes they do not exist, sometimes they do exist but they start skipping stops, and mainly, they arrive way later than predicted, we are talking "Arrival in 5 minutes" but actually you wait for 30 minutes. This problem with unpredictable buses is driving the daily commuters away from mass transport, as many studies have shown. Overall the reasons to look for better predictions and provide them to the public are very relevant and needed.

This led us to mainly focus on our data and predictions we could make with it. Instead of focusing on routing algorithms, payments of tickets through the app, etc. our predictions our front stage and center. We needed to dedicate different components just for these predictions and train our own Encoder Decoder AI model. In the end we have managed to get our predictions working and provide them to the user in a nice simple GUI.

# Glossary
> The terms used need definitions beyond the colloqial meaning

|Term|Definition|
|--|--|
|Route|Collection of trips following a similar path, think of `220`|
|Trip|One instance of a bus trip, repeats weekly, think of `220` leaving at Ovens at 10:00 and arriving in Carrigaline at 13:00|
|Shape|The shape of the path a specific trip follows|
|Stop|Straightforward, just a bus stop|
|Distance|Distance from the beginning of the trip in meters|
|(Vehicle) Updates|Real-time updates, a timestamp and a location of a bus given in coordinates|

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

## Bad Data

One of the main issues we had to deal with was inconsistent data. The inconsistency comes from the static data mainly. Of course real-time can report a bus which is off-route, not scheduled, etc., but that is to be expected and can be filtered out. However static data is provided as a zip file in csv formatted text files online. This is okay as we can simply download the file, unzip it, process the csv data, turn it into a relational tables and use it. However the main issue is that id fields which are used as primary keys CHANGE. And they change frequently and without a notification. This means a route id for the route "220" might change overnight with no reason to, trip id changes as well, but at a different rate, etc.

The way to combat this was to build the PostgreSQL periodically, let's say every day to prevent out of data ids. This means the creation of the tables needed to be optimized for speed, because there are millions of rows to process, filter out, index, etc. This was eventually achieved by constructing optimized filter queries, using pandas and constructing indexes for fast lookups.

A second issue now is that the training data can become stale, since there is a lot of preprocessing that needs to be done to get from a set of coordinates and timestamps associated with a trip id to a set of stops and time they were passed at, we need the PostgreSQL database for preprocessing as well, however the data in the "up-to-date" database might not be compatible with the collected data week ago. We are still working to resolve this, we will start storing snapshots of the database each time it is updated and also convert the raw json data into csv datasets because the datasets are actually static data agnostic, meaning they do not rely on static data and thus do not go stale.

### Bus model

### Inference

Inference is the container which takes care of the AI predictions. This means the inference itself, in other words using the already trained model to predict new times. But also it handles preprocessing the raw json data into the csv files, which is quite a complex task. You might ask where does this model come from? Well it is not really represented in our architecture, because it was prototyped and trained in google colab.

To make sense of the workflow, the model and the usage of the model, let me split this section into multiple parts: at first I will walk you through the data preprocessing needed to train the model. After we are familiar with the data I will explain the model itself, its architecture, the reasons behind choosing such architecture, the training, results and troubleshooting. When you know where this model came from I will explain how it is deployed and queried in the inference container.

#### Preprocessing

Preprocessing our data was crucial in order to extract useful information for the model to learn from. The methodology I used to pick the features and shape of data to feed the model was along the lines of "if I cannot make a reasonable estimate from the data, the model cannot either." So for example simply giving the model coordinates and timestamps with the hopes it would predict the next ones would be naive.

The first step in this procedure is to decide how to encode time. In other words how to encode the fact that the bus is progressing through time. As raw data the updates (coordinates + timestamps) are at random intervals, ~ 2 mins apart. That is quite bad for our model as it does not transition nicely to the arrival time at stops which we are ultimately interested in. Instead I decided to structure the data in bus stops. So we would give the model information about bus stops, first the observed ones, ie the stops which the bus already passed with information of arrival time, scheduled arrival time, time in the day and distance along the route. 

Converting the updates into bus stops is not straightforward. First I fetch all of the stops for this trip, calculate the distance of that stop from the beginning of the trip (using shapes table). During processing I keep track of the processed ones with an index. Then I start going through the updates, if a stop (or more) happen to be between these updates, I use linear interpolation to estimate the arrival time. This is possible because I know the distance travelled for the stops and the updates too, this gives me a nice correlation. So assuming the bus travels at constant speed (this also means it never stops) then it would arrive at that bus stop in x amount of time. For example if update 1 is 100 meters and update 2 is 200 meters and our bus stop is 175 meters far, then our interpolation ratio would be (175 - 100) / (200 - 100) = 0.75. And if update one would be at 10 seconds and update 2 at 18 seconds, then the stop was passed at 0.75 * (18 - 10) + 10 = 16 seconds. This might seem like a bad estimation, but overall it preserves the progress of the trip perfectly and slight deviations in the exact arrival time are okay as long as the overall speed through the trip is preserved. The fact our model does not account for idling times at stops seems like an oversight, but when researchers have tried to deal with this issue, they ended up creating two models, one to predict the travel and the other to predict the stop times, but without an incredible improvement boost. Instead I assume that there is a high correlation between high waiting times and slow travel, meaning if the model can learn that the trip is going slowly, the longer idle times will be naturally modeled as well, so I do not see a reason to focus on idle prediction yet. I would like to add that better techniques exist, such as spline interpolation, however that was beyond my scope as of now.  

Now that we have stops with estimated arrival times, we can do further engineering to give our model an easier time during training. First of all it is a common practice to predict the relative error to the scheduled time. For example if the bus arrived at 14:25 but was scheduled for 14:22, then the relative error is 3 minutes. We can track the relative error across the stops and it forms quite a nice smooth curve, which makes it really nice to predict. Another advantage is that it gives the model a reference point, so the error further into the future does not deviate drastically. Although it is important to mention that the relative error will increase further into the future thanks to the entropy of the system. This is quite significant in our ideology, because we aim to build trust with the user of the application to trust the prediction. If we would try to predict too far into the future it would be impossible to provide consistent results, therefore we introduce a hard stop of ~15 stops and we do not predict further than that.

Another factor to focus on is that the model will be recurant, effectively this means the model sees just one bus stop at a time and iterates over them. Our data should reflect that, so instead of for example providing the scheduled arrival times as is, I provide the scheduled time to the next bus stop and also the distance to the next bus stop, etc. This helps the model if the relative error will decrease or increase (For example longer stretches between usually mean a decrease, etc.). 

Last aspect I want to talk about is the normalization of values. This essentially means that the values should be in a similar range. For this reason I subtract the current delay from all of the times fed into the model, meaning the relative error is always 0 at the start, this helps with cases like an hour delay or more, which might throw off the model, even though the actual trip has normal times between stops. Of course this delay is then added after inference. 

So now we are ready to take a look at the example training data from the dataset:

#### Model Architecture

I will start by mentioning that the architecture was not my idea and it is well documented and widely used design. The idea to use it for this specific task of bus predictions came actually from one of the research papers which attempted to predict bus times with an Encoder Decoder architecture. The basic idea of encoder-decoder is that the encoder sees some data and "encodes" or extracts some relevant information about that data, specifically this extracted information is in a form of a _hidden context vector_ which in our model has the dimension of 120. Using this approach makes sense if we assume that there is some nice abstraction or attribute of our system which is relevant for our predictions and can be extracted from the data. In our case that is true, what I assume is happening is that the hidden context vector is encoding the state of the traffic and the state of the bus. So if the bus is crowded it might start skipping stops, if it is at night, the bus might skip most stops because they are empty and there is less traffic. However I did not carry out analysis of the model which is usually quite hard to do, so I am only guessing this is what is happening. 

The job of the decoder then is to take this _hidden state vector_ and use it to predict further stops. You can notice now that the hidden vector as a kind of bottle neck for the information that can be carried over to the predictions. As we will find later, this is something that is good for our model but also cause some issues, because it might abstract away too much information, which for example is good to find out the state of the traffic and "forget" stops which were passed longer time ago, but knowing the exact relative error for the last few stops would be quite helpful and the hidden vector does abstract away from this as well. This causes our model to badly predict the relative error of the first stop and then predict the second one with just a few seconds off from the first one. I will explain how to remedy this later. 

But how do we feed the model all of the stop? We also have a variable number of stops which are observed and a variable which are targets for our prediction, so we need our model to be quite flexible. This can be achieved by using the recurant approach which we have mentioned before. So essentially go stop by stop until the end. This is incorporated into the encoder decoder by putting an LSTM (Long Short Term Memory) model inside both the encoder and the decoder. These are Recurrent Neural Networks (RNNs for short) meaning they process the stops one by one, each step producing a hidden vector which is fed into the next iteration together with the stop information. LSTM is special because it also introduces a forgetful component which essentially learns to forget unimportant information or keep important information for longer. The reason to choose an LSTM among other RNNs was quite arbitrary, however it is known to perform better than classical ones. In the future it might be worth looking into different ones as well. 

Another important detail is that we use small neural networks to embed components into a single vector. So if we are giving each stop the "time to stop", "distance to stop" and the "time" all of these three get embedded together, same goes for trip information, like the day in the week and the route.

So the overall prediction looks like this:
1. Extract trip features and embed them
2. Use them as the first hidden vector in the Encoder and feed the observed stops to the LSTM inside the encoder
3. Give the hidden vector given to us by the LSTM inside encoder to the decoder 
4. In the decoder go though the target stops and predict the relative errors for each one of them

#### Training

Training was done inside google colab, because it provides a notebook environment which is helpful when debugging and prototyping. Furthermore google colab provides free compute resources to train the model. 

I have collected around 4000 trips which are fit for training, so for example the bus does not go off route, there are enough stops passed, etc. The final model trained on all of these in 40 epochs. The training/validation/test split was 70/15/15. Traditional MSE was used and optimizer was Adam. 

During training the model did not go through many changes, unlike the format of the data which was iterated on multiple times, here is presented only the final version. The main issue in the training was that the model had a hard time predicting the first stop in the trip, which is actually quite unintuitive, it would make sense that the first stop should be easiest to predict and the further ones will be harder. So as explained before, this is caused by the architecture of encoder decoder, which essentially splits the two LSTMs into two, therefore the first pass in the decoder has actually the hardest job at predicting, because it has the least amount of previous information in the RNN. This is currently remedied by quite a brute solution, I simply let the decoder see an overlap in the observed stops. So currently last 2 stops which are observed 
are fed into the decoder as well, to give it an easier start. In the future I am thinking of improving the model in some way to solve it in a nicer way, however this method did reduce the first error significantly, so it has its merits.

I have also figured out that a decent number of stops into the future is about 15, anything further than that causes to model to have a hard time training, because of the high entropy, so whatever the model tries, the data will eventually deviate too much in the end. 

#### Deployment

Currently the preprocessing of the data is done inside the inference container. This is also true for the inference, in other words the process of using the trained model to predict new information. Therefore when the model is deployed, I receive the raw json data and I convert it into a csv in the same format as the training data. An important detail to mention which causes some headaches during debugging is that we simulate "batching". This is the practice of separating training data into batches to improve performance. However this means that the model is expecting information one dimension higher than just one trip. So when we feed the information into the model, we create a batch of size one. 

The model also needs to be loaded into memory to be used, because this takes few seconds, I load the model once on startup of the container and keep it inside a wrapper class around that model. Afterwards the model is idle until a prediction request arrives through the RESTful API. In the future this preprocessing should be done in the class which is querying the model to reduce the response time. It should also happen async. 

### Training data collection

### Front end (maybe divided into more chapters)

### Flow (Events triggering changes in the architecture)

## Summary

## Lessons learned

## Contributions

### Radek

### Liam

###  Pawel

###  Alex
