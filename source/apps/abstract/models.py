import datetime

from django.db import models


# Shortcut for empty model fields
EMPTY = {'blank': True, 'null': True}

# Set up the statuses so they're globally accessible
HIDDEN = 'H'
DRAFT = 'D'
PUBLISHED = 'P'

STATUSES = (
    ('HIDDEN', HIDDEN),
    ('DRAFT', DRAFT),
    ('PUBLISHED', PUBLISHED),
)


class CommonModel(models.Model):
    """ This is an abstract model which will be inherited by nearly all models.
    When the object is created it will get a date_created timestamp and each
    time it is modified it will recieve a date_modified time stamp as well.
    """

    date_created = models.DateTimeField("Date Created", auto_now_add=True)
    date_modified = models.DateTimeField("Date Modified", **EMPTY)


    class Meta:
        abstract = True


    def save(self, *args, **kwargs):
        self.date_modified = self.update_date_modified()
        super(CommonModel, self).save(*args, **kwargs)


    @property
    def meta_name(self):
        return self._meta.object_name


    def update_date_modified(self):
        """ Override this to change how date_modified works. """
        return datetime.datettime.now()


class StatusManager(models.Manager):
    """ This adds a query method to pull all published records. """

    def status(self, value):
        return super(StatusManager, self).get_query_set().filter(status=value)


    def published(self):
        today = datetime.date.today()

        query = self.status(PUBLISHED).filter(pub_date__lte=today)
        query = query.filter(models.Q(exp_date__gt=today) |
                             models.Q(exp_date__isnull=True))

        return query


class StatusModel(CommonModel):
    """ This abstract model has the same properties as the Common Model, but it
    allows for statuses to be applied to the object.
    """

    status = models.CharField("Status", max_length=1,
                              choices=STATUSES, default=PUBLISHED)
    exp_date = models.DateField("Expiration Date", **EMPTY)
    pub_date = models.DateField("Published Date", default=datetime.date.today,
                                help_text="Date to be published")

    objects = StatusManager()


    class Meta:
        abstract = True


    @property
    def published(self):
        today = datetime.date.today()

        return (
            self.status == PUBLISHED and
            self.pub_date <= today and

            # Not expired
            (self.exp_date is None or
             self.exp_date > today)
        )
