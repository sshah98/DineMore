# GW Dining Tracker

## The goal is to provide a way for students to input their current balance. The program will track user spending with input of the place they bought and the money they spent

-   (will need to be changed later because many students don't actually get receipts or care how much money they spent at one time)

The application starts off with the input value of the current balance of the student

### _Done_:

-   CSV file contains vendor information (name, address, website, and filters inc. veg friendly, deliver, late night)
-   CSV file containing prices of every transaction in one's get history from present day to 6 months ago
-   python file scrapes GET-Cbord website for data, puts into DataFrame and then plots line with regression

-   Focus on predicting by date, when dining dollars will run out 

### _To Do_:

1.  See what other statistical analysis and information can be understood from the data

-   Intermediary steps here
-   Intermediary steps here
-   Get data about the average amount spent per day
-   Data about how much you spend per week
-   Get data about when you will run out of gworld based on current spending     habits
-   Get data about places you spend the most money
-   Figure out other key things that could help users 

3.  Implement into a Django REST API so that other people can start accessing their information 
4.  Figure out how to convert the rest api to a web interface in the beginning so that users can see


### _Next Steps_:

Make a django/flask app -- figure that out
Login page that user uses with same user and password as GET App
One single page that shows Average spent in the last week, average spending per day
Broken by category - food, printing, laundry, snacks(gallery market, etc)


