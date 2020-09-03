from fastapi import FastAPI, Request, Body
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import socket
import platform
import logging

import products_service
from products_service import ProductService, StateService, PubSubService

extra = {'host_name': socket.gethostname(), 'system': platform.uname()[0]}
log_format = f' %(levelname)s:  {extra["system"]} {extra["host_name"]} - %(asctime)s - %(name)s - %(funcName)s - %(message)s'
logging.basicConfig(format=log_format, level=logging.INFO)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    logging.info('Retrieving products')
    products = await ProductService.get_products()    
    return templates.TemplateResponse("index.html", {"request": request, "products": products})


@app.get("/showCart")
async def show_cart(request: Request):
    shopping_cart_items = await StateService.get_cart_state()
    logging.info('Retrieving shopping cart state')
    return templates.TemplateResponse("shoppingcart.html", {"request": request, "items": shopping_cart_items})


@app.post("/addToCart")
async def add_to_cart(request: Request, id: str = Body(..., embed=True)):
    product = await ProductService.get_product(id)
    logging.info(f'Adding product to cart => {product.id}')
    await StateService.add_to_cart(product)


@app.post("/checkout")
async def cart_checkout(request: Request):
    shopping_cart_items = await StateService.get_cart_state()
    logging.info(f'Publishing checkout message')
    await PubSubService.publish_message('checkout', shopping_cart_items)


@app.get("/privacy")
async def show_privacy_policy(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})


@app.on_event("shutdown")
def shutdown():
    ProductService.close_aio_client()
    StateService.close_aio_client()
    PubSubService.close_aio_client()
    logging.info(f"Peace out. I'm outta here...ls")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
