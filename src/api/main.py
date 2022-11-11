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

    """
    print(main(board.dict()))

    return main(board.dict())
    board = await board.json()
    result = main(board)
    return result
