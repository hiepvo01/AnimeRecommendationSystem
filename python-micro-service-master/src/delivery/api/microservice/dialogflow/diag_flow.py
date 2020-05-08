import argparse,uuid,base64
import codecs, requests, json
import dialogflow_v2beta1 as dialogflow
#Usage:
# Gets responses from dialog flow
def get_diag_flow_responses(session_client,audio_encoding,audio_file_path,session_path,language_code):

    def request_generator(audio_config, audio_file_path):
        query_input = dialogflow.types.QueryInput(audio_config=audio_config)

        # The first request contains the configuration.
        yield dialogflow.types.StreamingDetectIntentRequest(
            session=session_path, query_input=query_input)

        # Here we are reading small chunks of audio data from a local
        # audio file.  In practice these chunks should come from
        # an audio input device.
        with open(audio_file_path, 'rb') as audio_file:
            while True:
                chunk = audio_file.read(4096)
                if not chunk:
                    break
                # The later requests contains audio data.
                yield dialogflow.types.StreamingDetectIntentRequest(
                    input_audio=chunk)
    
    sample_rate_hertz = 16000
    audio_config = dialogflow.types.InputAudioConfig(audio_encoding=audio_encoding, language_code=language_code,sample_rate_hertz=sample_rate_hertz)
    requests_audio = request_generator(audio_config, audio_file_path)
    responses = session_client.streaming_detect_intent(requests_audio)

    return responses