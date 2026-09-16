from django.contrib import admin
from .models import (
    Category,
    Venue,
    Organizer,
    Tag,
    Event,
    Attendee,
    Review,
)


admin.site.register(Category)
admin.site.register(Venue)
admin.site.register(Organizer)
admin.site.register(Tag)
admin.site.register(Event)
admin.site.register(Attendee)
admin.site.register(Review)