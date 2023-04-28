"""
This script sets up a FastAPI web service to create a board given the input JSON data
representing a bug. The API receives a bug data and returns the evaluation result for that
board. The API accepts CORS requests, allowing cross-origin requests from any origin.

To run the FastAPI web service, simply execute the script from the command line:
uvicorn main:app --reload


The FastAPI server will start, and the API will be available at http://127.0.0.1:8000
"""

from os import system, getenv
from subprocess import check_output

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api.boardTypes import Bug
from engine.eval import main


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/board")
async def create_board(board: Bug):
    """
    FastAPI endpoint that receives a JSON data representing a bug and returns the evaluation result for the board.

    Argumments:
    board (Bug): An instance of the Bug class representing the bug data.

    Returns:
        dict: A dictionary containing the evaluation result for the board, or an error message if an exception is raised.
    """
    try:
        result = main(board.dict())
    except Exception as e:
        return {"error": str(e)}
    return result
