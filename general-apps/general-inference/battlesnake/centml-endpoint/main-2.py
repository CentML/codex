#BASIC SNAKE

import random
import typing


def info() -> typing.Dict:
    print("INFO")
    return {
        "apiversion": "1",
        "author": "vagias",  # TODO: Your Battlesnake Username
        "color": "#00FF00",  # TODO: Choose color
        "head": "space-helmet",  # TODO: Choose head
        "tail": "bolt",  # TODO: Choose tail
    }


def start(game_state: typing.Dict):
    print("GAME START")


def end(game_state: typing.Dict):
    print("GAME OVER\n")


def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    # Prevent moving backwards
    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False
    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False
    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False
    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # Step 1 - Prevent moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if my_head["y"] == board_height - 1:  # Don't move up if it's at the top edge
        is_move_safe["up"] = False
    if my_head["y"] == 0:  # Don't move down if it's at the bottom edge
        is_move_safe["down"] = False
    if my_head["x"] == 0:  # Don't move left if it's at the left edge
        is_move_safe["left"] = False
    if my_head["x"] == board_width - 1:  # Don't move right if it's at the right edge
        is_move_safe["right"] = False

    # Step 2 - Prevent colliding with itself
    my_body = game_state['you']['body']
    for segment in my_body:
        if my_head["x"] + 1 == segment["x"] and my_head["y"] == segment["y"]:
            is_move_safe["right"] = False
        if my_head["x"] - 1 == segment["x"] and my_head["y"] == segment["y"]:
            is_move_safe["left"] = False
        if my_head["y"] + 1 == segment["y"] and my_head["x"] == segment["x"]:
            is_move_safe["up"] = False
        if my_head["y"] - 1 == segment["y"] and my_head["x"] == segment["x"]:
            is_move_safe["down"] = False

    # Step 3 - Prevent colliding with other snakes
    opponents = game_state['board']['snakes']
    for snake in opponents:
        for segment in snake['body']:
            if my_head["x"] + 1 == segment["x"] and my_head["y"] == segment["y"]:
                is_move_safe["right"] = False
            if my_head["x"] - 1 == segment["x"] and my_head["y"] == segment["y"]:
                is_move_safe["left"] = False
            if my_head["y"] + 1 == segment["y"] and my_head["x"] == segment["x"]:
                is_move_safe["up"] = False
            if my_head["y"] - 1 == segment["y"] and my_head["x"] == segment["x"]:
                is_move_safe["down"] = False

    # Step 4 - Move towards food
    food = game_state['board']['food']
    if food:  # If food is present on the board
        closest_food = min(food, key=lambda f: abs(f["x"] - my_head["x"]) + abs(f["y"] - my_head["y"]))
        if closest_food["x"] > my_head["x"] and is_move_safe["right"]:
            next_move = "right"
        elif closest_food["x"] < my_head["x"] and is_move_safe["left"]:
            next_move = "left"
        elif closest_food["y"] > my_head["y"] and is_move_safe["up"]:
            next_move = "up"
        elif closest_food["y"] < my_head["y"] and is_move_safe["down"]:
            next_move = "down"
        else:
            next_move = random.choice([move for move, isSafe in is_move_safe.items() if isSafe])
    else:
        # If no food, choose a random move from the safe ones
        safe_moves = [move for move, isSafe in is_move_safe.items() if isSafe]
        if len(safe_moves) == 0:
            print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
            next_move = "down"
        else:
            next_move = random.choice(safe_moves)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})