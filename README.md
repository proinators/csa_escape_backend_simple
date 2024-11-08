# CSA Space Escape - Backend

The backend service behind CSA's Space Escape event, for ATMOS 2024. A unified Socket based experience for managing the whole game, with multiple player devices, the main screen and an admin control panel.

## Getting Started

To get started with the CSA Space Escape API, clone this repository and install the required dependencies listed in `requirements.txt`.

```sh 
pip install -r requirements.txt
```

Run the application using Uvicorn:
```sh
uvicorn main:app --reload
```

#### Real-time Communication
This API uses Socket.IO for real-time communication. Connect to the Socket.IO server at `/socket.io` to receive live updates during the game.

### Development
This project uses Uvicorn as the ASGI server, Starlette for the web framework, and Socket.IO for real-time communication. Ensure you have Python 3.6+ installed to run this project.


## API Reference
TODO