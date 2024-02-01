import json

from django.core import serializers

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Event


class EventPerformerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "account"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data):

        text_data = text_data.replace('\'', '\\\"')
        print(text_data)
        text_data_json = json.loads(text_data)
        event = text_data_json['event']
        new_performer = text_data_json['performer']
        user = text_data_json['user']
        deserialized_user = self.deserialize_obj(user)
        deserialized_event = self.deserialize_obj(event)
        if new_performer:
            deserialized_performer = self.deserialize_obj(new_performer)
        else:
            deserialized_performer = None

        boolean = await self._change_performer_validation(deserialized_user, deserialized_event)
        if boolean:
            deserialized_event = await self._change_performer(deserialized_event, deserialized_performer)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'change_performer',
                    'performer': new_performer,
                    'event': deserialized_event.toJSON(),
                    'user': user,
                }
            )
        else:
            performer_for_response = deserialized_event.performer
            if (performer_for_response):
                performer_for_response = performer_for_response.toJSON()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'change_performer',
                    'performer': performer_for_response,
                    'event': event,
                    'user': user,
                }
            )

    async def change_performer(self, event):
        _user = event['user']
        _event = event['event']
        _performer = event['performer']
        await self.send(text_data=json.dumps({
            'type': 'change_performer',
            'event': _event,
            'performer': _performer,
            'user': _user,
        }))

    def deserialize_obj(self, obj):
        deserialized_obj = serializers.deserialize('json', obj)
        for obj in deserialized_obj:
            return obj.object

    @sync_to_async
    def _change_performer(self, event: Event, performer):
        db_event = Event.objects.filter(id=event.id).first()
        db_event.performer = performer
        db_event.save()
        return db_event

    @sync_to_async
    def _change_performer_validation(self, deserialized_user, deserialized_event):
        return (deserialized_user.is_staff or deserialized_user.is_superuser) and (not deserialized_event.performer or deserialized_event.performer == deserialized_user)
