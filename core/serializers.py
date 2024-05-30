from rest_framework import serializers

class BaseSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        self.url = context.get('url', None)
        super().__init__(*args, **kwargs)

    class Meta:
        abstract = True