# Getting started

## Goal

The goal of this step is to get a very basic setup of a web service hostable on Cumulocity and exposing a hello world REST API

## Key concepts

- Cumulocity manifest file (cumulocity.json)

## Steps

1. Create manifest file
2. Create webserver.py
3. Add simple hello world handler in python

## Commands

All commands assume that you are located in the folder of the current step

### Build docker

```
$ docker build . -t c8y-tutorial:0.1
```

### Run docker locally

We will expose the web service on localhost:8080
```
$ docker run -p 8080:80 c8y-tutorial:0.1
```

### Create deployable package

```
$ docker save c8y-tutorial:0.1 > image.tar
$ zip c8y-tutorial-1 image.tar cumulocity.json
```