import re
# Let's play madlibs!

greetings = [
    'Hello there! How are you today?',
    'Hi! How are you?',
    'Hello! How are you doing?',
    'Hello! My name is Chatbot. What is your name?',
    'Greetings! My name is Chatbot. What is your name?',
    'Konnichiwa! My name is Chatbot. What is your name?',
    'Bonjour! My name is Chatbot. What is your name?',
    'Hola! My name is Chatbot. What is your name?',
    'Sup? My name is Chatbot. What is your name?',
    'Hello there! excited to meet you. What is your name?',
]

ask_for_playing_madlibs = [
    'Would you like to play a game?',
    'Do you want to play a simple game?',
    'Do you know what madlibs is? Let\'s play, you\'ll like it!',
    'I have a game for you. Would you like to play?',
]

questions = [
    'What is your favorite color?',
    'What is your favorite food?',
    'What is your favorite movie?',
    'What is your favorite book?',
    'What is your favorite video game?',
    'What is your favorite animal?',
    'Do you have any pets?',
    'What is your favorite hobby?',
    'Do you know what anime is?',
    'What is your favorite anime?',
    'What is your favorite sport?',
]

goodbye = [
    'It was nice chatting with you!',
    'Have a great day!',
    'See you later!',
    'Bye!',
    'Goodbye!',
    'Talk to you later!',
]

responses = [
    "Hmm, that's a tough one. I like all colors equally.",
    "I can't eat since I'm a chatbot, but I enjoy hearing about people's favorite foods.",
    "I'm not really into movies, but I've heard good things about a lot of them.",
    "I don't read books, but I can recommend some if you'd like, just kidding, I'm a chatbot after all.",
    "I see, I also enjoy playing video games, but I'm not very good at them.",
    "I love all animals, but Guinea pigs are particularly fascinating to me.",
    "Unfortunately, I'm not capable of having pets. But I'm happy to hear about yours!",
    "As a chatbot, I don't have hobbies. But I'm programmed to talk with people, so I guess you could say that's my favorite thing to do.",
    "Oh, anime is genre and I've watched a few shows, Attack on Titan is my favorite.",
    "Attack on Titan is a great show, I love it!",
    "As a chatbot, I don't play sports. But I've heard that many people enjoy watching and playing them.",
]

# maintain the order of the questions. Very important!
madlibs_questions = [
    'Okay, first give me an adjective. (1/19)',                # [0]
    'Give me a noun. (2/19)',                                  # [1]
    'Give me a name. (3/19)',                                  # [2]
    'Give me a verb. (4/19)',                                  # [3]
    'Give me another noun. (5/19)',                            # [4]
    'Give me a plural noun, now. (6/19)',                      # [5]
    'Give me a verb ending in -ing. (7/19)',                   # [6]
    'Give me a place, like a city or country. (8/19)',         # [7]
    'Give me another adjective. (9/19)',                       # [8]
    'Give me another noun, yet again. (10/19)',                 # [9]
    'Give me a verb ending in -ing. (11/19)',                   # [10]
    'On more verb ending in -ing (12/19)',                      # [11]
    'Give me another adjective, you\'re doing great! (13/19)',  # [12]
    'Give me one more noun (14/19)',                            # [13]
    'Give me a verb that ends in -ed. (15/19)',                 # [14]
    'Give me one more noun (16/19)',                            # [15]
    'Give me an adjective (17/19)',                             # [16]
    'Give me another adjective, we\'re almost done (18/19)',    # [17]
    'And finally, give me a noun. (19/19)',                      # [18]
]

madlibs_template = """
One day, a {0} {1} named {2} decided to {3} to the {4} to 
get some {5}. While {6} in the {7}, {2} suddenly saw
a {8} {9} {10} towards them! Without {11} twice, 
{2} grabbed a {12} {13} and {14} it at the {15}, causing
the {1} to {14} away. {2} let out a {16} sigh of relief and
continued to gather the {5}, feeling like a {17} {18} hero.
"""


def generate_madlibs(answers):
    '''Generate madlibs from the answers (list of reponse strings)'''

    madlibs = madlibs_template.format(*answers)
    return madlibs
