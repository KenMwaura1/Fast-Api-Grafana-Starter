import uvicorn


host="0.0.0.0"
port=8001
app="app.main:app"



if __name__ == '__main__':
    uvicorn.run(app, host=host, port=port)