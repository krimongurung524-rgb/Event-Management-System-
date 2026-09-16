from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("events/", views.event_list, name="event_list"),
    path("events/create/", views.event_create, name="event_create"),
    path("events/<int:pk>/", views.event_detail, name="event_detail"),
    path("events/<int:pk>/update/", views.event_update, name="event_update"),
    path("events/<int:pk>/delete/", views.event_delete, name="event_delete"),

    path("categories/", views.category_list, name="category_list"),
    path("categories/<int:pk>/", views.category_detail, name="category_detail"),

    path("organizers/", views.organizer_list, name="organizer_list"),
    path("organizers/<int:pk>/", views.organizer_detail, name="organizer_detail"),

    path("venues/", views.venue_list, name="venue_list"),
    path("venues/<int:pk>/", views.venue_detail, name="venue_detail"),

    path("tags/", views.tag_list, name="tag_list"),

    path("attendees/", views.attendee_list, name="attendee_list"),
    path("attendees/<int:pk>/", views.attendee_detail, name="attendee_detail"),

    path("reviews/", views.review_list, name="review_list"),

    path("search/", views.search_events, name="search_events"),
    path("advanced-search/", views.advanced_search, name="advanced_search"),

    path("upcoming/", views.upcoming_events, name="upcoming_events"),
    path("past/", views.past_events, name="past_events"),
    path("expensive/", views.expensive_events, name="expensive_events"),

    path("events/category/<int:pk>/", views.events_by_category, name="events_by_category"),
    path("events/organizer/<int:pk>/", views.events_by_organizer, name="events_by_organizer"),

    path("orm-demo/", views.orm_demo, name="orm_demo"),
]