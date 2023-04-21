from django.db.models import CharField


class CustomCharField(CharField):
    def __init__(self, *args, **kwargs) -> None:
        kwargs['max_length'] = 255
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)
