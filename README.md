# Hackathon Backend
This project contains a simple backend which returns the nearby racks given a lat, long and radius.

## Starting the Backend
To start the backend and database, run:
```shell
docker compose up --build
```
To populate the database with the rack data, first install gdal:
```shell
brew install gdal
```
Then run the following command to insert the rack data into the database. Make sure to change the connection parameters accordingly.
```shell
ogr2ogr -f "PostgreSQL" \
PG:"host=localhost port=5432 dbname=postgres user=user password=password" \ # Change parameters accordingly
data.geojson \
-nln racks \
-nlt POINT \
-lco GEOMETRY_NAME=geom \
-overwrite
```