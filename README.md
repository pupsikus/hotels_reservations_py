# API
Room reservation CRUD methods are covered with tests ('tests/test_reservations.py')
Project uses sqllite database which is located in memory and deleted when script 
is finished. All room reservation data stores in the table 'room_reservations',
which is an ORM. SQLAlchemy is used to connect with the database.

If you want to make a room reservation you must create a new Visitor first.
If you wat to update a reservation you must create a new Visitor with updated all
necessary fields.

To reserve a room you must initialize a Reservation object, choose method: 
create, read(get_reserve), delete, update and point an argument which 
is a Visitor object. Read method (get_reserve) searches by exact room number,
start date and end date, but internal searches are used range search.
There is also a separate method 'search_reservations_by_date_range' which
returns all reservation from start date to end date range, without room number argument.
Visitor can have lots of different fields, but for reservation it is used only:
first name, last name, room number, start reservation date, end reservation date.
All data is checked on Visitor initialization step. 

You may handle errors using base exceptions: RoomReservationException and VisitorException.

There are several TODO rows which are just a remind that check data fields 
can be expend.

# PROBLEM STATEMENT

“BlaBlaBla Hotels” needs a Property Management System to operate their hotel business. 
Your task is to define and implement a backend REST API using the Python programming language. 
The API should provide functionality to do following:

CRUD Reservations
Search Reservations by date range (e.g. get reservations from 15 to 19 April 2017)

Reservation is a first-class citizen of the system. 
Reservation entity contains: first & last name of the guest, room number, 
start date and end date of the stay.


# IMPLEMENTATION DETAILS

Please follow these rules for your solution:

Use Python as a programming language.
Use gradle as a build tool.
Distribute application as a docker image via hub.docker.com
Share the code via github.com

You’re also encouraged to use any third-party libraries and frameworks, 
which may simplify you work.

When posting the code to Github, keep in mind we prefer some commits 
history in the repo vs single commit. Tests are welcome and encouraged.
