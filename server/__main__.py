from uvicorn import run

if __name__ == "__main__":
    run(
        app="server:app",
        host="0.0.0.0",
        port=8080,
        http="httptools",
        loop="uvloop",
        interface="asgi3",
        factory=True,
        reload=True,
    )
