import json 
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # So essentially we have to subscribe an incoming user who connects to a channel of information on the Redis stack.Okay, set of keyword arguments from the sort of url request essentially one of those is come room name. (remember, ChatConsumer is a class, so you are dealing with an instance of that here e.g. one chatter). [self] we need groupo cuz we need to group the chatters by which chatroom they are. Thats why we create these new properties
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # And then we have to subscribe the incoming client, the incoming user to that channel in Redis.
        await self.channel_layer.group_add(
            self.room_group_name,
            # ChatGPT: The self.channel_name is a property of the AsyncWebsocketConsumer class that represents the unique name of the channel for a single WebSocket connection.
            
            # the self.channel_name is passed as an argument to the group_add method of the channel_layer. This method is used to add the current WebSocket connection to a group, identified by self.room_group_name. This allows messages to be sent to all users in the chat room by sending messages to the group, rather than sending messages to each user individually.
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    # essentially send that information to Redis so that other users can see it.
    async def receive(self, text_data):
        # So I'm only saying the JSON object that arrives, the JSON string, we're going to pause it into a Python Dect. And then this is just a Python Dect of the various messages
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # self.send(text_data=json.dumps({'message': message}))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # So it's not enough just to take incoming messages from one client and put them on Redis. We also have to decide what to do with the messages that appear on Redis that didn't come from a specific client.

    # So we'll define this chat message, function, essentially when a new message appears for the channel we're looking at on Redis and we'll pick it up and push it out to every user as well. ChatGPT: The event in async def chat_message(self, event) refers to a message that has been sent to the chat room group. When a message is sent to a group, the channel layer will send the message to all members (all websockets opened/chatters)of the group. For each consumer that is a member of the group, the channel layer will trigger the appropriate event handler.

    #[self] the reason why its event here is cuz this is something that is sent by .channel_layer.group_send
    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))



