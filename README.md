# Zomentum Movie Booking REST API

## Features 
    **TICKET EXPIRATION in 8 hours**
    **REST API to CREATE,UPDATE,GET,DELETE TICKETS**
    **Robust Logger to log events/Failures**
    **NoSQL MongoDB Database with PyMODM ORM Engine**
    **FLASK Python based Backend**

## API Endpoints:
    **/api/v1/booking GET** - Get Information about tickets

    **/api/v1/booking POST** - Create new tickets

    **/api/v1/booking PUT** - Create/Update tickets

    **/api/v1/booking DELETE** - Delete tickets

## Architecture
    Uses Flask  (python framework) for serving,
    Mongodb for backend, PyMODM ORM engine for Flask app to 
    communicate with the mongodb database.

    The app.py file contains the main server definition 
    as well as the endpoint definition and the Scheduler to 
    expire tickets in 8 hours

    The apis.py contains the definitions for the endpoint handlers

    The database.py contains abstractions and definition for the 
    database procedures and the ORM object definition of a Ticket

    The logger.py contains a simple logger to log events, failures