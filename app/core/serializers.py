from rest_framework import serializers

from .utils import get_current_url
from .models import AboutUsInfo

class BaseSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        if "request" in context:
            self.url = get_current_url(context.get('request', None))
        elif "url" in context:
            self.url = context.get('url', None)
        super().__init__(*args, **kwargs)

    class Meta:
        abstract = True


class AboutUsInfoSerializer(BaseSerializer):

    class Meta:
        model = AboutUsInfo
        fields = [
         "email", "phone_number", "address",
        ]