# Using service users

## Goal

The goal of this step is to define your own permission objects for securing your microservice and instead of using the users credentials for Cumulocity access we will use the service user.

## Key concepts

- Required permissions
- New permission roles
- Single tenant service user

## Steps

1. Add required and new permissions to the manifest file
2. Access service user from environment to access Cumulocity

## Commands

All commands assume that you are located in the folder of the current step

### Build docker

```
$ docker build . -t c8y-tutorial:0.5
```

### Run docker locally

As we are now using the service user we need to inject one user locally. You can either create a specific user with the same rights as configured or use your own one if it has enough permissions.
```
$ docker run -p 8080:80 -e C8Y_BASEURL=https://examples.cumulocity.com -e C8Y_TENANT=examples -e C8Y_USER=myUser -e C8Y_PASSWORD=myPassword c8y-tutorial:0.5
```

### Create deployable package

```
$ docker save c8y-tutorial:0.5 > image.tar
$ zip c8y-tutorial-5 image.tar cumulocity.json
```