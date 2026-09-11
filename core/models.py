from django.db import models


# Abstract base model
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


# 1) Category — simple model
class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# 2) Organizer — OneToOne with Venue (1 to 1)
class Venue(BaseModel):
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    capacity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='venues/', blank=True, null=True)

    def __str__(self):
        return self.name


class Organizer(BaseModel):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    bio = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    # OneToOne — euta organizer = euta matra venue
    venue = models.OneToOneField(
        Venue,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='organizer'
    )

    def __str__(self):
        return self.name


# 3) Tag — ManyToMany ko lagi
class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# 4) Event — main model
# ForeignKey to Category (1 to many)
# ManyToMany to Tag
class Event(BaseModel):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='events/')          # compulsory image
    start_datetime = models.DateTimeField()                  # compulsory datetime
    end_datetime = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    total_seats = models.IntegerField(default=0)

    # ForeignKey — 1 category = many events (1 to many)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='events'
    )

    # ForeignKey — 1 organizer = many events (1 to many)
    organizer = models.ForeignKey(
        Organizer,
        on_delete=models.CASCADE,
        related_name='events'
    )

    # ManyToMany — 1 event = many tags, 1 tag = many events
    tags = models.ManyToManyField(
        Tag,
        related_name='events',
        blank=True
    )

    def __str__(self):
        return self.title


# 5) Attendee — ForeignKey to Event (1 to many)
class Attendee(BaseModel):
    TICKET_CHOICES = [
        ('vip', 'VIP'),
        ('general', 'General'),
        ('student', 'Student'),
    ]

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    ticket_type = models.CharField(max_length=20, choices=TICKET_CHOICES, default='general')
    slug = models.SlugField(unique=True)
    # ForeignKey — 1 event = many attendees
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='attendees'
    )

    def __str__(self):
        return f"{self.full_name} - {self.event.title}"


# 6) Review — ForeignKey to Event
class Review(BaseModel):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    reviewer_name = models.CharField(max_length=200)
    comment = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    def __str__(self):
        return f"{self.reviewer_name} - {self.event.title}"
