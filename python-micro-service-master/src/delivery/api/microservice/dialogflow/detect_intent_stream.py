import delivery.api.microservice.dialogflow.diag_flow as df
import delivery.api.microservice.dialogflow.manage_responses as mr
import argparse,uuid,base64
import codecs, requests, json
import dialogflow_v2beta1 as dialogflow
import os

# [START dialogflow_detect_intent_streaming]
def detect_intent_stream(project_id, session_id, audio_file_path, language_code):

    session_client = dialogflow.SessionsClient()
    session_client_audio = dialogflow.SessionsClient()

    # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
    sample_rate_hertz = 48000
    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    session_path = session_client.session_path(project_id, session_id)

    responses=df.get_diag_flow_responses(session_client,audio_encoding,audio_file_path,session_path,language_code)
    
    json_final=mr.handle_responses(responses,session_client,session_path,audio_file_path,language_code)
    return json_final
    
# [END dialogflow_detect_intent_streaming]
