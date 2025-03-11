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
  - Responsible for providing the up-to-date data to the gateway
  - Currently fetches the real-time and static data itself
  - Fetches and stores the static data in PostgreSQL
- Gateway
  - Connects the model to the clients
  - Answers the requests from the client
  - Serves as a proxy to decouple the front facing responsibility from the bus model
- Training Data Collection
  - Receives the JSON real-time data from Bus model after it is fetched
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

One of the main issues we had to deal with was inconsistent data. The inconsistency comes from the static data mainly. Of course real-time can report a bus which is off-route, not scheduled, etc., but that is to be expected and can be filtered out. However static data is provided as a ZIP file in CSV formatted text files online. This is okay as we can simply download the file, unzip it, process the CSV data, turn it into a relational tables and use it. However the main issue is that id fields which are used as primary keys CHANGE. And they change frequently and without a notification. This means a route id for the route "220" might change overnight with no reason to, trip id changes as well, but at a different rate, etc.

The way to combat this was to build the PostgreSQL periodically, let's say every day to prevent out of data ids. This means the creation of the tables needed to be optimized for speed, because there are millions of rows to process, filter out, index, etc. This was eventually achieved by constructing optimized filter queries, using pandas and constructing indexes for fast lookups.

A second issue now is that the training data can become stale, since there is a lot of preprocessing that needs to be done to get from a set of coordinates and timestamps associated with a trip id to a set of stops and time they were passed at, we need the PostgreSQL database for preprocessing as well, however the data in the "up-to-date" database might not be compatible with the collected data week ago. We are still working to resolve this, we will start storing snapshots of the database each time it is updated and also convert the raw json data into csv datasets because the datasets are actually static data agnostic, meaning they do not rely on static data and thus do not go stale.

### Bus model

bap

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

The purpose of training data collection is to collect the data from GTFS Realtime, filter it and store it in a non-wasteful format. At the start this container has queried the API itself, because the bus model was not implemented yet fully. However it would be wasteful to query it twice, so now the bus model container simply passes the received JSON files to the training data collection container. 

The data is filtered to only contain city Cork buses, this was done to only contain buses with similar routes. In the future new bus routes which are longer distance will be tested to see how they function with our model.  

Afterwards the data is processed to a different format. Instead of a lot of individual updates I create one trip document with an array of vehicle updates, to reduce the size of the stored data.

### Front end (maybe divided into more chapters)

### Flow (Events triggering changes in the architecture)

The flow of the program can be nicely separated into different events which trigger functions in the containers. These events are usually new information, but also requests from the client side. Here is a quick break down:

|Event|Flow triggered|Duration|
|--|--|--|
|Real-time update|bus model fetches data, which is then stored by training data collection. If there is a new update, inference is asked to update its prediction|1 min|
|Static update|bus model fetches the latest static data and rebuilds the PostgreSQL, it also sends the new route id to name dictionary to inference|~1day|
|Client update|Client queries gateway for updated bus data, it then fetches this info from bus model|~1 min|
|Client request|Client requests more detailed info, queries gateway which then queries the bus model|Unscripted|

During development we have used this prototype of a diagram to assist us:

--->>> Insert the architecture drawing 

I have found that thinking about our architecture in this way is helpful to conceptualize the architecture and connect components together. Also when extending our functionality you should ask yourself which flow does this fit in and if it does not fit into any of them, then it is probably not needed. 

#### Real-time update

In further detail, the real-time update is triggered by a cronjob which start running automatically on running the bus model container every minute. At first the data is fetched from the endpoint: `https://api.nationaltransport.ie/gtfsr/v2/vehicles`. What is helpful is that this endpoint is standardized over different transport providers, which makes our code further expendable to new locations. 

Then the responsibility of the bus model container after receiving this information is to send it to the training data collection container, which processes it as described above. Furthermore the bus model keeps track of the current live buses and they should have the most up to date predictions for them, so they are ready to go when the client requests them. So if new information is received, new predictions need to be made. Therefore inference is contacted and its predictions are stored in the bus model. 

#### Static update

As mentioned in the bad data section, the static data is highly unstable and needs to be updated regularly. The scripts to do so are located in the bus model container, since it is responsible for providing the up to date information. The scripts download the zip file containing the static data from `https://www.transportforireland.ie/transitData/Data/GTFS_Realtime.zip`, then unzipped into a directory using a bash script, which afterwards call the python script to create tables, populate them with the data from the unzipped files and filter them to only contain the data we care about. 

