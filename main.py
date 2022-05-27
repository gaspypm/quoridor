import asyncio
import json
import sys
import websockets
from random import randint
import time

async def send(websocket, action, data):
    message = json.dumps(
        {
            'action': action,
            'data': data,
        }
    )
    print(message)
    await websocket.send(message)


async def connect(auth_token):
    uri = "wss://4yyity02md.execute-api.us-east-1.amazonaws.com/ws?token={}".format(auth_token)
    while True:
        try:
            print('connection to {}'.format(uri))
            async with websockets.connect(uri) as websocket:
                await play(websocket)
        except KeyboardInterrupt:
            print('Exiting...')
            break
        except Exception:
            print('Connection error.')
            time.sleep(3)


async def play(websocket):
    while True:
        try:
            request = await websocket.recv()
            request_data = json.loads(request)
            print_data(request_data)
            if request_data['event'] == 'challenge':
                await send(
                    websocket,
                    'accept_challenge',
                    {
                        'challenge_id': request_data['data']['challenge_id'],
                    },
                )
            if request_data['event'] == 'your_turn':
                await process_your_turn(websocket, request_data)
        except KeyboardInterrupt:
            print('Exiting...')
            break
        except Exception as e:
            print('error {}'.format(str(e)))
            break  # force login again


def print_data(request_data):
    if request_data['event'] == 'list_users':
        print('\nConnected users:', end=' ')
        print(*request_data['data']['users'], sep=', ')
    if request_data['event'] == 'game_over':
        print('\n––––––––––– GAME OVER –––––––––––')
        if request_data['data']['score_1'] > request_data['data']['score_2']:
            print('Congratulations ' + request_data['data']['player_1'] + '!')
            print('You won with ' + str(request_data['data']['score_1']) + ' points.')
        elif request_data['data']['score_1'] < request_data['data']['score_2']:
            print('Congratulations ' + request_data['data']['player_2'] + '!')
            print('You won with ' + str(request_data['data']['score_2']) + ' points.')
        else:
            print('You tied.')

    if request_data['event'] == 'your_turn':
        board_index = ['0', 'a', '1', 'b', '2', 'c', '3', 'd', '4', 'e', '5', 'f', '6', 'g', '7', 'h', '8']
        j = 0
        print('\nBoard:')
        print(' |0a1b2c3d4e5f6g7h8|\n |–––––––––––––––––|')
        for i in range(0, 289, 17):
            print(board_index[j] + '|' + (request_data['data']['board'])[i:i + 17] + '|')
            j += 1
        print('  –––––––––––––––––')

        print('Score ' + request_data['data']['player_1'] + ': ' + str(request_data['data']['score_1']))
        print('Score ' + request_data['data']['player_2'] + ': ' + str(request_data['data']['score_2']))


async def process_your_turn(websocket, request_data):
    if randint(0, 4) >= 1:
        await process_move(websocket, request_data)
    else:
        await process_wall(websocket, request_data)


async def process_move(websocket, request_data):
    side = request_data['data']['side']
    pawn_board = [[None for _ in range(9)] for _ in range(9)]

    for row in range(9):
        for col in range(9):
            string_row = request_data['data']['board'][17 * (row * 2): 17 * (row * 2) + 17]
            pawn_board[row][col] = string_row[col * 2]

    for row in range(9):
        for col in range(9):
            if pawn_board[row][col] == side:
                from_row = row
                from_col = col
                break

    if pawn_board[from_row + (1 if side == 'N' else -1)][from_col] != ' ':
        to_row, to_col = move_sideways(from_row, from_col)
    else:
        to_row, to_col = move_forward(side, from_row, from_col)

    await send(
        websocket,
        'move',
        {
            'game_id': request_data['data']['game_id'],
            'turn_token': request_data['data']['turn_token'],
            'from_row': from_row,
            'from_col': from_col,
            'to_row': to_row,
            'to_col': to_col,
        },
    )


def move_sideways(row, col):
    to_col = col + (1 if col < 8 else -1)
    to_row = row
    return to_row, to_col


def move_forward(side, row, col):
    to_row = row + (1 if side == 'N' else -1)
    to_col = col
    return to_row, to_col


async def process_wall(websocket, request_data):
    await send(
        websocket,
        'wall',
        {
            'game_id': request_data['data']['game_id'],
            'turn_token': request_data['data']['turn_token'],
            'row': randint(0, 8),
            'col': randint(0, 8),
            'orientation': 'h' if randint(0, 2) > 0 else 'v'
        },
    )


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        auth_token = sys.argv[1]
        asyncio.get_event_loop().run_until_complete(connect(auth_token))
    else:
        print('Please provide your auth_token.')
