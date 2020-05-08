import json
#Usage
#Auxiliary set of files of manage_responses.py function
#Mainly functions that manage dictionairies
def get_final_json(server_response_text, query_result, audio_encode):
    json_trial = json.loads(server_response_text)
    user_response = query_result.query_text
    dialogflow_response = query_result.fulfillment_text
    json_trial.update({"user_response" : user_response})
    json_trial.update({"dialogflow_response" : dialogflow_response})
    json_trial.update({"dialogflow_response_in_B64" : audio_encode.decode()})
    json_final = json.dumps(json_trial)
    return json_final
