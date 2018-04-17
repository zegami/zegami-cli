# zegami-cli
A Command Line Interface for [Zegami](https://www.zegami.com).

Zegami is a visual data exploration tool that makes the analysis of large collections of image rich information quick and simple.

# Installation
```
pip3 install zegami-cli[sql]
```

# Commands

## Login
The login command promtps for username and password which is then used to retrieve a long-lived API token which can be used for subsequent requests. The token is stored in a file in the currenet users data directory.
Once retrieved all subsequest commands will use the stored token, unless it is specifically overridden wiht the `--token` option
```
zeg login
```

## Get a collection
Get the details of a collection.
If the `collection id` is excluded then all collections will be listed.
```
zeg get collections [collection id] --project [Project Id] --token [API token]
```

## Update a collection
Update a collection - *coming soon*.
```
zeg update collections [collection id] --project [Project Id] --config [path to configuration yaml] --token [API token]
```

The config `yaml` file is used to specify additional configuration for the collection update. It can be used to update the collection metadata, like the name or description, or it can perform actions like make public.
```
# The type of update. For now this needs to be set to 'publish'
update_type: publish
# Config for the publish update type
publish_config:
# Flag to indicate if the collection should be published or unpublished
    publish: true
# The id of the project to publish to
    destination_project: public
```

## Delete a collection
Delete a collection
```
zeg update collections [collection id] --project [Project Id] --token [API token]
```

## Get a data set
Get a data set
```
zeg get dataset [dataset id] --project [Project Id] --token [API token]
```

## Update a data set
Update an existing data set with new data.
```
zeg update dataset [dataset id] --project [Project Id] --config [path to configuration yaml] --token [API token]
```

The config `yaml` file is used to specify additional configuration for the data set update. There are *two* supported `dataset_type` supported.

### File
The `file` type is used to update a data set with a file. It can be set up to either specify the fully qualified path to a `.csv.`, `.tsv` or `.xlsx` file to upload using the `path` property *or* the `directory` property can be used to upload the latest file in a directory location.
```
# The type of data set. For now this needs to be set to 'file'
dataset_type: file
# Config for the file data set type
file_config:
# Path to the dataset file
    path: 
# Or path to a directory that contains data files.
# Only the latest file that matches the accepted extensions (.csv, .tsv, .xlsx)
# will be uploaded. This is useful for creating collections based on
# automated exports from a system, like log files.
    directory:
```

### SQL
The `sql` type is used to update a data set based on an `SQL` query.
Uses SQLAlchemy to connect to the database. See http://docs.sqlalchemy.org/en/latest/core/engines.html and https://www.connectionstrings.com/ for the correct connection string format.

```
# The type of data set. For now this needs to be set to 'file'
dataset_type: sql
# Config for the sql data set type
sql_config:
# The connection string.
    connection: 
# SQL query
    query:
```

## Delete a data set
Delete a data set - *coming soon*.
```
zeg delete dataset [dataset id] --project [Project Id] --token [API token]
```

## Get an image set
Get an image set - *coming soon*.
```
zeg get imageset [dataset id] --project [Project Id] --token [API token]
```

## Update an image set
Update an image set with new images.
```
zeg update imageset [dataset id] --project [Project Id] --config [path to configuration yaml] --token [API token]
```

The config `yaml` file is used to specify additional configuration for the image set update. The `paths` property is used to specify the location of images to upload and can include both images and directories.
```
# The type of image set. for now this needs to be set to 'file'
imageset_type: file
# Config for the file image set type
file_config:
# A collection of paths. Paths can be to both images and directories 
    paths:
        - an_image.jpg
        - a/directory/path
```

## Delete an image set
Delete an image set - *coming soon*.
```
zeg delete imageset [dataset id] --project [Project Id] --token [API token]
```
