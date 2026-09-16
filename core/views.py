from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, F, Count, Avg, Sum
from django.utils import timezone

from .models import (
    Category,
    Venue,
    Organizer,
    Tag,
    Event,
    Attendee,
    Review,
)


# =========================================================
# 1. HOME
# =========================================================

def home(request):
    events = Event.objects.all().order_by("-start_datetime")[:6]

    return render(request, "core/home.html", {
        "events": events
    })


# =========================================================
# 2. DASHBOARD
# =========================================================

def dashboard(request):
    context = {
        "total_events": Event.objects.count(),
        "total_categories": Category.objects.count(),
        "total_venues": Venue.objects.count(),
        "total_organizers": Organizer.objects.count(),
        "total_attendees": Attendee.objects.count(),
        "total_reviews": Review.objects.count(),
    }

    return render(request, "core/dashboard.html", context)


# =========================================================
# 3. EVENT LIST
# =========================================================

def event_list(request):
    events = Event.objects.all().order_by("start_datetime")

    return render(request, "core/event_list.html", {
        "events": events
    })


# =========================================================
# 4. EVENT DETAIL
# =========================================================

def event_detail(request, pk):
    event = get_object_or_404(
        Event.objects.select_related(
            "category",
            "organizer"
        ).prefetch_related("tags"),
        pk=pk
    )

    return render(request, "core/event_detail.html", {
        "event": event
    })


# =========================================================
# 5. CREATE EVENT
# =========================================================

def event_create(request):
    

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        start_datetime = request.POST.get("start_datetime")
        end_datetime = request.POST.get("end_datetime")
        price = request.POST.get("price") or 0
        total_seats = request.POST.get("total_seats") or 0
        status = request.POST.get("status") or "upcoming"
        image = request.FILES.get("image")

        category_id = request.POST.get("category")
        organizer_id = request.POST.get("organizer")

        category = get_object_or_404(Category, id=category_id)
        organizer = get_object_or_404(Organizer, id=organizer_id)

        event = Event.objects.create(
            title=title,
            description=description,
            slug=title.lower().replace(" ", "-"),
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            price=price,
            total_seats=total_seats,
            status=status,
            image=image,
            category=category,
            organizer=organizer,
        )

        selected_tags = request.POST.getlist("tags")

        if selected_tags:
            event.tags.set(selected_tags)

        return redirect("event_detail", pk=event.pk)
    
    categories = Category.objects.all()
    organizers = Organizer.objects.all()
    tags = Tag.objects.all()
    
    return render(request, "core/event_create.html", {
        "categories": categories,
        "organizers": organizers,
        "tags": tags,
    })


# =========================================================
# 6. UPDATE EVENT
# =========================================================

def event_update(request, pk):

    event = get_object_or_404(
        Event,
        pk=pk
    )

    categories = Category.objects.all()
    organizers = Organizer.objects.all()
    venues = Venue.objects.all()
    tags = Tag.objects.all()

    if request.method == "POST":

        event.title = request.POST.get("title")
        event.description = request.POST.get("description")

        event.start_datetime = request.POST.get(
            "start_datetime"
        )

        event.end_datetime = request.POST.get(
            "end_datetime"
        )

        event.price = request.POST.get("price")

        event.total_seats = request.POST.get(
            "total_seats"
        )

        event.status = request.POST.get("status")

        category_id = request.POST.get("category")
        organizer_id = request.POST.get("organizer")
        venue_id = request.POST.get("venue")

        event.category = get_object_or_404(
            Category,
            id=category_id
        )

        event.organizer = get_object_or_404(
            Organizer,
            id=organizer_id
        )

        event.venue = get_object_or_404(
            Venue,
            id=venue_id
        )

        # Update image only if a new image is uploaded
        if request.FILES.get("image"):
            event.image = request.FILES.get("image")

        event.save()

        # Update Many-to-Many tags
        selected_tags = request.POST.getlist("tags")

        event.tags.set(selected_tags)

        return redirect(
            "event_detail",
            pk=event.pk
        )

    context = {
        "event": event,
        "categories": categories,
        "organizers": organizers,
        "venues": venues,
        "tags": tags,
    }

    return render(
        request,
        "core/event_update.html",
        context
    )


# =========================================================
# 7. DELETE EVENT
# =========================================================

def event_delete(request, pk):

    event = get_object_or_404(
        Event,
        pk=pk
    )

    if request.method == "POST":

        event.delete()

        return redirect(
            "event_list"
        )

    return render(
        request,
        "core/event_delete.html",
        {
            "event": event
        }
    )


# =========================================================
# 8. CATEGORY LIST
# =========================================================

def category_list(request):

    categories = Category.objects.all()

    return render(
        request,
        "core/category_list.html",
        {
            "categories": categories
        }
    )


