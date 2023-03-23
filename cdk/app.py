from aws_cdk import core
from chatgpt_irc_stack.chatgpt_irc_stack import ChatgptIrcStack

app = core.App()
ChatgptIrcStack(app, 'ChatgptIrcStack')
app.synth()