Since the PostgreSQL database is centralized, not many other actions need to be made in this flow, except for one. `route_id_to_name`is often used to filter out the trips we care about, because it contains only the route ids of routes we choose to track. It is stored in PostgreSQL as a table with two attributes, the route id and the name of the route. However an issue arises when a container stores this mapping of route ids on startup, because the route ids might change while it is running and then the stored data becomes stale. To prevent simply fetching the data periodically, the bus model pushes it to the containers that need it on the event of the static data update. Currently it only services the inference container. This probably made you think about publisher subscriber architecture and it is the same principle, however we did not go full out on the publisher subscriber architecture for example using Redis, because we deemed it a bit of an overkill. 

## Summary

In this report we have shown that the architecture of our system is modular, separated into Docker containers for the many benefits that it brings. These benefits are collaboration, abstraction, reusability, scalability and elasticity if we deploy our containers in a cluster. Afterwards we have went through the individual containers and explained their respective functionality, focusing on justifying the choices made about the design, explaining where future improvements could be made and explaining the function in high level abstractions. 

Furthermore we have shown how these containers connect to each other in the flow section of the report. In our view the flow ties everything together and it is a great perspective on our architecture which improves understanding and helps us and potential contributors stay on the right track when it comes to implementing features. The reader should now have a good understanding of the different components, what they do and how they help achieve the overall goal of providing real-time information about buses. The reader should also be aware of the potential drawbacks in our design, how they could be addressed and hopefully also learned from our observations during development. 

Overall our architecture provides up to date information on buses which it fetches from GTFS. We store the data fetched in order to provide new training data for our AI model. This model is then used to infer the arrival times of the buses which are currently on the roads, focusing on reliability of our predictions and understanding the limitations of our model. All of this real-time state of the buses is managed by the bus model container, which offers extensive API endpoints to fetch the latest information. These endpoints are mainly accessed by our gateway container which acts as a sort of proxy to sit in between the client requests and the bus model. This helps with decoupling and for example introducing security in the future. All of this data is then displayed by the front end code, which aims to provide a fast, smooth, simple experience to its users. Integrating a map significantly improved the user experience.

Finally our goal of providing a simple, smooth experience of looking up credible information on real-time bus data was achieved, however there are still many areas we aim to improve in the near future. 

## Lessons learned

The architecture of our system is modularized in containers. This has helped us collaborate between each other, because all was needed to do was define APIs well between the containers. Afterwards we could work on our own containers and collaborate on the things that matter such as overall architecture, satisfying the use cases, etc. while abstracting the implementation details. This had a surprising effect on our collaboration as well, because our understanding of individual containers we have not worked on was not in depth, we were more critical of each others work and everyone else served as a sort of product manager, checking that the development is useful for the use cases mainly. This helped us focus on our goals and not stray too far into implementation rabbit holes and details. It was also interesting see how important mutual respect was as well during development, because otherwise this criticality of others work would hinder collaboration. 

Defining the API endpoints is a crucial step during development of modularized architecture, so it should be done as soon as possible to prevent one developer waiting on the definition of an API to continue his work. Another reason to do so is to write dummy containers which would be used for testing, which is something we would greatly benefit from, especially when it comes to the development of the front-end code, because often front end developers where waiting on the back end to be implemented to test out their features. 

Another important takeaway is to keep your code on main a functional version of your program that other developers can use as a jumping off point to develop their code further. This lends itself into developing in small incremental changes instead of massive features all at once. We found ourselves all too often merging development branches while leaving the main behind because the code on main was simply outdated and the massive features the branches were used for were too big to be considered "done" to be merged into main, because the are always somewhat unfinished. So instead of doing this we would dedicate the branches to smaller, manageable features which can be implemented, tested and then pushed to main. Instead of basically abusing branches to just do our own thing the whole time and merging the branches if someone needed our updates. 

On the topic of merging code to main, we now really appreciate CI/CD pipelines, which would make our life much much more easier and less stressful. If we had more time we would definitely focus on setting up the pipelines as soon as possible. This would also allow us to push code straight to our home server which Radek has setup, but because during most of the development cycle the main was either too outdated to work with the front end in its current state or somewhat broken, we ended not using our server nearly at all. 

The CI/CD pipelines would also involve a lot of tests. I do not need to stress how important are tests during development and the lack of automated testing was really a burden on all of us, the main issue was that we had so much code to write that test were simply an afterthought. I am not sure if so pressed for time tests are still something that needs to be automated, because we are not super familiar with testing frameworks, so it would take some time to set it up and put everyone on board. However it is one of our priorities now to have a decent test coverage of our code, since the MVP is functional, so we can focus on cementing the current architecture in place and make it more stable. If we knew we had more time, our focus would definitely shift towards testing more. 

