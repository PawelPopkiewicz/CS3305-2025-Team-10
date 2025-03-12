# Busig

> AI-Powered Bus Predictions

Busig is an app which aims to provide a seamless, smooth and simple way to access bus time data, such as the location of buses, stops, schedules and mainly predictions. It was developed mainly because me (Radek Zajicek) and Liam Cotter commute every workday and we found the existing solutions not satisfactory.

The main issues include cluttered, out of date, "laggy" interface which would be extra frustrating to use for example while holding a cup of coffee and waiting for a bus stop, or when running late to a bus, etc. This frustration guided our front end development and design, instead of for example providing a path finding algorithm to find the route from place A to place B, we already figured Google Maps does a good enough job and most commuters already know perfectly which bus they would like to take and where. So instead we focused on the daily commuters who already are accustomed to the city. This led to minimal and simple GUI, focus on performance of the map and small number of pages.

Another issues where the absurdly inaccurate predictions given to users. I am sure many people know what we are talking about, but for the lucky among our readers, here is a typical experience: You want to go to work in the morning from a satellite town which should have regular buses every 20 minutes into the city centre, however that is never true and there are many mornings when there is a one-hour gap or more. Secondly when you look at the app the most you can hope for is that it will show you that a bus exists and will eventually arrive, if you are lucky anyway, sometimes they do not exist, sometimes they do exist but they start skipping stops, and mainly, they arrive way later than predicted, we are talking "Arrival in 5 minutes" but actually you wait for 30 minutes. This problem with unpredictable buses is driving the daily commuters away from mass transport, as many studies have shown. Overall the reasons to look for better predictions and provide them to the public are very relevant and needed.

This led us to mainly focus on our data and predictions we could make with it. Instead of focusing on routing algorithms, payments of tickets through the app, etc. our predictions our front stage and center. We needed to dedicate different components just for these predictions and train our own Encoder Decoder AI model. In the end we have managed to get our predictions working and provide them to the user in a nice simple GUI.

## Glossary

> The terms used need definitions beyond the colloquial meaning

| Term              | Definition                                                                                                                |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Route             | Collection of trips following a similar path, think of `220`                                                              |
| Trip              | One instance of a bus trip, repeats weekly, think of `220` leaving at Ovens at 10:00 and arriving in Carrigaline at 13:00 |
| Shape             | The shape of the path a specific trip follows                                                                             |
| Stop              | Straightforward, just a bus stop                                                                                          |
| Distance          | Distance from the beginning of the trip in meters                                                                         |
| (Vehicle) Updates | Real-time updates, a timestamp and a location of a bus given in coordinates                                               |

## Overall Architecture

Our architecture is following the latest trend of microservices, because we realized our program is easy to modularize. This means we would put our code in Docker containers which would then talk to each other through http restful API implemented in flask. In the future when our app would be available for the wider public we could use Kubernetes to organize and deploy a cluster of the containers, ensuring scalability, elasticity and robustness. Especially if we would choose a cloud solution such a Google Kubernetes Engine. For now however all of the containers are orchestrated using the docker compose functionality. Implemented in the docker-compose.yaml file. This takes care of setting up a shared network among the containers, building them, adding variables to their environments, persisting data using docker volumes which maps a part of the local file space to the space in the container and more. Instead of cloud our app currently runs on a home ubuntu server which is enough for development needs.

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

![Architecture of our system](images/architecture_diagram_busig.png)

### Bad Data

One of the main issues we had to deal with was inconsistent data. The inconsistency comes from the static data mainly. Of course real-time can report a bus which is off-route, not scheduled, etc., but that is to be expected and can be filtered out. However static data is provided as a ZIP file in CSV formatted text files online. This is okay as we can simply download the file, unzip it, process the CSV data, turn it into a relational tables and use it. However the main issue is that id fields which are used as primary keys CHANGE. And they change frequently and without a notification. This means a route id for the route "220" might change overnight with no reason to, trip id changes as well, but at a different rate, etc.

The way to combat this was to build the PostgreSQL periodically, let's say every day to prevent out of data ids. This means the creation of the tables needed to be optimized for speed, because there are millions of rows to process, filter out, index, etc. This was eventually achieved by constructing optimized filter queries, using pandas and constructing indexes for fast lookups.

A second issue now is that the training data can become stale, since there is a lot of preprocessing that needs to be done to get from a set of coordinates and timestamps associated with a trip id to a set of stops and time they were passed at, we need the PostgreSQL database for preprocessing as well, however the data in the "up-to-date" database might not be compatible with the collected data week ago. We are still working to resolve this, we will start storing snapshots of the database each time it is updated and also convert the raw json data into csv datasets because the datasets are actually static data agnostic, meaning they do not rely on static data and thus do not go stale.

### Bus Model

