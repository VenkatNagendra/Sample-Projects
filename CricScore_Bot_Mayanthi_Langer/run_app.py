from rasa_core.channels.rest import HttpInputChannel
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_slack_connector import SlackInput

nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/cricscorenlu')
agent = Agent.load('./models/dialouge', interpreter = nlu_interpreter)
input_channel = SlackInput('xoxp-577750409252-577782185266-578870809207-1c1de3b609e8118ba21c5260c9c65a36',
                            'xoxb-577750409252-577795462418-lDbvxAXFr0XElvHDBqUHW4Vd',
                            'CDBHUzVkR4DK0J2bStNXZWvs',
                             True)
agent.handle_channel(HttpInputChannel(5004,'/',input_channel))


