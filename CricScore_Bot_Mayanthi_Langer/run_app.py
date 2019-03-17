from rasa_core.channels.rest import HttpInputChannel
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_slack_connector import SlackInput

nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/cricscorenlu')
agent = Agent.load('./models/dialouge', interpreter = nlu_interpreter)
input_channel = SlackInput('OAuth Access Token',
                            'Bot User OAuth Access Token',
                            'Verification Token',
                             True)
agent.handle_channel(HttpInputChannel(5004,'/',input_channel))


