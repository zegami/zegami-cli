# zegami-cli
A Command Line Interface for [Zegami](https://www.zegami.com).

Zegami is a visual data exploration tool that makes the analysis of large collections of image rich information quick and simple.

# Installation
```
git clone https://github.com/zegami/zegami-cli.git
cd zegami-cli
pip install .
```

# Commands

## Get all collections
Get a list of all collections
```
zegcli get collections --token [API token]
```

## Update a collection
Update a collection
```
zegcli update collections [collection id] --token [API token]
```

## Delete a collection
Delete a collection
```
zegcli update collections [collection id] --token [API token]
```

## Get a data set
Get a data set
```
zegcli get dataset [dateset id] --token [API token]
```

## Update a data set
Update a data set
```
zegcli update dataset [dateset id] --token [API token]
```

## Delete a data set
Delete a data set
```
zegcli delete dataset [dateset id] --token [API token]
```

## Get an image set
Get an image set
```
zegcli get imageset [dateset id] --token [API token]
```

## Update an image set
Update an image set
```
zegcli update imageset [dateset id] --token [API token]
```

## Delete an image set
Delete an image set
```
zegcli delete imageset [dateset id] --token [API token]
```