# =========================================================
# 9. CATEGORY DETAIL
# =========================================================

def category_detail(request, pk):

    category = get_object_or_404(
        Category,
        pk=pk
    )

    events = Event.objects.filter(
        category=category
    ).order_by("start_datetime")

    return render(
        request,
        "core/category_detail.html",
        {
            "category": category,
            "events": events
        }
    )


# =========================================================
# 10. ORGANIZER LIST
# =========================================================

def organizer_list(request):

    organizers = Organizer.objects.all()

    return render(
        request,
        "core/organizer_list.html",
        {
            "organizers": organizers
        }
    )


# =========================================================
# 11. ORGANIZER DETAIL
# =========================================================

def organizer_detail(request, pk):

    organizer = get_object_or_404(
        Organizer,
        pk=pk
    )

    events = Event.objects.filter(
        organizer=organizer
    ).order_by("start_datetime")

    return render(
        request,
        "core/organizer_detail.html",
        {
            "organizer": organizer,
            "events": events
        }
    )


# =========================================================
# 12. VENUE LIST
# =========================================================

def venue_list(request):

    venues = Venue.objects.all()

    return render(
        request,
        "core/venue_list.html",
        {
            "venues": venues
        }
    )


# =========================================================
# 13. VENUE DETAIL
# =========================================================

def venue_detail(request, pk):

    venue = get_object_or_404(
        Venue,
        pk=pk
    )

    events = Event.objects.filter(
        venue=venue
    ).order_by("start_datetime")

    return render(
        request,
        "core/venue_detail.html",
        {
            "venue": venue,
            "events": events
        }
    )


# =========================================================
# 14. TAG LIST
# =========================================================

def tag_list(request):

    tags = Tag.objects.all()

    return render(
        request,
        "core/tag_list.html",
        {
            "tags": tags
        }
    )


# =========================================================
# 15. ATTENDEE LIST
# =========================================================

def attendee_list(request):

    attendees = Attendee.objects.select_related(
        "event"
    ).all()

    return render(
        request,
        "core/attendee_list.html",
        {
            "attendees": attendees
        }
    )


# =========================================================
# 16. ATTENDEE DETAIL
# =========================================================

def attendee_detail(request, pk):

    attendee = get_object_or_404(
        Attendee.objects.select_related("event"),
        pk=pk
    )

    return render(
        request,
        "core/attendee_detail.html",
        {
            "attendee": attendee
        }
    )


# =========================================================
# 17. REVIEW LIST
# =========================================================

def review_list(request):

    reviews = Review.objects.select_related(
        "event"
    ).all()

    return render(
        request,
        "core/review_list.html",
        {
            "reviews": reviews
        }
    )


# =========================================================
# 18. SEARCH EVENTS
# =========================================================

def search_events(request):

    query = request.GET.get(
        "q",
        ""
    )

    events = Event.objects.all()

    if query:

        events = Event.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    return render(
        request,
        "core/search.html",
        {
            "events": events,
            "query": query
        }
    )


# =========================================================
# 19. ADVANCED SEARCH
# =========================================================

def advanced_search(request):

    search_type = request.GET.get(
        "type",
        ""
    )

    value = request.GET.get(
        "value",
        ""
    )

    events = Event.objects.all()

    if value:

        if search_type == "exact":

            events = Event.objects.filter(
                title__exact=value
            )

        elif search_type == "contains":

            events = Event.objects.filter(
                title__contains=value
            )

        elif search_type == "icontains":

            events = Event.objects.filter(
                title__icontains=value
            )

        elif search_type == "startswith":

            events = Event.objects.filter(
                title__startswith=value
            )

        elif search_type == "istartswith":

            events = Event.objects.filter(
                title__istartswith=value
            )

        elif search_type == "endswith":

            events = Event.objects.filter(
                title__endswith=value
            )

        elif search_type == "iendswith":

            events = Event.objects.filter(
                title__iendswith=value
            )

        elif search_type == "regex":

            events = Event.objects.filter(
                title__regex=value
            )

        elif search_type == "iregex":

            events = Event.objects.filter(
                title__iregex=value
            )

    return render(
        request,
        "core/advanced_search.html",
        {
            "events": events,
            "search_type": search_type,
            "value": value
        }
    )


# =========================================================
# 20. UPCOMING EVENTS
# =========================================================

def upcoming_events(request):

    events = Event.objects.filter(
        start_datetime__gte=timezone.now()
    ).order_by("start_datetime")

    return render(
        request,
        "core/upcoming_events.html",
        {
            "events": events
        }
    )


# =========================================================
# 21. PAST EVENTS
# =========================================================

