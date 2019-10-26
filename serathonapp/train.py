
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot

chatbot = ChatBot('Chatterbot', trainer='chatterbot.trainers.CorpusTrainer',
                  storage_adapter='chatterbot.storage.SQLStorageAdapter',
                  database_uri='sqlite:///database.sqlite3',
                  logic_adapters=[
                      {
                          'import_path': 'chatterbot.logic.BestMatch',
                          'default_response': 'I am sorry, but I do not understand.',
                          'maximum_similarity_threshold': 0.90
                      }
                  ]
                  )

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")
