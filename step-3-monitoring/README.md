# Configuring logging and monitoring

## Goal

The goal of this step is to create logging on stdout and configure the health endpoint to utilize the automatic monitoring of Cumulocity.

## Key concepts

- Cumulocity health endpoint monitoring
- Logging

## Steps

1. Add lifeness probe in manifest file
2. Add health endpoint
3. Add logging on stdout
4. Add endpoint to kill the service in order to test automatic failover
5. (optional) Add logging to file and expose it via REST

## Commands

All commands assume that you are located in the folder of the current step

### Build docker

```
$ docker build . -t c8y-tutorial:0.3
```

### Run docker locally

```
$ docker run -p 8080:80 -e C8Y_BASEURL=https://examples.cumulocity.com c8y-tutorial:0.3
```

### Create deployable package

```
$ docker save c8y-tutorial:0.3 > image.tar
$ zip c8y-tutorial-3 image.tar cumulocity.json
```