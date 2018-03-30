# zegami-cli
A Command Line Interface for [Zegami](https://www.zegami.com).

Zegami is a visual data exploration tool that makes the analysis of large collections of image rich information quick and simple.

# Installation
```
pip install zeg
```

# Commands

## Get a collection
Get the details of a collection
```
zeg get collections [collection id] --project [Project Id] --token [API token]
```

## Update a collection
Update a collection
```
zeg update collections [collection id] --project [Project Id] --token [API token]
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
Update a data set
```
zeg update dataset [dataset id] --project [Project Id] --config [path to configuration yaml] --token [API token]
```

```
# The type of data set. This needs to be set to 'file'
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

## Delete a data set
Delete a data set
```
zeg delete dataset [dataset id] --project [Project Id] --token [API token]
```

## Get an image set
Get an image set
```
zeg get imageset [dataset id] --project [Project Id] --token [API token]
```

## Update an image set
Update an image set
```
zeg update imageset [dataset id] --project [Project Id] --token [API token]
```

## Delete an image set
Delete an image set
```
zeg delete imageset [dataset id] --project [Project Id] --token [API token]
```
