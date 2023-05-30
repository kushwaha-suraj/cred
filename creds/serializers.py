from rest_framework.serializers import ModelSerializer
from creds.models import Creds


class CredsSerializer(ModelSerializer):
    
    
    class Meta:
        model = Creds
        fields = [ 'id', 'title', 'desc', 'is_complete']