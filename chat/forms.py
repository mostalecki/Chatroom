from django.forms import CharField, ModelForm
from django.core.validators import RegexValidator
from .models import Room

room_name_validator = RegexValidator(r'^[0-9a-zA-Z]*$', "Room name must contain only ASCII alphanumerics.")

class RoomForm(ModelForm):
    name = CharField(max_length=128, validators=[room_name_validator])

    class Meta:
        model = Room
        fields = ['name', 'is_private']