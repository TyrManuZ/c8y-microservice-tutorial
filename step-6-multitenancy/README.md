# Creating a multi tenant microservice

## Goal

The goal of this step is change the microservice from a single tenant deployment to a multi tenant deployment

## Key concepts

- Multi tenancy
- Polling for subscribed tenants

## Steps

1. Change isolation in manifest file
2. Utilize service bootstrap credentials for polling subscribed tenants

## Commands

All commands assume that you are located in the folder of the current step

### Build docker

```
$ docker build . -t c8y-tutorial:0.6
```

### Run docker locally

As we are now have a multi tenant microservice we need to inject the bootstrap user instead of a "normal" user. How to aquire the user you can check below.
```
$ docker run -p 8080:80 -e C8Y_BOOTSTRAP_TENANT=examples -e C8Y_BOOTSTRAP_USER=servicebootstrap_c8y-tutorial-6 -e C8Y_BOOTSTRAP_PASSWORD=myPassword -e C8Y_BASEURL=https://examples.cumulocity.com c8y-tutorial:0.6
```

### Create deployable package

```
$ docker save c8y-tutorial:0.5 > image.tar
$ zip c8y-tutorial-5 image.tar cumulocity.json
```

### Aquire service bootstrap user

The service bootstrap user is unique for each microservice. If you need it for local testing you can get it via REST. You will need to create the microservice application first and then execute the following REST request.

Request:
```
GET /application/applications/{{applicationId}}/bootstrapUser HTTP/1.1
Host: examples.cumulocity.com
Authorization: Basic ...
```

Response:
```
{
    "name": "servicebootstrap_c8y-tutorial-6",
    "password": "myPassword",
    "tenant": "examples"
}
```