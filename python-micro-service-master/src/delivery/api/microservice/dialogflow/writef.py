import codecs, base64
#Usage
#Auxiliary set of files of manage_responses.py function
#Mainly functions writes data in files and in command line
def write_expected_audio(query_result):
    with open('src/delivery/api/microservice/dialogflow/dialogflow_and_server_response/expected_audio.txt', 'wb') as expected_audio:
        expected_audio.write(query_result.query_text.encode())
        print('Expected Audio written to file "expected_audio.txt"')
        expected_audio.close()
        
def write_output_wav(response):
        print('Fulfillment text: {}\n'.format(response.query_result.fulfillment_text))
        with codecs.open('botResponse.wav', 'wb') as out:
                print(response.output_audio[0:100])
                out.write(response.output_audio)
                print('Audio content written to file "botResponse.wav"')

def write_audio_encode(response):
    audio_encode = base64.b64encode(response.output_audio)
    with open('src/delivery/api/microservice/dialogflow/dialogflow_and_server_response/encode.txt', 'wb') as encode_out:
        encode_out.write(audio_encode)
        print('Base64 response written to file "encode.txt"')
        encode_out.close()

def write_server_response_text(server_response_text):
    with open('src/delivery/api/microservice/dialogflow/dialogflow_and_server_response/server_response.json', 'wb') as server_response_file:
        server_response_file.write(server_response_text)
        print('Server Response written to file "server_response.json"')
        server_response_file.close()

def Base64decode(audio64):
    audio64_decode = base64.b64decode(audio64)
    with codecs.open('src/delivery/api/microservice/dialogflow/dialogflow_and_server_response/User_Response.wav', 'wb') as user_response_file:
        user_response_file.write(audio64_decode)
        print('User Response written to file "User_response.wav"')
        user_response_file.close()

def print_transcript(responses):

    print('=' * 20)
    for response in responses:
        print('Intermediate transcript: "{}".'.format(
                response.recognition_result.transcript))
    # Note: The result from the last response is the final transcript along
    # with the detected content.
    query_result = response.query_result 
    print('=' * 20)

    return response,query_result

def full_print(query_result):
    print('Query text: {}'.format(query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        query_result.intent.display_name,
        query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        query_result.fulfillment_text))


