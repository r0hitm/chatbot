import random as r
import cbrain.questions as q


class Chatbot:
    def __init__(self):
        self.__greeting_tokens = [
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

        # in case we don't know what to say
        self.__default_responses = [
            'I don\'t understand.',
            'I don\'t know what you mean.',
            'Please try again.',
            'Can you rephrase that?',
            'I don\'t know what to say.',
        ]

        # Game variables
        self.__madlibs_responses = []  # stores the user's responses to the madlibs questions
        self.__playing = False
        self.__asked_question = False
        self.__asked_question_i = 0
        self.__madlib_qi = 0  # madlibs question index

    def __reset_madlibs(self):
        '''Resets the madlibs game'''
        self.__madlibs_responses = []
        self.__playing = False
        self.__asked_question = False
        self.__asked_question_i = 0
        self.__madlib_qi = 0

    def __greet(self):
        '''Greets the user'''
        return r.choice(q.greetings)

    def __ask_for_playing_madlibs(self):
        '''Asks the user if they want to play madlibs'''
        invite = r.choice(q.ask_for_playing_madlibs)
        invite += ' ' + '(Type "yes", "yeah", or "play" to begin)'
        return invite

    def __ask_madlibs_question(self, repeat=False):
        '''Returns a list of madlibs questions'''
        madlib_question = q.madlibs_questions[self.__madlib_qi]
        print(f"### DEBUG ###\n repeat={repeat}\n")
        if not repeat:
            self.__madlib_qi += 1
        return madlib_question

    def __goodbye(self):
        '''Says goodbye to the user'''
        return r.choice(q.goodbye)

    def __ask_question(self):
        '''Asks the user a question'''
        self.__asked_question = True
        self.__asked_question_i = r.randint(0, len(q.questions) - 1)
        return q.questions[self.__asked_question_i]

    def get_response(self, user_input):
        '''Returns a response to the user's input'''

        print(
            f"### DEBUG ###\n user_input = {user_input}, playing = {self.__playing}\n")

        if user_input == None:
            return self.__greet()

        if self.__asked_question:
            self.__asked_question = False
            return q.responses[self.__asked_question_i]

        user_input = user_input.strip().lower()

        if self.__playing:
            return self.__play_madlibs(user_input)

        if user_input in self.__greeting_tokens:
            return self.__greet()

        elif not self.__playing and 'play' in user_input or 'yeah' in user_input or 'yes' in user_input or 'sure' in user_input:
            return self.__play_madlibs(True)

        elif 'goodbye' in user_input or 'bye' in user_input or 'see you later' in user_input:
            return self.__goodbye()

        if r.random() < 0.5:
            # print('### DEBUG ###\nAsking question\n')
            return self.__ask_question()
        else:
            # print('### DEBUG ###\nAsking for playing madlibs\n')
            return self.__ask_for_playing_madlibs()

    def __play_madlibs(self, user_input):
        '''Plays madlibs with the user'''

        if user_input == True:
            self.__playing = True
            return 'Let\'s play madlibs (Type "stop playing" to abort)!\n\n' + self.__ask_madlibs_question()

        if user_input == 'stop playing' and self.__playing:
            self.__playing = False
            return 'Okay, goodbye! You don\'t have to play if you don\'t want to.'

        if len(user_input.split()) != 1:
            return 'Please enter only one word as I\'m asking for'

        self.__madlibs_responses.append(user_input)

        if self.__madlib_qi == len(q.madlibs_questions):
            self.__reset_madlibs()
            res = 'Here\'s your madlibs story:    ' + \
                q.generate_madlibs(self.__madlibs_responses)
            return res

        return self.__ask_madlibs_question()
