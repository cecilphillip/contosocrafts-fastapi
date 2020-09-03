# ContosoCrafts (Fastapi Edition)

This is a python port of https://github.com/cecilphillip/ContosoCrafts/tree/dapr. This Contoso Crafts demo is a single page e-store the servers as a example for build microservice style applications with [DAPR](https://dapr.io/).

## Spinning up the environment

First, spin up the supporting infrastructure components.

```bash
> docker-compose -f docker-compose-infra.yml up -d
```
> The services in this compose file bind to various ports on your host machine. Consider changing these bindings in `docker-compose-infra.yml` if you have another services listening on those ports.

Next, launch the application containers and sidecars.

```bash
> docker-compose up -d
```

> The main web application binds to port 80 on your host machine. Consider changing this port binding in `docker-compose-dapr.yml` if you have another service listening on that port.

### Requirements

- Docker
- Python 3.8.0 or above
- Visual Studio Code
- Python extension for Visual Studio Code

## What's in the box

### Application Components

- [Contoso Website](src/website)
- [Products API](src/productsapi)
- [Checkout Processor](src/messageprocessor)

### Python packages used

- [fastapi](https://fastapi.tiangolo.com/)
- [motor](https://motor.readthedocs.io/en/stable/)
- [uvicorn](http://www.uvicorn.org/)
- [aiohttp](https://docs.aiohttp.org/)

### Infrastructure Components

- [MongoDB](https://docs.mongodb.com/) - Products data
- [RabbitMQ](https://www.rabbitmq.com/) - Message Broker
- [Redis](https://redis.io/) - State store
- [zipkin](https://zipkin.io/) - Distributed tracing
