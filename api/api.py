from os import system, getenv
from subprocess import check_output

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from boardTypes import Board
from eval import main


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/board/")
async def create_board(board: Request):
    """

    """
    board = await board.json()
    print(board)
    result = main(board, board["xValue"], board["yValue"])
    return result