def past_events(request):

    events = Event.objects.filter(
        start_datetime__lt=timezone.now()
    ).order_by("-start_datetime")

    return render(
        request,
        "core/past_events.html",
        {
            "events": events
        }
    )


# =========================================================
# 22. EXPENSIVE EVENTS
# =========================================================

def expensive_events(request):

    events = Event.objects.filter(
        price__gt=1000
    ).order_by("-price")

    return render(
        request,
        "core/expensive_events.html",
        {
            "events": events
        }
    )


# =========================================================
# 23. EVENTS BY CATEGORY
# =========================================================

def events_by_category(request, pk):

    category = get_object_or_404(
        Category,
        pk=pk
    )

    events = Event.objects.filter(
        category=category
    ).prefetch_related(
        "tags"
    ).order_by("start_datetime")

    return render(
        request,
        "core/events_by_category.html",
        {
            "category": category,
            "events": events
        }
    )


# =========================================================
# 24. EVENTS BY ORGANIZER
# =========================================================

def events_by_organizer(request, pk):

    organizer = get_object_or_404(
        Organizer,
        pk=pk
    )

    events = Event.objects.filter(
        organizer=organizer
    ).select_related(
        "category",
        "venue"
    ).order_by("start_datetime")

    return render(
        request,
        "core/events_by_organizer.html",
        {
            "organizer": organizer,
            "events": events
        }
    )


# =========================================================
# 25. ORM DEMO
# =========================================================

def orm_demo(request):

    # EXACT
    exact_events = Event.objects.filter(
        title__exact="Music Festival"
    )

    # CONTAINS
    contains_events = Event.objects.filter(
        title__contains="Fest"
    )

    # ICONTAINS
    icontains_events = Event.objects.filter(
        title__icontains="fest"
    )

    # STARTS WITH
    startswith_events = Event.objects.filter(
        title__startswith="Music"
    )

    # ISTARTS WITH
    istartswith_events = Event.objects.filter(
        title__istartswith="music"
    )

    # ENDS WITH
    endswith_events = Event.objects.filter(
        title__endswith="Festival"
    )

    # IENDS WITH
    iendswith_events = Event.objects.filter(
        title__iendswith="festival"
    )

    # GREATER THAN
    gt_events = Event.objects.filter(
        price__gt=1000
    )

    # GREATER THAN OR EQUAL
    gte_events = Event.objects.filter(
        price__gte=1000
    )

    # LESS THAN
    lt_events = Event.objects.filter(
        price__lt=5000
    )

    # LESS THAN OR EQUAL
    lte_events = Event.objects.filter(
        price__lte=5000
    )

    # RANGE
    range_events = Event.objects.filter(
        price__range=(1000, 5000)
    )

    # IN
    in_events = Event.objects.filter(
        category_id__in=[1, 2, 3]
    )

    # IS NULL
    isnull_events = Event.objects.filter(
        image__isnull=False
    )

    # REGEX
    regex_events = Event.objects.filter(
        title__regex=r"^[A-Z]"
    )

    # IREGEX
    iregex_events = Event.objects.filter(
        title__iregex=r"festival"
    )

    # Q OBJECT
    q_events = Event.objects.filter(
        Q(title__icontains="music") |
        Q(description__icontains="music")
    )

    # F OBJECT
    # Compare price with total_seats
    f_events = Event.objects.filter(
        price__gt=F("total_seats")
    )

    # AGGREGATION
    statistics = Event.objects.aggregate(
        total_events=Count("id"),
        average_price=Avg("price"),
        total_price=Sum("price"),
    )

    # ANNOTATION
    category_event_count = Category.objects.annotate(
        total_events=Count("event")
    )

    # SELECT RELATED
    related_events = Event.objects.select_related(
        "category",
        "organizer",
        "venue"
    )

    # PREFETCH RELATED
    prefetched_events = Event.objects.prefetch_related(
        "tags",
        "attendees",
        "reviews"
    )

    context = {

        "exact_events": exact_events,

        "contains_events": contains_events,

        "icontains_events": icontains_events,

        "startswith_events": startswith_events,

        "istartswith_events": istartswith_events,

        "endswith_events": endswith_events,

        "iendswith_events": iendswith_events,

        "gt_events": gt_events,

        "gte_events": gte_events,

        "lt_events": lt_events,

        "lte_events": lte_events,

        "range_events": range_events,

        "in_events": in_events,

        "isnull_events": isnull_events,

        "regex_events": regex_events,

        "iregex_events": iregex_events,

        "q_events": q_events,

        "f_events": f_events,

        "statistics": statistics,

        "category_event_count": category_event_count,

        "related_events": related_events,

        "prefetched_events": prefetched_events,
    }

    return render(
        request,
        "core/orm_demo.html",
        context
    )