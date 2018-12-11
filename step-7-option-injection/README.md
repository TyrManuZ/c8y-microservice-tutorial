# Access injected tenant options

## Goal

The goal of this step is show how the platform injects tenant options of the microservice directly into each request. Encrypted tenant options will be automatically decrypted in this process

## Key concepts

- (encrypted) tenant options for microservices

## Steps

1. Add REST handler that outputs all HTTP headers of the request

## Commands

All commands assume that you are located in the folder of the current step

### Build docker

```
$ docker build . -t c8y-tutorial:0.7
```

### Run docker locally

```
$ docker run -p 8080:80 -e C8Y_BOOTSTRAP_TENANT=examples -e C8Y_BOOTSTRAP_USER=servicebootstrap_c8y-tutorial-6 -e C8Y_BOOTSTRAP_PASSWORD=myPassword -e C8Y_BASEURL=https://examples.cumulocity.com c8y-tutorial:0.7
```

### Create deployable package

```
$ docker save c8y-tutorial:0.7 > image.tar
$ zip c8y-tutorial-7 image.tar cumulocity.json
```

### Create tenant options

The category of the tenant option needs to equal the contextPath of the microservice to be injected into the requests.

Request:
```
POST /tenant/options HTTP/1.1
Host: examples.cumulocity.com
Authorization: Basic ...
Content-Type: application/json
Accept: application/json

{
    "category": "c8y-tutorial-7",
    "key": "myFirstTenantOption",
    "value": "unsecureValue"
}
```

In order to get the tenant option encrypted you need to prefix the key with "credentials.". Encrypted tenant options will be returned on the normal API only in encrypted form.

Request:
```
POST /tenant/options HTTP/1.1
Host: examples.cumulocity.com
Authorization: Basic ...
Content-Type: application/json
Accept: application/json

{
    "category": "c8y-tutorial-7",
    "key": "credentials.secureKey",
    "value": "secureValue"
}
```