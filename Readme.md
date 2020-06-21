# Victoria Recycle Map
This readme will outline the steps required to setup an environment to work on the map.

## Software requirements
- QGIS (https://qgis.org/en/site/forusers/download.html)
- PostgreSQL (https://www.postgresql.org/download/) with PostGIS extension (https://postgis.net/)
- GDAL/OGR (https://gdal.org/)

As an alternative I have had a lot of success installing PostGIS and GDAL/OGR within Docker containers. Once you have docker configured it makes the install process simple from the command line and the tools and dependencies are all installed in their own self-contained environment. Useful links:
- https://docs.docker.com/install/
- https://hub.docker.com/r/kartoza/postgis/
- https://github.com/geo-data/gdal-docker


## Download spreadsheet data
This process formerly used Mapbox's [Geo for Google Docs](https://github.com/mapbox/geo-googledocs) to geocode the data and export as GeoJSON. Due to deprecations in the Google Docs API, this tool no longer works. Instead coordinates should now be entered manually and we can use GDAL/OGR to read a CSV file instead of GeoJSON.

1. Go to https://docs.google.com/spreadsheets/d/153YiB4-abz2BiDY3xQJ-PkVE5bbkfqPyM6vHe66CeSQ/edit?usp=sharing
2. Download each of the worksheets from the spreadsheet (`FacilityProductJoin`, `Products`, `Facilities`, `Product Categories`). File > Download as > Comma-seperated values (.csv, current sheet).
3. Move all of the data to the `Data` directory within the root directory (the same level as this readme).

## Create new PostGIS database, tables and views
1. Make sure you are working in the project's root directory in the terminal and run the `create_db.sql` script PostgreSQL. The steps below are using the (`psql`)[http://postgresguide.com/utilities/psql.html] command line tool. The following command uses the default PostgreSQL configuration. Parameters may need to be updated depending on how you configured your database.
```
psql postgres://postgres:postgres@localhost:5432 -a -f create_db.sql
```

You can also use [pgAdmin](https://www.pgadmin.org/download/) as a GUI.

## Populate database with facilities
1. Use `ogr2ogr` to create and populate the `facilities` table in the database. From the command line, `cd` to the root direcotory (the one that contains the `Data` directory) and run the following command:
```
ogr2ogr \
    -f "PostgreSQL" \
    PG:"host=localhost port=5432 user=postgres password=postgres dbname=vic_recycle_map" \
    "./Data/productfacilityinfo - Facilities.csv" \
    -nln "facilities" \
    -oo "X_POSSIBLE_NAMES=geo_longitude*" \
    -oo "Y_POSSIBLE_NAMES=geo_latitude*" \
    -oo "KEEP_GEOM_COLUMNS=NO" \
    -t_srs EPSG:3857 \
    -s_srs EPSG:4326
```

## Create the other tables and views
1. From the project's root directory, run the `create_tables_and_views.sql` script with `psql`:
```
psql postgres://postgres:postgres@localhost:5432 -a -f create_tables_and_views.sql
```

