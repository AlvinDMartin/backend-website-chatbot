import uvicorn
from Final_main_API import app


if __name__ == '__main__':
    uvicorn.run("debug_server:app", 
    host='127.0.0.1',
    port=4200, 
    reload=True,
    ssl_keyfile="./key.pem",
    ssl_certfile="./cert.pem"
    )