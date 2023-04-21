from django.db.models import CharField


class OptionalCharField(CharField):
    def __init__(self, *args, **kwargs) -> None:
        kwargs['max_length'] = 255
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)
