import random as r
import cbrain.questions as q

GREETING_TOKENS = [
    'hello',
    'hi',
    'greetings',
    'konnichiwa',
    'bonjour',
    'hola',
    'sup',
    'hey',
    'what is your name?',
    'what\'s your name?',
    'are you a bot?',
    'are you a human?',
    'hello, how are you?',
]

#  in case we don't know what to say
DEFULT_RESPONSES = [
    'I don\'t understand.',
    'I don\'t know what you mean.',
    'Please try again.',
    'Can you rephrase that?',
    'I don\'t know what to say.',
]

# Game variables
madlibs_responses = []  # stores the user's responses to the madlibs questions
playing = False
asked_question = False
asked_question_i = 0
madlib_qi = 0  # madlibs question index


def greet():
    '''Greets the user'''
    return r.choice(q.greetings)


def ask_for_playing_madlibs():
    '''Asks the user if they want to play madlibs'''
    invite = r.choice(q.ask_for_playing_madlibs)
    invite += ' ' + '(Type "yes", "yeah", or "play" to begin)'
    return invite

def ask_madlibs_question():
    '''Returns a list of madlibs questions'''
    global madlib_qi
    madlib_question = q.madlibs_questions[madlib_qi]
    madlib_qi = madlib_qi + 1
    return madlib_question


def goodbye():
    '''Says goodbye to the user'''
    return r.choice(q.goodbye)


def ask_question():
    '''Asks the user a question'''
    global asked_question
    global asked_question_i

    asked_question = True
    asked_question_i = r.randint(0, len(q.questions) - 1)
    return q.questions[asked_question_i]


def get_response(user_input):
    '''Returns a response to the user's input'''
    global asked_question

    user_input = user_input.lower()

    if playing:
        return play_madlibs(user_input)

    if asked_question:
        asked_question = False
        return q.responses[asked_question_i]

    if user_input in GREETING_TOKENS:
        return greet()

    elif 'play' in user_input or 'yeah' in user_input or 'yes' in user_input:
        return play_madlibs('play')

    elif 'goodbye' in user_input or 'bye' in user_input or 'see you later' in user_input:
        return goodbye()

    if r.random() < 0.5:
        return ask_question()
    else:
        return ask_for_playing_madlibs()


def play_madlibs(user_input=None):
    '''Plays madlibs with the user'''
    global madlib_qi
    global playing

    if user_input is None:
        return ask_for_playing_madlibs()

    if user_input == 'stop playing' and playing:
        playing = False
        return 'Okay, goodbye! You don\'t have to play if you don\'t want to.'

    if user_input == 'play' and not playing:
        playing = True
        return 'Let\'s play madlibs (Type "stop playing" to abort)!\n\n' + ask_madlibs_question()

    if len(user_input.split()) != 1:
        return 'Please enter only one word as I\'m asking for'

    madlibs_responses.append(user_input)

    if madlib_qi == len(q.madlibs_questions):
        playing = False
        res = 'Here\'s your madlibs story:    ' + \
            q.generate_madlibs(madlibs_responses)
        return res

    return ask_madlibs_question()
