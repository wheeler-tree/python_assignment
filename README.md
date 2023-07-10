# Overview

## Introduction

A stock data storage and statistical calculator application with Flask as the framework, SQLAlchemy as the Database Interface, Sqlite as the Database.

## Commands

Make sure you already have installed docker, python3, pip, and virtualenv in your server.

1. Create a new virtual environment in the current directory

   ```
   virtualenv env
   ```

2. Load the activation script

   ```shell
   source env/bin/activate
   ```

3. Install docker-compose

   ```shell
   pip3 install docker-compose
   ```

4. Add your API_KEY from  

   [AlphaVantage]: https://www.alphavantage.co/documentation/

    in the conf/dev.yaml

5. Start the application

   ```shell
   sh app.sh start
   ```

6. Stop the application

   ```shell
   sh app.sh stop
   ```

   

## Verify

1. Get financial data API

   ```shell
   curl -X GET 'http://127.0.0.1/api/financial_data?start_date=2023-07-01&end_date=2023-07-10&symbol=IBM&limit=10&page=1'
   ```

2. Get statistics API

   ```shell
   curl -X GET 'http://127.0.0.1/api/statistics?start_date=2023-07-01&end_date=2023-07-10&symbol=IBM'
   ```

   

## Methodologies Used

For this project, I selected Flask as the web framework due to its simplicity and lightweight nature. Given the relatively simple requirements of the project, there was no need to use a heavier framework like Django. Flask allowed me to quickly develop and deploy the required functionality without unnecessary overhead.

In terms of the database, I opted for SQLite. SQLite is a self-contained and serverless database engine that is well-suited for small-scale applications. It doesn't require a separate database server, making it easy to manage and deploy. Additionally, SQLite provides good performance for single-user scenarios and simplifies the setup process.

While alternatives like MySQL or PostgreSQL could have been considered, SQLite was chosen to align with the lightweight nature of the project and to avoid the complexity of managing a separate database server.

By leveraging Flask and SQLite, I was able to deliver a streamlined solution that met the project requirements efficiently and effectively.

## Improvement points

During the development of the project, several areas were identified for potential improvement. These areas include:

### Logging

Logging plays a crucial role in monitoring and troubleshooting applications. While the project currently lacks a comprehensive logging system, it would be beneficial to implement one. By incorporating appropriate logging statements throughout the codebase, we can capture valuable information about the application's behavior, error conditions, and performance. This will aid in debugging issues and maintaining the application in the long run.

### Exception Handling

Proper exception handling is essential for robust and reliable applications. Currently, the project lacks a comprehensive approach to handling exceptions. Enhancing the exception handling mechanism will involve implementing try-except blocks at appropriate places, capturing specific exceptions, and providing meaningful error messages or responses to users. This will improve the application's resilience and user experience by gracefully handling unexpected situations.

### Model-View-Controller (MVC) Architecture

The current codebase could benefit from adhering to the Model-View-Controller (MVC) architectural pattern. MVC provides a structured approach to separating concerns within an application. By clearly defining models, views, and controllers, we can achieve better code organization, maintainability, and scalability. This architectural pattern promotes loose coupling between components and allows for easier testing and reusability of code.

### Unit Testing

While the project demonstrates the functionality, there is a lack of comprehensive unit tests. Unit tests are essential for ensuring the correctness of individual components and detecting regressions. By writing unit tests for various functions, methods, and modules, we can verify that they perform as expected and catch any potential issues early in the development cycle. This will enhance the project's stability, maintainability, and confidence in the codebase.

By addressing these improvement points, we can enhance the overall quality, maintainability, and reliability of the project. These enhancements will result in a more robust and user-friendly application that is easier to maintain and extend in the future.

## Total hour spents

During the development of the project, a total of 13 hours were spent on various tasks. The breakdown of hours is as follows:

- July 7: 3 hours
  - Time spent investigating the Flask framework and documenting the initial project requirements.
- July 8: 5 hours
  - Time spent implementing the functionality to retrieve raw data and designing the APIs.
- July 9: 3 hours
  - Time spent setting up Docker and creating the shell script for starting and stopping the application.
- July 10: 2 hours
  - Time spent on documentation, refining the project's documentation to provide clarity and improve readability.

Due to my recent transition to a Python developer position, I had a limited timeframe of only 3 days to complete this assignment. Despite the time constraints, I want to express my gratitude for the opportunity given to me.
