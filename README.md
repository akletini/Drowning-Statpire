# Drowning-Statpire

Simple Web-Application to monitor social media statistics for the band Drowning Empire using Python with Flask and SQLAlchemy.

The application will collect data for Instagram, YouTube and Spotify twice every day to create a database for visualizing trends and possibly apply machine learning at a later stage. Therefore a sufficient amount of data over a large timespan has to be aggregated (ideally including promotion cycles, releases, etc.).  

#

# Administration and Setup

## Create Database and Tables

```python
from controller.flask_controller import db
db.create_all()
```

## Delete Database and Tables

```python
from controller.flask_controller import db
db.drop_all()
```

## Create and Retrieve all Entries (e.g. for Instagram Statistics)

```python
from controller.flask_controller import db
from models.models import InstagramEntry

# creation
entry = InstagramEntry(..params..)
db.session.add(entry)
db.session.commit()

# retrieval
InstagramEntry.query.all()
```
