import uvicorn
from Final_main_API import app


if __name__ == '__main__':
    uvicorn.run("debug_server:app",host='10.170.0.2',port=4200,reload=True)