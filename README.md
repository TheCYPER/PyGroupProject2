# AI1030 Group Assignment 2 - Smart Library System

 **Each time before running tests, ```data.*``` should be executed to generate data, whatever the directory you are locating at.**

## Project Structure

 - ```data.py``` uses ```Faker``` library to generate fake data.
 - ```db_init.py``` initializes ```SQLAlchemy``` engines, ```Base``` class, and sessions.
 - ```library.py``` provides an interface between tables in the SQL database and self-defined data management methods.
 - ```recommendation_demo.py``` implements a recommendation system.
 - ```test.py``` tests the functionality of methods and the speed of two different searching algorithms.
 - ```timing_test.py``` provides more additional tests with more details.
 - ```models/``` specifies three main Python classes that are mapped to SQL database.

 ## Experiments

 Folders ```expr/``` and ```expr2/``` contain a simplified project and codes for rigorous time complexity experiments. The difference between them are that in ```expr/models/books.py```, ```title``` feature is defined as ```title = Column(String, nullable=False)```, without ```index=True```, while ```expr2/models/books.py```, parameter ```index=True``` is used.

 Each experiment provides the comparison between naive search and advanced search, visualizing data, and fitting data. These two experiments can be re-done easily locally.