Although big design up front is something seen as a bit outdated, I think our team would still benefit from spending a little bit more time in the initial design phase and mapping out a clear step by step plan on how to achieve what we have wanted. Although we have individually managed the tasks we needed to do individually, it is equally if not more important to manage to time plan as a group. So in the future we would definitely focus more on planning out our weeks and holding ourselves accountable to meet the team deadlines. 

Communication among team members is also very important, mainly explaining the reasoning behind your choices to the rest of the team, without focusing too much on the technical detail. This improves mutual understanding and nurtures the collaborative environment. 

## Contributions

As discussed before, the collaboration between team members was nicely separated because we have worked on separate containers when it comes to the back end. The front end was of course more coupled, so the workflows between Alex and Pawel overlap.

### Radek

Learned about and created the Docker containers for our system. This included creating the Dockerfiles for each of the containers, orchestrating the deployment using the docker compose yaml file and using docker hub to transfer the images to my home server. Furthermore I have given a quick tutorial on how to use docker, how to deploy it on your own machine and how to run code inside it for testing. 

Inside the docker containers I have also helped setup the Flask APIs, this means setting the dependencies and running the server using Gunicorn. I had to also manage the networking between the containers, which involved setting up a network which they share and exposing the ports needed. Finally I had to set up port mapping on my home route in order to expose the services to the WAN. 

Installed Ubuntu server on my old laptop, set up the networking on that laptop to provide static IP and also implemented basic security with firewall and ssh. I then ran ad managed the server for the duration of the training data collection, sometimes debugging and troubleshooting it. 

I have written the code to collect the training data, this involves connecting to the API endpoint, deciding on which routes to collect, filtering the data accordingly, designing the structure of the mongodb collection to store the collected data efficiently and writing the code to convert the raw data to the more storage efficient form.

Setup the mongodb container with authentication and managing the connection to that database with pymongo. Wrote insert queries to insert the converted collected data into the collection. Also wrote some basic queries to check the state of the database which help to monitor its health. 

This training data collection container also has a RESTful API which allows it to communicate with other containers, usually for the purpose of providing the collected data.

In order to filter the data out I also needed to implement the static data database, which at first I have done with SQLite but later migrated all of that code to PostgreSQL. This means designing the database schema to store static data such as routes, trips, stops, etc., setting up the dependencies and cascades on the database, which proved harder than it looks because the way PostgreSQL handles cascades can be incredibly inefficient, so sometimes even though the reference is there, it is better to not write it for performance reasons. I have then wrote the code to filter out the database which was also quite tricky to optimize thanks to the sizes of the tables which can go into millions of rows for some of them. And of course we needed the code to be efficient, because this database would be rebuild essentially every day. This also involved setting up indexes on the tables to allow for faster filtering and faster queries down the line.

I have written the bash script to download the zip file, unzip it and create the relational PostgreSQL database with it. Which was initially inside the training data collection container but later I moved it to the bus model.

I have developed the inference container. First of all by preprocessing the collected training data and converting it into a dataset which can be trained on. This was one of the most challenging parts of the entire project, because I needed to map the coordinates associated with timestamps and a trip id to much more rich data, such as when were stops passed on that trip with distances to them on that trip, etc. All of this is too complicated to put down in text, but it involved designing a very efficient way to query the databases on the tables which contain millions of rows (sometimes you would need to join these tables together, which would need to be done efficiently, otherwise the amount of rows to process would be in billions). 

After designing the queries needed I still needed to develop the code which would use those queries in order to process the data into something the model would use. This was not so simple because of course you need to know the model architecture to pre-process the data for it, but you need to know which data you are working with to design the model. So these two design phases happened in tandem, so often I would reiterate on the model architecture and change the data accordingly, then I would find a nicer representation of the data and change the model, etc. Eventually I have developed a trip manager class which converts the training and in the future extended it to preprocess the data for inference as well. 

The model itself was developed in google colab. Firstly I have decided to use Encoder Decoder after reading research papers, then used the library pytorch which handles most of the code for me, all I needed to do was make the existing model architecture fit with my specific data I wanted the model to predict. When eventually the code was compiling I still needed to actually train the model which involves a lot of iterations and adjusting hyper parameters. This was the case for me as well, I have adjusted the epochs, number of trips the model tried to predict, introduced randomness into the dataset to help with generalization and resolved the issue of the first stop prediction with the overlap as I mentioned before. Eventually I have gotten good results on the test dataset.

Finally I have deployed the model in the inference container and provided the API routes to access this model. This involved creating a wrapper class around the model which handled the inference, loading the model and data manipulation. 

I have also created the architecture diagram and played a big role in designing the architecture because I was in charge of the containerization. And as everyone else I have worked on the presentation, helped with the design of the one page report and I wrote most of the project report, except for the containers and contributions which I have not worked on personally.

### Liam

###  Pawel

###  Alex
