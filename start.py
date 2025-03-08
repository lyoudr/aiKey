import sys
import uvicorn


def start_app(port: int):
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        app_dir="src",
        h11_max_incomplete_event_size=335544320,
        reload=True,
    )


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    start_app(port=port)
