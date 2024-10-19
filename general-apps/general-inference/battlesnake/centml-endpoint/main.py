import random
import typing
import heapq
from collections import deque
import time

MAX_DEPTH = 3  # Depth of the minimax search tree
TIME_LIMIT = 0.25  # Maximum time in seconds per move

def info() -> typing.Dict:
    print("INFO")
    return {
        "apiversion": "1",
        "author": "vagias",
        "color": "#FF0000",  # Hex color for red
        "head": "space-helmet",
        "tail": "bolt",
    }

def start(game_state: typing.Dict):
    print("GAME START", game_state)

def end(game_state: typing.Dict):
    print("GAME OVER\n", game_state)

# Directions and their respective x, y coordinate changes
directions = {
    "up": (0, 1),
    "down": (0, -1),
    "left": (-1, 0),
    "right": (1, 0),
}

def move(game_state: typing.Dict) -> typing.Dict:
    start_time = time.time()

    my_head = game_state["you"]["body"][0]  # Head position
    my_body = game_state["you"]["body"]  # Body positions
    health = game_state["you"]["health"]
    opponents = [snake for snake in game_state['board']['snakes'] if snake['id'] != game_state['you']['id']]
    board = game_state['board']

    # Get valid moves
    valid_moves = get_valid_moves(my_head, my_body, opponents, board)

    if not valid_moves:
        # No valid moves, choose a default move
        print(f"MOVE {game_state['turn']}: No valid moves available! Moving up")
        return {"move": "up"}

    best_score = float('-inf')
    best_move = None

    for move_direction, new_head in valid_moves.items():
        new_body = [new_head] + my_body[:-1]  # Simulate moving forward
        score = minimax(game_state, new_head, new_body, opponents, MAX_DEPTH, False, float('-inf'), float('inf'), start_time)
        if score > best_score:
            best_score = score
            best_move = move_direction

        # Time check to prevent timeout
        if time.time() - start_time > TIME_LIMIT:
            print("Time limit reached during minimax calculation")
            break

    if best_move is None:
        # Fallback to a random valid move
        best_move = random.choice(list(valid_moves.keys()))

    print(f"MOVE {game_state['turn']}: {best_move} with score {best_score}")
    return {"move": best_move}

def get_valid_moves(head, body, opponents, board):
    board_width = board['width']
    board_height = board['height']
    occupied = get_occupied_positions(body, opponents)
    valid_moves = {}
    for direction, (dx, dy) in directions.items():
        new_x = head['x'] + dx
        new_y = head['y'] + dy
        new_head = {'x': new_x, 'y': new_y}
        if is_safe(new_head, occupied, board_width, board_height):
            valid_moves[direction] = new_head
    return valid_moves

def is_safe(position, occupied, board_width, board_height):
    x, y = position['x'], position['y']
    if x < 0 or x >= board_width or y < 0 or y >= board_height:
        return False
    if (x, y) in occupied:
        return False
    return True

def get_occupied_positions(my_body, opponents):
    occupied = set()
    for segment in my_body[:-1]:  # Exclude tail as it moves
        occupied.add((segment['x'], segment['y']))
    for snake in opponents:
        for segment in snake['body']:
            occupied.add((segment['x'], segment['y']))
    return occupied

def minimax(game_state, my_head, my_body, opponents, depth, is_maximizing_player, alpha, beta, start_time):
    # Time check
    if time.time() - start_time > TIME_LIMIT:
        return evaluate(game_state, my_head, my_body, opponents)

    # Base case: depth limit reached or game over
    if depth == 0 or is_game_over(my_head, my_body, opponents, game_state['board']):
        return evaluate(game_state, my_head, my_body, opponents)

    if is_maximizing_player:
        max_eval = float('-inf')
        valid_moves = get_valid_moves(my_head, my_body, opponents, game_state['board'])
        if not valid_moves:
            return evaluate(game_state, my_head, my_body, opponents)
        for move_direction, new_head in valid_moves.items():
            new_body = [new_head] + my_body[:-1]
            eval = minimax(game_state, new_head, new_body, opponents, depth - 1, False, alpha, beta, start_time)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval
    else:
        min_eval = float('inf')
        for opponent in opponents:
            opponent_head = opponent['body'][0]
            opponent_body = opponent['body']
            opponent_board = game_state['board']
            valid_moves = get_valid_moves(opponent_head, opponent_body, [game_state['you']] + [s for s in opponents if s['id'] != opponent['id']], opponent_board)
            if not valid_moves:
                continue  # Skip if opponent has no valid moves
            for move_direction, new_head in valid_moves.items():
                new_body = [new_head] + opponent_body[:-1]
                new_opponent = {'body': new_body, 'id': opponent['id'], 'health': opponent['health']}
                new_opponents = [new_opponent] + [s for s in opponents if s['id'] != opponent['id']]
                eval = minimax(game_state, my_head, my_body, new_opponents, depth - 1, True, alpha, beta, start_time)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cutoff
        return min_eval

def evaluate(game_state, my_head, my_body, opponents):
    score = 0

    # Survival is the highest priority
    if is_collision(my_head, my_body, opponents, game_state['board']):
        return float('-inf')

    # Distance to food
    food = game_state['board']['food']
    if food:
        distances = [manhattan_distance(my_head, f) for f in food]
        min_distance = min(distances)
        score -= min_distance * 1.5  # Closer to food is better
    else:
        min_distance = 0  # No food, neutral impact

    # Health
    score += game_state['you']['health'] * 0.5

    # Control of space
    space = flood_fill(my_head, my_body, opponents, game_state['board'])
    score += len(space) * 1.0  # More accessible space is better

    # Avoid being close to larger opponents
    for opponent in opponents:
        if len(opponent['body']) >= len(my_body):
            distance = manhattan_distance(my_head, opponent['body'][0])
            if distance < 3:
                score -= (3 - distance) * 10  # Penalize proximity to larger snakes

    return score

def is_game_over(my_head, my_body, opponents, board):
    return is_collision(my_head, my_body, opponents, board)

def is_collision(head, body, opponents, board):
    occupied = get_occupied_positions(body, opponents)
    return not is_safe(head, occupied, board['width'], board['height'])

def manhattan_distance(a, b):
    return abs(a['x'] - b['x']) + abs(a['y'] - b['y'])

def flood_fill(head, my_body, opponents, board):
    board_width = board['width']
    board_height = board['height']
    occupied = get_occupied_positions(my_body, opponents)
    queue = deque()
    visited = set()
    queue.append((head['x'], head['y']))
    visited.add((head['x'], head['y']))

    while queue:
        x, y = queue.popleft()
        for dx, dy in directions.values():
            nx, ny = x + dx, y + dy
            if 0 <= nx < board_width and 0 <= ny < board_height:
                if (nx, ny) not in occupied and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    return visited

if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})