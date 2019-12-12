import delivery.api.microservice.dialogflow.writef as w1
import delivery.api.microservice.dialogflow.handle_data as hd
import argparse,uuid,base64
import codecs, requests, json
import dialogflow_v2beta1 as dialogflow
# Usage
# Writes outputs of dialog file in output files present in dialogflow_and_server_response
def handle_responses(responses,session_client_audio,session_path,audio_file_path,language_code):
    
    response,query_result=w1.print_transcript(responses)

    text_input = dialogflow.types.TextInput(text=query_result.query_text, language_code=language_code)
    query_input_audio = dialogflow.types.QueryInput(text=text_input)
    output_audio_config = dialogflow.types.OutputAudioConfig(audio_encoding=dialogflow.enums.OutputAudioEncoding.OUTPUT_AUDIO_ENCODING_LINEAR_16)

    response = session_client_audio.detect_intent(session=session_path, query_input=query_input_audio, output_audio_config=output_audio_config)

    output_audio_convert = response.output_audio.decode('ISO-8859-1')
    response.output_audio = output_audio_convert.encode('utf-8')
    audio_encode = base64.b64encode(response.output_audio)

    d1 = {}
    server_response_text = json.dumps(d1)
    json_final=hd.get_final_json(server_response_text, query_result, audio_encode)
    
    return  json_final