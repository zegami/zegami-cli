# zegami-cli
A Command Line Interface for [Zegami](https://www.zegami.com).

Zegami is a visual data exploration tool that makes the analysis of large collections of image rich information quick and simple.

# Installation
```
pip install zegami-cli
```

# Commands

## Get a collection
Get the details of a collection
```
zeg get collections [collection id] --project [Project Id] --token [API token]
```

## Update a collection
Update a collection - *coming soon*.
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
Update an existing data set with new data.
```
zeg update dataset [dataset id] --project [Project Id] --config [path to configuration yaml] --token [API token]
```

The config `yaml` file is used to specify additional configuration for the data set update. It can be set up to either specify the fully qualified path to a `.csv.`, `.tsv` or `.xlsx` file to upload using the `path` property *or* the `directory` property can be used to upload the latest file in a directory location.
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
