"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
from firebase import firebase

import datetime
from datetime import datetime as dt

firebase = firebase.FirebaseApplication("https://spajam2018-dbd7e.firebaseio.com/", None)


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    result = firebase.get('/end', None)
    today = dt.today() + datetime.timedelta(hours=9)
    last = dt.strptime(result, '%Y-%m-%d %H:%M:%S')
    dist = last - today
    dist = str(int(dist.total_seconds() / 60))
    if int(dist) > 0:
        speech_output = "ようこそ「ペットイ」へ！残り" + dist +"分です！"
        reprompt_text = "ようこそ「ペットイ」へ！残り" + dist +"分です！"
        should_end_session = True
    else:
        speech_output = "ようこそ「ペットイ」へ！先にアプリから時間を入力してね"
        reprompt_text = "ようこそ「ペットイ」へ！先にアプリから時間を入力してね"
        should_end_session = True
    
    session_attributes = {}
    card_title = "Welcome"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "お疲れ様！"
    # タイマー終了処理
    today = dt.today() + datetime.timedelta(hours=9) + datetime.timedelta(seconds=1)
    today = today.strftime("%Y-%m-%d %H:%M:%S")
    result = firebase.put('', '/end', today)
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def set_color_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = True

    if 'Color' in intent['slots']:
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def set_greeting_text(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = True

    # firebaseの書き換え
    if 'setting' in intent['slots']:
        try:
            setting = intent['slots']['setting']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
            minute = intent['slots']['minute']['value'][:-1]
        except:
            speech_output = ''
            reprompt_text = speech_output
            return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
        
        result = firebase.get('/end', None)
        last = dt.strptime(result, '%Y-%m-%d %H:%M:%S')
        
        if minute == "十五":
            minute = 15
        elif minute == "三十":
            minute = 30
        elif minute == "四十五":
            minute = 45
        elif minute == "六十":
            minute = 60
        
        if setting == '減少':
            speech_output = str(minute) + '分減らしました！'
            last = last - datetime.timedelta(minutes=int(minute))
        elif setting == '増加':
            speech_output = str(minute) + '分増やしました！'
            last = last + datetime.timedelta(minutes=int(minute))
        else:
            speech_output = "頑張って"
    else:
        speech_output = "頑張って"
    
    last = last.strftime("%Y-%m-%d %H:%M:%S")
    firebase.put('', '/end', last)
    
    reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def set_stop_text(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = True

    # スロットの中にlanguage変数があるか確認する
    if 'setting' in intent['slots']:
        try:
            setting = intent['slots']['setting']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
        except:
            speech_output = ''
            reprompt_text = speech_output
            return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
        
            
            
        if setting == '停止':
            speech_output = 'タイマーを終了します！お疲れ様！'
            should_end_session = True
    else:
        speech_output = "頑張って"

    
    today = dt.today() + datetime.timedelta(hours=9) + datetime.timedelta(seconds=1)
    today = today.strftime("%Y-%m-%d %H:%M:%S")
    firebase.put('', '/end', today)
    
    reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
        
def set_leave_text(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = True
    
    #firebaseから残り時間の取得 0分なら終わってる内容を話す
    result = firebase.get('/end', None)
    today = dt.today() + datetime.timedelta(hours=9)
    last = dt.strptime(result, '%Y-%m-%d %H:%M:%S')
    dist = last - today
    dist = str(int(dist.total_seconds() / 60))
    
    if int(dist) > 0:
        speech_output = "あと"+dist+"分です！"
    else:
        speech_output = "既に終わっています！お疲れ様！"
        should_end_session = True

    reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        

def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = True

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "greeting":
        return set_greeting_text(intent, session)
    elif intent_name == "stop":
        return set_stop_text(intent, session)
    elif intent_name == "leave":
        return set_leave_text(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
