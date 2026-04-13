"""WebSocket consumers for real-time queue updates."""

# from channels.generic.websocket import AsyncJsonWebsocketConsumer
#
# class QueueConsumer(AsyncJsonWebsocketConsumer):
#     async def connect(self):
#         self.department = self.scope['url_route']['kwargs']['department']
#         self.group_name = f'queue_{self.department}'
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)
#
#     async def queue_update(self, event):
#         await self.send_json(event['data'])
