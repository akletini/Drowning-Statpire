# Drowning-Statpire

Simple Web-Application to monitor social media statistics for the band Drowning Empire using Python with Flask and SQLAlchemy

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

## Create and Retrieve all Entries (i.e. for Instagram Statistics)

```python
from controller.flask_controller import db
from models.models import InstagramEntry

# creation
entry = InstagramEntry(<followCount>, <followeeCount>, <dateOfSearch>)
db.session.add(entry)
db.session.commit()

# retrieval
InstagramEntry.query.all()
```
