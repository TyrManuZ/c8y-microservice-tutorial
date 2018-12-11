# Accessing Cumulocity APIs

## Goal

The goal of this step is to create a REST endpoint that will call Cumulocity, grab some data and do so business logic on it.

## Key concepts

- Using incomming credentials to access Cumulocity

## Steps

1. Create REST handler to calculate average
2. Use credentials of incomming request to call Cumulocity API for raw measurements
3. Return result of business logic

## Commands

All commands assume that you are located in the folder of the current step

### Build docker

```
$ docker build . -t c8y-tutorial:0.4
```

### Run docker locally

```
$ docker run -p 8080:80 -e C8Y_BASEURL=https://examples.cumulocity.com c8y-tutorial:0.4
```

### Create deployable package

```
$ docker save c8y-tutorial:0.4 > image.tar
$ zip c8y-tutorial-4 image.tar cumulocity.json
```