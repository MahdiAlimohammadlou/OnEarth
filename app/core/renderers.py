from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, (ReturnList, ReturnDict)):
            response_data = {
                'data': data
            }
        else:
            response_data = {
                'data': data,
                'message': data.get('detail', 'Success'),
                'status': renderer_context['response'].status_code
            }
        return super().render(response_data, accepted_media_type, renderer_context)