The Bus model container runs a Flask server which primarily manages the transfer of data and responding to requests from the front-end. The data transfer aspect is more deeply discussed in the [Data Flow](#flow-events-triggering-changes-in-the-architecture) section.

#### Data Sources

Transport For Ireland (TFI), provide static data files for several transport operators in the country. The data is provided in a ZIP file consisting of 9 CSV files. The files are listed below:

| File Name          | Contents                                                    | Approx Size (rows) |
| ------------------ | ----------------------------------------------------------- | ------------------ |
| agency.txt         | Information for all operators                               | 7                  |
| feed_info.txt      | Data Feed Metadata                                          | 1                  |
| calendar.txt       | Specifies on what days a trip runs                          | 170                |
| calendar_dates.txt | Exceptions to calendar.txt                                  | 380                |
| routes.txt         | Specifies details about routes                              | 440                |
| trips.txt          | Specifies details about trips, including the route it is on | 216K               |
| stops.txt          | Specifies details about each stop                           | 10500              |
| stop_times.txt     | Specifies the time for each trip arriving at each stop      | 6.3M               |
| shapes.txt         | Specifies the coordinates of each trip's physical route     | 6.3M               |

The data is formatted to comply with GTFS, the General Transit Feed Specification, a standardised format for supplying public transport data amongst many transport authorities around the world. Fortunately this means that the format is well documented. The relation between the nine files can be handily presented in a relational table format, presented below.

![https://www.researchgate.net/figure/Relations-among-different-text-files-of-a-GTFS-feed_fig1_319605381](images/relation_GTFS_diagram.png)

As PostgreSQL utilises a relational database schema, this matched up well with the static GTFS data, allowing us to create tables very similar to the headers of each CSV file. The database creation and population uses a combination of bash and Python scripts, more of which is explained in the [Static Update](#static-update) section.

Live data is sourced from `https://api.nationaltransport.ie/gtfsr/v2/vehicles`, provided by TFI, and fetched minutely with a cronjob. Due to the nature of Docker images, we can only create cronjobs when building the images, but we cannot run the `cron service` process until the container starts. We have opted to start the process in the background from the Python script as to avoid the creation of another container just for cronjobs. An ideal future solution to this issue is to create the cronjobs outside of all of the Docker containers and have them be triggered on the local machine. This may cause installation issues as the project would have external dependancies now.

The live data primarily serves to provide the location of buses and the corresponding timestamp. They also include other metadata such as a trip ID and the status of the schedule (cancelled, scheduled or added).

Our third and final source of external data is crowdsourced bus data provided through an API at `https://bustimes.org/api/vehicles/`. The data uses a common (but slightly modified) ID to the TFI live data, allowing us to relate this data to our other sources of data. This API provides information such as number plates, vehicle model, fuel source, bus style (double decker vs coach, etc) and special features. With this data, we may collect extra information which would allow us to estimate maximum bus capacity or provide images of the buses. This data is not currently presented in the front-end app, but can easily be integrated to any information screen.

#### A Pythonic GTFS Representation

With an amalgamation of several data sources, I needed a logical way of processing the data in a quick manner. The live data did not lend itself well to a relational table format, so I opted for a series of Python classes which would be able to store the data while the server runs and perform various operations with ease. I would be able to create attributes based off of the data sources and then create methods to turn this data into a usable format. For example, generating timetables from the given schedules would be difficult to do solely using a database query, but I can easily do this in Python, while taking into account the latest prediction data as well. These data processing tasks are well suited to Python and vastly reduced the development time. The static data is fetched from the PostgreSQL database on the server startup, usually taking 50-100s to create all of the necessary class instances. The single complex SQL query required was for calculating the orientation of the bus stops and buses themselves.

Both buses and bus stops share the same basic code to calculate their orientation. The location (as latitude and longitude) and a relevant shape_id (ID of a shape that the bus stop / bus is on) is provided. The nearest set of coordinates (on the given shape) to the provided point is returned, along with the closest point which is >5m away from the first point. By maintaining a 5m minimum, it reduces the chance of the orientation being wildly off due to bad data. The shape data also provides `shape_dist_travelled`, which tells us how far into the shape the given point is. This is used to ensure that we do not return an orientation that is facing 180° off. This uses a single complex SQL query due to the indexing provided by the database, but not Python, as we utilise a join (thus, a Cartesian product) within the query.

When new live bus data is received, information required by the inference container is collated. This includes some trip metadata and a series of coordinates and their timestamps. It is sent to the inference container where new predictions are returned. This data is provided in the form of an estimated (or actual for past stops) arrival time for each stop. It is stored in the Pythonic bus model where each Trip class instance stores its own prediction. Later, the client will send a request fetching the predicted times for a bus or stop and both the predicted times and the schedule will be used to calculate arrival times for stops. To calculate the scheduled stops for a given bus, the corresponding trip must be used along `Services` with the calendar files. Each `Service` specifies what days of the week the trip operates on, the start and end date of the service, and also any exceptions to the schedule, such as holiday periods which may add or remove buses. These are used to find whether the trip is in operation on the given day. The `stop_times` class is used to calculate the scheduled arrival time for each bus stop, in a time specified (in HH:MM:SS) from 00:00:00 to 29:59:00. This slight inconvenience means that care needs to be taken in storing the data, as the visit to the stop may occur in the morning of the following day relative to the service day specified. When returning data to the client, the predicted data is given priority and the schedule is only used as a backup when there is no prediction (for example, the very start of a new trip). This data is formatted and sorted for the front-end to easily render.

When testing the bus model late at night, there were often instances where no buses going to a given stop had started their trip yet (and thus the trip had no live data). This is not too rare for the first few stops of a route, but was confusing to users at night as our app was showing that no buses were scheduled to arrive at the stop in the future. This was solved by looking at "blocks" of trips specified in the schedule that a single bus was meant to be driving on. It could tell us which trip was the next to be taken, and we could do a simple prediction of the arrival times by taking the current delay and adding it to the scheduled times. This meant that if a bus was arriving at a stop on the current or next trip, it would appear in the list of future bus arrivals.

The Pythonic GTFS model is used by the Flask server to efficiently fulfil requests by both the front-end and the other containers. Five of the Flask routes indirectly connect to the front-end through the gateway container, while three of the routes are used to update the Pythonic model with new data, while also passing on the data to other containers as necessary. The remaining routes will be used in the future by the front-end. Two error-catching Flask routes have also been setup to return either 404 or 500 errors instead of no response being returned.

The population of the Pythonic bus model is handled by `gtfsr.py` which allows us to abstract and group functionality for more readable code. Handling the TFI static data requires database access, so I created a decorator function which would handle the opening and closing of the database connection, while also providing the wrapped function with the cursor object. Many fields in the PostgreSQL database act as foreign keys referencing other tables, so we must take this into account in the Pythonic bus model too. The order to load the various tables from the database is strict as there are many attributes of the Python classes that rely on pre-existing objects. For example, if we store both a `trip_id` and the corresponding instance of the `Trip` class, we must make sure the instance exists before attempting to assign the attribute. Despite this, there are a still a few Python class attributes that are not populated until all tables are processed, such as the rotation of bus stops which rely on the `Shape`, `Trip` and `Stop` classes.

### Gateway

The gateway was introduced in our architecture to decouple the bus model Flask server from communicating outside of the containers, while also providing sufficient modularity to allow us to add more features in the future that will not use the bus model. For example, an account system or collection of telemetry data could be handled here without modifiying the bus model container, helping keep the cohesion high. The gateway acts as a proxy of sorts which doesn't allow external connections to call internal routes in the bus model container, improving the security of the back-end.

The gateway container solely consists of a Flask server that mirrors five routes that the client requires to operate. These call the corresponding routes in the bus model container through HTTP requests and handle any 404 or 500 status code errors that may pop up. Initially, this Flask server also served dummy data to the front-end when the bus model and inference containers were not fully functional.

A port is exposed to outside of the containers to allow for the client to make requests to this container. The responses (from the bus model) are returned to the client without alteration.

### Inference

Inference is the container which takes care of the AI predictions. This means the inference itself, in other words using the already trained model to predict new times. But also it handles preprocessing the raw json data into the csv files, which is quite a complex task. You might ask where does this model come from? Well it is not really represented in our architecture, because it was prototyped and trained in google colab.

To make sense of the workflow, the model and the usage of the model, let me split this section into multiple parts: at first I will walk you through the data preprocessing needed to train the model. After we are familiar with the data I will explain the model itself, its architecture, the reasons behind choosing such architecture, the training, results and troubleshooting. When you know where this model came from I will explain how it is deployed and queried in the inference container.

#### Preprocessing

Preprocessing our data was crucial in order to extract useful information for the model to learn from. The methodology I used to pick the features and shape of data to feed the model was along the lines of "if I cannot make a reasonable estimate from the data, the model cannot either." So for example simply giving the model coordinates and timestamps with the hopes it would predict the next ones would be naive.

The first step in this procedure is to decide how to encode time. In other words how to encode the fact that the bus is progressing through time. As raw data the updates (coordinates + timestamps) are at random intervals, ~ 2 mins apart. That is quite bad for our model as it does not transition nicely to the arrival time at stops which we are ultimately interested in. Instead I decided to structure the data in bus stops. So we would give the model information about bus stops, first the observed ones, in other words the stops which the bus already passed with information of arrival time, scheduled arrival time, time in the day and distance along the route.

Converting the updates into bus stops is not straightforward. First I fetch all of the stops for this trip, calculate the distance of that stop from the beginning of the trip (using shapes table). During processing I keep track of the processed ones with an index. Then I start going through the updates, if a stop (or more) happen to be between these updates, I use linear interpolation to estimate the arrival time. This is possible because I know the distance travelled for the stops and the updates too, this gives me a nice correlation. So assuming the bus travels at constant speed (this also means it never stops) then it would arrive at that bus stop in x amount of time. For example if update 1 is 100 meters and update 2 is 200 meters and our bus stop is 175 meters far, then our interpolation ratio would be (175 - 100) / (200 - 100) = 0.75. And if update one would be at 10 seconds and update 2 at 18 seconds, then the stop was passed at 0.75 \* (18 - 10) + 10 = 16 seconds. This might seem like a bad estimation, but overall it preserves the progress of the trip perfectly and slight deviations in the exact arrival time are okay as long as the overall speed through the trip is preserved. The fact our model does not account for idling times at stops seems like an oversight, but when researchers have tried to deal with this issue, they ended up creating two models, one to predict the travel and the other to predict the stop times, but without an incredible improvement boost. Instead I assume that there is a high correlation between high waiting times and slow travel, meaning if the model can learn that the trip is going slowly, the longer idle times will be naturally modeled as well, so I do not see a reason to focus on idle prediction yet. I would like to add that better techniques exist, such as spline interpolation, however that was beyond my scope as of now.

Now that we have stops with estimated arrival times, we can do further engineering to give our model an easier time during training. First of all it is a common practice to predict the relative error to the scheduled time. For example if the bus arrived at 14:25 but was scheduled for 14:22, then the relative error is 3 minutes. We can track the relative error across the stops and it forms quite a nice smooth curve, which makes it really nice to predict. Another advantage is that it gives the model a reference point, so the error further into the future does not deviate drastically. Although it is important to mention that the relative error will increase further into the future thanks to the entropy of the system. This is quite significant in our ideology, because we aim to build trust with the user of the application to trust the prediction. If we would try to predict too far into the future it would be impossible to provide consistent results, therefore we introduce a hard stop of ~15 stops and we do not predict further than that.

Another factor to focus on is that the model will be recurrent, effectively this means the model sees just one bus stop at a time and iterates over them. Our data should reflect that, so instead of for example providing the scheduled arrival times as is, I provide the scheduled time to the next bus stop and also the distance to the next bus stop, etc. This helps the model if the relative error will decrease or increase (For example longer stretches between usually mean a decrease, etc.).

Last aspect I want to talk about is the normalization of values. This essentially means that the values should be in a similar range. For this reason I subtract the current delay from all of the times fed into the model, meaning the relative error is always 0 at the start, this helps with cases like an hour delay or more, which might throw off the model, even though the actual trip has normal times between stops. Of course this delay is then added after inference.

So now we are ready to take a look at the example training data from the dataset:

| id                  | route name | day | time   | stop id      | scheduled arrival time | scheduled departure time | distance to stop | time to stop | residual stop time |
| ------------------- | ---------- | --- | ------ | ------------ | ---------------------- | ------------------------ | ---------------- | ------------ | ------------------ |
| 4497 38961202502090 | 206        | 6   | 1262.6 | 8380B2407401 | 0.0                    | 0.0                      | 0.0              | 0.0          | 0.0                |
| 4497 38961202502090 | 206        | 6   | 1263.1 | 8380B2407501 | 30.0                   | 30.0                     | 365.5            | 30.0         | 3.0                |
| 4497 38961202502090 | 206        | 6   | 1263.6 | 8380B2407601 | 60.0                   | 60.0                     | 241.0            | 30.0         | -4.8               |
| 4497 38961202502090 | 206        | 6   | 1264.1 | 8380B2407701 | 90.0                   | 90.0                     | 202.6            | 30.0         | -15.2              |
| 4497 38961202502090 | 206        | 6   | 1264.6 | 8370B2407801 | 120.0                  | 120.0                    | 326.6            | 30.0         | -13.0              |
| 4497 38961202502090 | 206        | 6   | 1265.1 | 8370B2011901 | 150.0                  | 150.0                    | 269.0            | 30.0         | 7.7                |
| 4497 38961202502090 | 206        | 6   | 1266.1 | 8370B2408001 | 210.0                  | 210.0                    | 376.7            | 60.0         | 39.0               |
| 4497 38961202502090 | 206        | 6   | 1267.1 | 8370B2408101 | 270.0                  | 270.0                    | 183.6            | 60.0         | 10.1               |
| 4497 38961202502090 | 206        | 6   | 1267.6 | 8370B2408201 | 300.0                  | 300.0                    | 332.8            | 30.0         | 21.8               |

#### Model Architecture

I will start by mentioning that the architecture was not my idea and it is well documented and widely used design. The idea to use it for this specific task of bus predictions came actually from one of the research papers which attempted to predict bus times with an Encoder Decoder architecture. The basic idea of encoder-decoder is that the encoder sees some data and "encodes" or extracts some relevant information about that data, specifically this extracted information is in a form of a _hidden context vector_ which in our model has the dimension of 120. Using this approach makes sense if we assume that there is some nice abstraction or attribute of our system which is relevant for our predictions and can be extracted from the data. In our case that is true, what I assume is happening is that the hidden context vector is encoding the state of the traffic and the state of the bus. So if the bus is crowded it might start skipping stops, if it is at night, the bus might skip most stops because they are empty and there is less traffic. However I did not carry out analysis of the model which is usually quite hard to do, so I am only guessing this is what is happening.

The job of the decoder then is to take this _hidden state vector_ and use it to predict further stops. You can notice now that the hidden vector as a kind of bottle neck for the information that can be carried over to the predictions. As we will find later, this is something that is good for our model but also cause some issues, because it might abstract away too much information, which for example is good to find out the state of the traffic and "forget" stops which were passed longer time ago, but knowing the exact relative error for the last few stops would be quite helpful and the hidden vector does abstract away from this as well. This causes our model to badly predict the relative error of the first stop and then predict the second one with just a few seconds off from the first one. I will explain how to remedy this later.

But how do we feed the model all of the stop? We also have a variable number of stops which are observed and a variable which are targets for our prediction, so we need our model to be quite flexible. This can be achieved by using the recurrent approach which we have mentioned before. So essentially go stop by stop until the end. This is incorporated into the encoder decoder by putting an LSTM (Long Short Term Memory) model inside both the encoder and the decoder. These are Recurrent Neural Networks (RNNs for short) meaning they process the stops one by one, each step producing a hidden vector which is fed into the next iteration together with the stop information. LSTM is special because it also introduces a forgetful component which essentially learns to forget unimportant information or keep important information for longer. The reason to choose an LSTM among other RNNs was quite arbitrary, however it is known to perform better than classical ones. In the future it might be worth looking into different ones as well.

Another important detail is that we use small neural networks to embed components into a single vector. So if we are giving each stop the "time to stop", "distance to stop" and the "time" all of these three get embedded together, same goes for trip information, like the day in the week and the route.

So the overall prediction looks like this:

1. Extract trip features and embed them
2. Use them as the first hidden vector in the Encoder and feed the observed stops to the LSTM inside the encoder
3. Give the hidden vector given to us by the LSTM inside encoder to the decoder
4. In the decoder go though the target stops and predict the relative errors for each one of them

![The model architecture](images/model_architecture_busig.png)

#### Training

Training was done inside google colab, because it provides a notebook environment which is helpful when debugging and prototyping. Furthermore google colab provides free compute resources to train the model.

I have collected around 4000 trips which are fit for training, so for example the bus does not go off route, there are enough stops passed, etc. The final model trained on all of these in 40 epochs. The training/validation/test split was 70/15/15. Traditional MSE was used and optimizer was Adam.

During training the model did not go through many changes, unlike the format of the data which was iterated on multiple times, here is presented only the final version. The main issue in the training was that the model had a hard time predicting the first stop in the trip, which is actually quite unintuitive, it would make sense that the first stop should be easiest to predict and the further ones will be harder. So as explained before, this is caused by the architecture of encoder decoder, which essentially splits the two LSTMs into two, therefore the first pass in the decoder has actually the hardest job at predicting, because it has the least amount of previous information in the RNN. This is currently remedied by quite a brute solution, I simply let the decoder see an overlap in the observed stops. So currently last 2 stops which are observed are fed into the decoder as well, to give it an easier start. In the future I am thinking of improving the model in some way to solve it in a nicer way, however this method did reduce the first error significantly, so it has its merits.

I have also figured out that a decent number of stops into the future is about 15, anything further than that causes to model to have a hard time training, because of the high entropy, so whatever the model tries, the data will eventually deviate too much in the end.

![Relative error by stop position from training](images/relative_error_by_position_busig.png)

#### Deployment

Currently the preprocessing of the data is done inside the inference container. This is also true for the inference, in other words the process of using the trained model to predict new information. Therefore when the model is deployed, I receive the raw json data and I convert it into a csv in the same format as the training data. An important detail to mention which causes some headaches during debugging is that we simulate "batching". This is the practice of separating training data into batches to improve performance. However this means that the model is expecting information one dimension higher than just one trip. So when we feed the information into the model, we create a batch of size one.

The model also needs to be loaded into memory to be used, because this takes few seconds, I load the model once on startup of the container and keep it inside a wrapper class around that model. Afterwards the model is idle until a prediction request arrives through the RESTful API. In the future this preprocessing should be done in the class which is querying the model to reduce the response time. It should also happen async.

### Training data collection

The purpose of training data collection is to collect the data from GTFS Realtime, filter it and store it in a non-wasteful format. At the start this container has queried the API itself, because the bus model was not implemented yet fully. However it would be wasteful to query it twice, so now the bus model container simply passes the received JSON files to the training data collection container.

The data is filtered to only contain city Cork buses, this was done to only contain buses with similar routes. In the future new bus routes which are longer distance will be tested to see how they function with our model.

Afterwards the data is processed to a different format. Instead of a lot of individual updates I create one trip document with an array of vehicle updates, to reduce the size of the stored data.

### Front End

#### User Experience

One of our main goals on the front-end was to ensure the user has a smooth and intuitive experience when navigating the lightweight app. Hence, we decided on the screen layout that centers around the map - the centerpiece of the application, that Alex ensured is readable and works smoothly - unlike the maps of many of our alternatives. Wherever possible, we tried to use familiar user flows, to improve the intuitiveness even further.

We ensured the first-time user can get to the key info they want within 2 clicks, to make the app accessible and avoid any potential confusion.

Typical flow: start on the empty home page -> navigate to the map (see the locations of buses and stops) -> click a bus/stop (see the selected schedule)

Additionally, to lower mobile data usage, we optimized the API usage to only need 3 calls for setup and as low as 1 per minute when keeping the app open, while still showing accurate data. When dealing with the schedule data, we only use calls for the strictly necessary information, saving resources and making the app more responsive. We also utilized useFocusEffect to deal with the schedule screens calling APIs when off-screen.

Despite initial ideas of adding an account based system, we decided against it, as we weighted the user benefit of being able to share their data between their devices against the risk of frustrating the first-time user that just wants to check the timetable.

#### Modularity and Reusability

A key aspect the front-end team decided to use React Native is how easy it is to achieve modularity - the key to a scalable and maintainable app. It also ensured the vast majority of our code is reusable between Android, IOS and web browsers.

We wanted to ensure that as many parts of the app were reusable - hence modular components that are used throughout multiple screens. Additionally, the programmatic and centralized implementation of the app theme allows for quick iterations of design, as the changes are reflected throughout the entire map.

By utilising Redux and global state management we ensure our components can access the necessary data regardless of their position in the app - avoiding excessive param passing, which can cause major issues when refactoring in React.

The above-mentioned techniques let us stay agile even as the project increases in scope.

#### Features

##### Live Interactive Map

Upon launching the app, users navigate to a smooth and responsive map interface. This map displays all nearby buses and bus stops using live data, which is efficiently refreshed every minute. For added clarity, each bus and stop includes direction indicators to help users understand the route flow at a glance.

##### Real-Time Bus Stop Information

When users tap on a bus stop on the map, detailed information is displayed, including upcoming bus arrival times, route numbers, and directions. This feature is designed to give quick answers to common commuter questions like “When is my bus arriving?”

##### Live Bus Tracking

Users already on a bus can select it directly from the map to view live details such as the current location and estimated time to upcoming stops. This is especially useful for planning when to get off the bus.

##### Search Functionality

The app features a dedicated search page where users can look up specific bus stops or bus routes. Results are dynamically filtered based on user input, streamlining navigation within the app.

##### Favorites System

To accommodate frequent users, the app allows saving favorite bus routes or stops. By tapping the star icon on any stop or bus, users can add it to their Home Screen for faster access on future trips. The data is persistent between sessions due to the usage of AsyncStorage, that saves the data on the local device and rehydrates it on startup.

##### Map Filtering

Users can filter the displayed data on the map to show only the selected bus routes or stops. This reduces clutter and allows for a more personalized and focused map view based on the user’s needs. Using this feature also further improves performance, as there are fewer markers to perform calculations on.

### Flow (Events triggering changes in the architecture)

The flow of the program can be nicely separated into different events which trigger functions in the containers. These events are usually new information, but also requests from the client side. Here is a quick break down:

| Event            | Flow triggered                                                                                                                                  | Frequency  |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| Real-time update | bus model fetches data, which is then stored by training data collection. If there is a new update, inference is asked to update its prediction | 1 min      |
| Static update    | bus model fetches the latest static data and rebuilds the PostgreSQL, it also sends the new route id to name dictionary to inference            | ~1 day     |
| Client update    | Client queries gateway for updated bus data, it then fetches this info from bus model                                                           | ~1 min     |
| Client request   | Client requests more detailed info, queries gateway which then queries the bus model                                                            | Unscripted |

During development we have used this prototype of a diagram to assist us:

![The sketch which showcases the containers and flow of events](images/architecture_flow_sketch.png)

I have found that thinking about our architecture in this way is helpful to conceptualize the architecture and connect components together. Also when extending our functionality you should ask yourself which flow does this fit in and if it does not fit into any of them, then it is probably not needed.

#### Real-time Update

In further detail, the real-time update is triggered by a cronjob which start running automatically on running the bus model container every minute. At first the data is fetched from the endpoint: `https://api.nationaltransport.ie/gtfsr/v2/vehicles`. What is helpful is that this endpoint is standardized over different transport providers, which makes our code further expendable to new locations.

Then the responsibility of the bus model container after receiving this information is to send it to the training data collection container, which processes it as described above. Furthermore the bus model keeps track of the current live buses and they should have the most up to date predictions for them, so they are ready to go when the client requests them. So if new information is received, new predictions need to be made. Therefore inference is contacted and its predictions are stored in the bus model.

#### Static Update

As mentioned in the bad data section, the static data is highly unstable and needs to be updated regularly. The scripts to do so are located in the bus model container, since it is responsible for providing the up to date information. The scripts download the zip file containing the static data from `https://www.transportforireland.ie/transitData/Data/GTFS_Realtime.zip`, then unzipped into a directory using a bash script, which afterwards call the python script to create tables, populate them with the data from the unzipped files and filter them to only contain the data we care about.

When frequently restarting the server (such as during development or kubernetes pods being spun up and down), we do not wish to build the database each time. Additionally, we create 2-4 workers per container and we do not want to create the database 2-4 times as it is shared amongst all containers and workers. However, we still want it to be built if it does not exist in its entirety, as the remainder of the back-end would struggle to function. Our solution is to create a Docker Volume which contains a file which acts as a flag to identify the presence of a complete database. On the first run of the containers, the file does not exist, so the static update script is executed, which usually takes ~5 minutes. If the database is successfully built, populated and indexed, the flag file is created. During future server boots, the file will be present and the database will not be recreated. It can still be created through by executing the bash script, either manually or through a cronjob.

Since the PostgreSQL database is centralized, not many other actions need to be made in this flow, except for one. `route_id_to_name`is often used to filter out the trips we care about, because it contains only the route ids of routes we choose to track. It is stored in PostgreSQL as a table with two attributes, the route id and the name of the route. However an issue arises when a container stores this mapping of route ids on startup, because the route ids might change while it is running and then the stored data becomes stale. To prevent simply fetching the data periodically, the bus model pushes it to the containers that need it on the event of the static data update. Currently it only services the inference container. This probably made you think about publisher subscriber architecture and it is the same principle, however we did not go full out on the publisher subscriber architecture for example using Redis, because we deemed it a bit of an overkill.

## Summary

In this report we have shown that the architecture of our system is modular, separated into Docker containers for the many benefits that it brings. These benefits are collaboration, abstraction, reusability, scalability and elasticity if we deploy our containers in a cluster. Afterwards we have went through the individual containers and explained their respective functionality, focusing on justifying the choices made about the design, explaining where future improvements could be made and explaining the function in high level abstractions.

Furthermore we have shown how these containers connect to each other in the flow section of the report. In our view the flow ties everything together and it is a great perspective on our architecture which improves understanding and helps us and potential contributors stay on the right track when it comes to implementing features. The reader should now have a good understanding of the different components, what they do and how they help achieve the overall goal of providing real-time information about buses. The reader should also be aware of the potential drawbacks in our design, how they could be addressed and hopefully also learned from our observations during development.

Overall our architecture provides up to date information on buses which it fetches from GTFS. We store the data fetched in order to provide new training data for our AI model. This model is then used to infer the arrival times of the buses which are currently on the roads, focusing on reliability of our predictions and understanding the limitations of our model. All of this real-time state of the buses is managed by the bus model container, which offers extensive API endpoints to fetch the latest information. These endpoints are mainly accessed by our gateway container which acts as a sort of proxy to sit in between the client requests and the bus model. This helps with decoupling and for example introducing security in the future. All of this data is then displayed by the front end code, which aims to provide a fast, smooth, simple experience to its users. Integrating a map significantly improved the user experience.

Finally our goal of providing a simple, smooth experience of looking up credible information on real-time bus data was achieved, however there are still many areas we aim to improve in the near future.

## Lessons Learned

The architecture of our system is modularized in containers. This has helped us collaborate between each other, because all was needed to do was define APIs well between the containers. Afterwards we could work on our own containers and collaborate on the things that matter such as overall architecture, satisfying the use cases, etc. while abstracting the implementation details. This had a surprising effect on our collaboration as well, because our understanding of individual containers we have not worked on was not in depth, we were more critical of each others work and everyone else served as a sort of product manager, checking that the development is useful for the use cases mainly. This helped us focus on our goals and not stray too far into implementation rabbit holes and details. It was also interesting see how important mutual respect was as well during development, because otherwise this criticality of others work would hinder collaboration. We used Github's pull request GUI to review each pull request in detail in order to approve or reject the request as necessary. Comments were used to communicate on potential issues as well. This allowed us to make sure a high standard of code was achieved before merging the code into another branch. It also gave each of us an insight into the latest work done by the others, but this was made difficult later on when branch merges had 200+ new commits involved.

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

Installed Ubuntu server on my old laptop, set up the networking on that laptop to provide static IP and also implemented basic security with firewall and ssh. I then ran and managed the server for the duration of the training data collection, sometimes debugging and troubleshooting it.

I have written the code to collect the training data, this involves connecting to the API endpoint, deciding on which routes to collect, filtering the data accordingly, designing the structure of the mongodb collection to store the collected data efficiently and writing the code to convert the raw data to the more storage efficient form.

Setup the mongodb container with authentication and managing the connection to that database with pymongo. Wrote insert queries to insert the converted collected data into the collection. Also wrote some basic queries to check the state of the database which help to monitor its health.

This training data collection container also has a RESTful API which allows it to communicate with other containers, usually for the purpose of providing the collected data.

In order to filter the data out I also needed to implement the static data database, which at first I have done with SQLite but later migrated all of that code to PostgreSQL. This means designing the database schema to store static data such as routes, trips, stops, etc., setting up the dependencies and cascades on the database, which proved harder than it looks because the way PostgreSQL handles cascades can be incredibly inefficient, so sometimes even though the reference is there, it is better to not write it for performance reasons. I have then wrote the code to filter out the database which was also quite tricky to optimize thanks to the sizes of the tables which can go into millions of rows for some of them. And of course we needed the code to be efficient, because this database would be rebuild essentially every day. This also involved setting up indexes on the tables to allow for faster filtering and faster queries down the line.

I have written the bash script to download the zip file, unzip it and create the relational PostgreSQL database with it. Which was initially inside the training data collection container but later I moved it to the bus model.

I have developed the inference container. First of all by preprocessing the collected training data and converting it into a dataset which can be trained on. This was one of the most challenging parts of the entire project, because I needed to map the coordinates associated with timestamps and a trip id to much more rich data, such as when were stops passed on that trip with distances to them on that trip, etc. All of this is too complicated to put down in text, but it involved designing a very efficient way to query the databases on the tables which contain millions of rows (sometimes you would need to join these tables together, which would need to be done efficiently, otherwise the amount of rows to process would be in billions).

After designing the queries needed I still needed to develop the code which would use those queries in order to process the data into something the model would use. This was not so simple because of course you need to know the model architecture to pre-process the data for it, but you need to know which data you are working with to design the model. So these two design phases happened in tandem, so often I would reiterate on the model architecture and change the data accordingly, then I would find a nicer representation of the data and change the model, etc. Eventually I have developed a trip manager class which converts the training and in the future extended it to preprocess the data for inference as well.

The model itself was developed in Google Colab. Firstly I have decided to use Encoder Decoder after reading research papers, then used the library pytorch which handles most of the code for me, all I needed to do was make the existing model architecture fit with my specific data I wanted the model to predict. When eventually the code was compiling I still needed to actually train the model which involves a lot of iterations and adjusting hyper parameters. This was the case for me as well, I have adjusted the epochs, number of trips the model tried to predict, introduced randomness into the dataset to help with generalization and resolved the issue of the first stop prediction with the overlap as I mentioned before. Eventually I have gotten good results on the test dataset.

Finally I have deployed the model in the inference container and provided the API routes to access this model. This involved creating a wrapper class around the model which handled the inference, loading the model and data manipulation.

I have also created the architecture diagram and played a big role in designing the architecture because I was in charge of the containerization. And as everyone else I have worked on the presentation, helped with the design of the one page report and I wrote most of the project report, except for the containers and contributions which I have not worked on personally.

### Liam

I primarily managed the bus model container, which initially only consisted of the Pythonic bus model representation and the Flask server, but latest involved other data processing tasks. Initially, I fetched and parsed the static (CSV) data myself, which fed directly into the Pythonic bus model. I expanded the bus model to include more than just the fields in the CSV files such as "joins" between the  as it was necessary to make the code more readable and quicker.

I researched and deciphered the static data provided by TFI, which remained complicated to understand despite the documentation available online. The data has been heavily normalised, so it is not presented in a straight forward style.

When the responsibility of the PostgreSQL database fell under the bus model container, I modified Radek's implementation and moved the data source of the Pythonic bus model to use the database. This also required me to modify the tables in the database to include some previously excluded fields found in the CSV files. I added a Docker Volume with a flag file to help indicate a complete database as well.

After we made a slight adjustment to the overall architecture of the back-end, I took responsiblity of ensuring that the training-data-collection and inference containers both had access to the static and live data by forwarding relevent data on each update. I also started fetching the bus vehicle data which is used in the Pythonic bus model.

I created a cronjob to fetch the live data minutely within the Dockerfile of the bus model container, so only the cron process must start to get it running.

I collect and store the required information that the prediction model needs and pass the data to the inference container on each bus location update. I handle the returned data in the Pythonic bus model. I compute the static bus schedule when there is no predicted arrival times yet and the front-end requests them. I format the times reduce extra calculations on the front-end.

I created and maintained the bus model Flask routes and made sure that the gateway container's Flask routes correctly called them and had appropriate error checking in place. I ensured that all routes required by the front-end were present and worked as intended during all stages of testing.

I ensured that no container was printing too much debugging information to allow server administrators (i.e. us) to be able to read the logs to check for errors and server launching progress.

###  Pawel

Analyzed pain points of users of similar products to ensure positive and accessible UX.

Designed and implemented a maintainable frontend architecture using React, ensuring seamless integration with the backend and enabling efficient data flow across the application.

Took full ownership for architecture related complex parts of the frontend - ranging from advanced data integration to performance optimization.

Developed a custom React hook and set up Redux to fetch, manage, and display dynamic data (buses, stops, timetables, routes) reliably from the backend.

Researched and set up reverse proxies to connect to backend during development.

Standardized TypeScript types to maintain consistency with evolving backend documentation and reduce runtime errors.

Optimized API calls and integrated AsyncStorage persistent storage, resulting in a convenient user experience and a smoother user interface.

Implemented efficient filtering and routing mechanisms to handle large datasets while ensuring the app remained responsive under frequent updates.

Authored the frontend section of the project report, clearly outlining architectural decisions, implementation challenges, and performance improvements.

Contributed to the overall project presentation, ensuring that the frontend design and functionality were effectively communicated.

### Alex

As part of the project, I was primarily responsible for the front-end design and development of the mobile application. My key contributions are outlined below:

I have started with designing the full user interface in Figma, taking inspiration from existing solutions such as Google Maps and TFI Live. While these apps influenced the layout, I created a custom design tailored to our use case, ensuring that the interface remained clean, intuitive, and easy to navigate.

I implemented the layout and styling of the application using React Native, with a focus on delivering a user-friendly and responsive experience across both iOS and Android platforms.

To improve performance, I optimized the map view by caching data such as buses and stops locally and minimizing unnecessary re-renders. This significantly improved responsiveness and overall app quality.

I developed and standardized the main UI components, including interactive map markers, bus information pages, and stop detail views. These components followed a consistent design pattern to enhance maintainability and usability.

I collaborated with Pawel to implement the map functionality, contributing to features such as live bus updates, location tracking, and marker interactions.

I was responsible for defining and enforcing a consistent data format for information passed to the front end (excluding predicted arrival times), which simplified integration and reduced potential errors during development.

I implemented the search page, which included filtering and selection functionality for bus stops, making it easier for users to find relevant transit information.

I also created API call functions within the API gateway to retrieve necessary data from the back end, ensuring smooth communication between the application layers.

Finally, I produced the final project video, which demonstrated the app’s features and functionality in a clear and engaging manner for presentation purposes.
