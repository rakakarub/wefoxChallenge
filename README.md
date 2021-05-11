### :computer: How to execute

#### How to install:
    git clone git@github.com:rakakarub/wefoxChallenge.git

#### How to run:
From the folder you have cloned the repo:

    cd wefoxChallenge/
    docker-compose up -d

### :memo: Notes

For this challenge python has been used. Although I've been given enough time, due to the errand I had to do, 
I've been able to spend ~7 hours on this project.

Implementation is added in to **payment_service** folder. I've also modified **docker-compose.yml** file. So that,
my service would be included, and the database secrets could be fetched. 

Under **payment_service** folder, there is a directory called **'src'** which includes all the python code.

#### Python files:
- **database_connector.py**: Initializes the db config and create table mapping classes. I've used **PonyORM** as object-relation mapping.
- **kafka_consumer_service.py**: This is to create KafkaConsumer object to connect brokers and consume messages.
- **rest_client_service**: This is to make calls to external payment endpoint and log endpoint. Simply, it is a client service
- **runner.py**: This is the main module of the project. It bootstraps kafka consumer, database connection and creates 
  rest client service. Then by polling, consumes the messages coming from kafka queue, and by looking at their topic 
  (online or offline), redirects to related method. If it is **offline** it just tries to insert payments table updates accounts.last_payment_date, 
  if it is **online**, it first validate the payment via a POST call to **/payment** endpoint then inserts payments table
  and updates accounts.last_payment_date  

### :pushpin: Things to improve

Since I mentioned earlier, I didn't have enough time (due to some errands) to make this a solid project.

- My initial thought was to implement this in Java with Spring Boot and Hibernate. I had to move on to python since I didn't have much time.
- Instead of using a single file for both database connection and the entity classes, creating a separate class for database connector and 
  separate classes for each entity would be perfect.
- Instead of using a single file for the application logic (**runner.py**), each individual service should have its own service class/object  
- I should've definitely added some unit tests.
- Documentation could've been added to the methods used.
