from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from cloudevents.http import CloudEvent, from_http, from_json

api = FastAPI()


@api.get('/dapr/subscribe')
async def subscribe():
    payload = [dict(
        pubsubname="rabbitmqbus",
        topic="checkout",
        route="/process/checkout"
    )]
    return JSONResponse(payload)


@api.post('/process/checkout')
async def checkout_order(request: Request):
    body: bytes = await request.body()
    event: CloudEvent = from_json(body)
    print(event.data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host='0.0.0.0', port=8000)
