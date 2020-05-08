from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket
from delivery.api.microservice.dialogflow.detect_intent_stream import detect_intent_stream
from delivery.api.microservice.modelreps.model import similar_animes, part_id, anime_score
from delivery.api.microservice.dialogflow.writef import Base64decode
import ast
import json

#app = Starlette(debug=DEBUG, routes=routes)
app = Starlette(debug=False)

@app.websocket_route('/chat')
async def websocket_endpoint(websocket: WebSocket):
    print("chat connection accepted")
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        data= '['+data+']'
        keys_final = ast.literal_eval(data)
        a = list(keys_final)
        audio = Base64decode(a[2])
        print("hellooooooooooooo")
        audio_path = "src\\delivery\\api\\microservice\\dialogflow\\dialogflow_and_server_response\\User_Response.wav"

        result = json.loads(detect_intent_stream(a[0], a[1], audio_path, a[3]))

        await websocket.send_json(result)
        print(type(data))

@app.websocket_route('/search_full')
async def websocket_endpoint(websocket: WebSocket):
    print("search_full connection accepted")
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
        full_result = part_id(data)
        full_result.insert(0, "List of available full names are: ")

        print(full_result)
        await websocket.send_json(full_result)

@app.websocket_route('/search_similar')
async def websocket_endpoint(websocket: WebSocket):
    print("search_similar connection accepted")
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
        full_result = similar_animes(data)
        full_result.insert(0, "5 similar animes to " + data + " are: ")

        print(full_result)
        await websocket.send_json(full_result)