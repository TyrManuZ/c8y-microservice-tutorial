# Working with ENV variables

## Goal

The goal of this step is to access the environment variables Cumulocity will inject in the docker runtime when the container is started.

## Key concepts

- Cumulocity environment variables

## Steps

1. Read out environment variables from os
2. Expose them via REST handler

## Commands

All commands assume that you are located in the folder of the current step

### Build docker

```
$ docker build . -t c8y-tutorial:0.2
```

### Run docker locally

We will inject one of the environment variables by hand. Keep in mind that for local testing you need to inject environment variables yourself.
```
$ docker run -p 8080:80 -e C8Y_BASEURL=https://examples.cumulocity.com c8y-tutorial:0.2
```

### Create deployable package

```
$ docker save c8y-tutorial:0.2 > image.tar
$ zip c8y-tutorial-2 image.tar cumulocity.json
```