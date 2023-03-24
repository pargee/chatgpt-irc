import irc.bot
import irc.strings
import openai
import configparser
import os

class ChatGPTBot(irc.bot.SingleServerIRCBot):
    def __init__(self, config):
        server = config['IRC']['server']
        port = int(config['IRC']['port'])
        channel = config['IRC']['channel']
        nickname = config['IRC']['nickname']
        password = config['IRC']['password']

        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, nickname)
        self.channel = channel
        self.nickname = nickname

        # Set up OpenAI API key
        openai.api_key = config['OpenAI']['api_key']

    def on_ready(self, connection, event):
        connection.join(self.channel)
        print(f"Joined channel {self.channel}")

    def on_pubmsg(self, connection, event):
        # Check if the bot is mentioned in the message
        if event.arguments[0].startswith(self.connection.get_nickname()):
            user_input = event.arguments[0].replace(self.connection.get_nickname(), "").strip()
            response = self.get_chatgpt_response(user_input)
            response_chunks = split_response(response)
            for chunk in response_chunks:
                connection.privmsg(self.channel, f"{event.source.nick}: {chunk}")

    def get_chatgpt_response(self, message):
        prompt = f"{self.nickname}: {message}"
        conversation = [
            {"role": "system", "content": "You are chatting with an AI assistant."},
            {"role": "user", "content": prompt}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.8,
        )
        return response.choices[0].message['content'].strip()


    def on_nicknameinuse(self, connection, event):
        connection.nick(connection.get_nickname() + "_")

    def on_welcome(self, connection, event):
        self.on_ready(connection, event)
    
def split_response(response, max_length=450):
    response = response.replace('\r', '')  # Remove carriage return characters
    words = response.split(' ')
    chunks = []

    current_chunk = ''
    for word in words:
        if len(current_chunk) + len(word) + 1 > max_length:
            chunks.append(current_chunk.strip())
            current_chunk = ''

        current_chunk += f' {word}'

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    bot = ChatGPTBot(config)
    bot.start()
