from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new chat bot instance
bot = ChatBot('Chatbot')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(bot)

# Train the chatbot on the English corpus
trainer.train('chatterbot.corpus.english')

# Function to get a response from the chatbot
def get_response(user_input):
    response = bot.get_response(user_input)
    return str(response)
