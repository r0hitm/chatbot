import random as r
import cbrain.questions as q


class Chatbot:
    '''Chatbot class that handles the chatbot's responses
    Each user has their own instance of this class'''

    def __init__(self):
        '''Initializes the chatbot'''
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

        # Default responses in case the chatbot doesn't know what to say
        self.__default_responses = [
            'I don\'t understand.',
            'I don\'t know what you mean.',
            'Please try again.',
            'Can you rephrase that?',
            'I don\'t know what to say.',
        ]

        # Madlibs Game variables
        # stores the user's responses to the madlibs questions
        self.__madlibs_responses = []
        self.__playing = False          # whether or not the user is playing madlibs
        self.__asked_question = False   # whether or not the chatbot has asked a question
        self.__asked_question_i = 0     # index of the question the chatbot asked
        self.__madlib_qi = 0            # index of the madlibs question

    def __reset_madlibs(self):
        '''Resets the madlibs game variables'''
        self.__madlibs_responses = []
        self.__playing = False
        self.__asked_question = False
        self.__asked_question_i = 0
        self.__madlib_qi = 0

    def __greet(self):
        '''returns a random greeting'''
        return r.choice(q.greetings)

    def __ask_for_playing_madlibs(self):
        '''returns a random invitation to play madlibs'''
        invite = r.choice(q.ask_for_playing_madlibs)
        invite += ' ' + '(Type "yes", "yeah", or "play" to begin)'
        return invite

    def __ask_madlibs_question(self, repeat=False):
        '''returns a madlibs question and, if repeat is False,
        increments the madlibs question index'''
        madlib_question = q.madlibs_questions[self.__madlib_qi]
        if not repeat:
            self.__madlib_qi += 1
        return madlib_question

    def __goodbye(self):
        '''Says goodbye to the user'''
        return r.choice(q.goodbye)

    def __ask_question(self):
        '''returns a random question'''
        self.__asked_question = True
        self.__asked_question_i = r.randint(0, len(q.questions) - 1)
        return q.questions[self.__asked_question_i]

    def get_response(self, user_input):
        '''Returns a response to the user's input'''
        if user_input == None:      # if the user didn't enter anything
            return r.choice(self.__default_responses)

        if self.__asked_question:   # if the chatbot has asked a question, reply with the answer
            self.__asked_question = False
            return q.responses[self.__asked_question_i]

        # remove whitespace and convert to lowercase
        user_input = user_input.strip().lower()

        if self.__playing:        # user is playing madlibs
            return self.__play_madlibs(user_input)

        if user_input in self.__greeting_tokens:    # user greets the chatbot
            return self.__greet()

        # user wants to play madlibs
        elif not self.__playing and 'play' in user_input or 'yeah' in user_input or 'yes' in user_input or 'sure' in user_input:
            return self.__play_madlibs(True)

        # user bids farewell
        elif 'goodbye' in user_input or 'bye' in user_input or 'see you later' in user_input:
            return self.__goodbye()

        # ask a question or play madlibs with the user 50% of the time
        if r.random() < 0.5:
            return self.__ask_question()
        else:
            return self.__ask_for_playing_madlibs()

    def __play_madlibs(self, user_input):
        '''Plays madlibs with the user and returns a response'''
        if user_input == True:      # user wants to play madlibs, so start the game
            self.__playing = True
            return 'Let\'s play madlibs (Type "stop playing" to abort)!\n\n' + self.__ask_madlibs_question()

        # user wants to stop playing madlibs
        if user_input == 'stop playing' and self.__playing:
            self.__playing = False
            return 'Okay, goodbye! You don\'t have to play if you don\'t want to.'

        # user has inputted more than one word or has inputted nothing
        if len(user_input.split()) != 1:
            return 'Please enter only one word as I\'m asking for'

        # got a valid response, so add it to the list of responses
        self.__madlibs_responses.append(user_input)
        print("### DEBUG: madlibs_responses = ", self.__madlibs_responses)
        # did we ask all the questions?
        if self.__madlib_qi == len(q.madlibs_questions):
            # yes, generate the madlibs story
            res = 'Here\'s your madlibs story:    ' + \
                q.generate_madlibs(self.__madlibs_responses)
            # and, reset
            self.__reset_madlibs()
            # and, return the story
            return res

        # in middle of game, so ask another question
        return self.__ask_madlibs_question()
