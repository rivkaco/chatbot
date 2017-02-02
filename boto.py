"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import random

# bottle allows you to see how to connect back and front end.
# ajax request sends from frontto backend.
# from now on- run server, there will be a get request which will be shown to user
@route('/', method='GET')
def index():
    return template("chatbot.html")
# return template is what is shown to the user, so put html file.
# '/' specifies the path
#
user_different_messages = ["how are you", "good", 'yes', "fun", "animal", "hi", "love", "sup", "can i", "you", "?", "hello"]
responses = ["boring question, how are you?", "I'm glad you are doing well", "is that what you think?", "party!", "I LOVE DOGS!", "hi there!", "I love you too", "Not much. what's up?", "no!", "of course", "Good question!", "nice to meet you!"]
animation_response = ["bored", "ok", "crying", "dancing", "dog", "excited", "giggling", "heartbroke", "inlove", "laughing", "money", "no", "takeoff", "waiting"]
cursewords = ["fuck", "shit", "bitch"]
ask_for_joke = ["joke"]
jokes = ["Today a man knocked on my door and asked for a small donation towards the local swimming pool. I gave him a glass of water.",
         "Feeling pretty proud of myself. The Sesame Street puzzle I bought said 3-5 years, but I finished it in 18 months.",
         "Intelligence is like an underwear. It is important that you have it, but not necessary that you show it off.",
         "A computer once beat me at chess, but it was no match for me at kick boxing.",
         "What did one ocean say to the other ocean? Nothing, they just waved.",
         "Why did the bee get married? Because he found his honey."]

def chatbot_curse(user_message):
    for c in cursewords:
        if c in user_message:
            return {"animation": "afraid", "msg": "Please don't use such horrible language!"}
    return None

def chatbot_responses(user_message):
    for message, r, a in zip(user_different_messages, responses, animation_response):
        if user_message.find(message) != -1:
            return {"animation": a, "msg": r}
    return None

def chatbot_joke(user_message):
    if any(j in user_message for j in ask_for_joke):
        return {"animation": "laughing", "msg": random.choice(jokes)}
    return None

def chatbot_default():
    return {"animation": "confused", "msg": "Sorry, that wasn't clear. Can you please repeat?"}

number_of_attempts = {"counter": 0}
@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    number_of_attempts["counter"] += 1
    if (number_of_attempts["counter"] == 1):
        return json.dumps({"animation" :"crying", "msg": "nice name " + user_message})
    result = chatbot_curse(user_message)
    if not result:
        result = chatbot_responses(user_message)
    if not result:
        result = chatbot_joke(user_message)
    if not result:
        result = chatbot_default()
    return json.dumps(result)

@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})

# static file handlers
@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()