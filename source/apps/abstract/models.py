import datetime

from django.db import models


# Use **BLANK instead of null=True, blank=True
BLANK = {'blank': True, 'null': True}


class CommonModel(models.Model):
    """ This is an abstract model which will be inherited by nearly all models.
    When the object is created it will get a date_created timestamp and each
    time it is modified it will recieve a date_modified time stamp as well.
    """
    date_created = models.DateTimeField("Date Created", auto_now_add=True)
    date_modified = models.DateTimeField("Date Modified", auto_now=True,
            editable=False)

    class Meta:
        abstract = True


class StatusManager(models.Manager):
    """ This adds a query method to pull all published records. """
    def published(self):
        today = datetime.date.today()

        return super(StatusManager, self).get_query_set().filter(
                status='P', pub_date__lte=today,
            ).filter(
                models.Q(expire_date__gt=today) | \
                models.Q(expire_date__isnull=True)
            )


class StatusModel(CommonModel):
    """ This abstract model has the same properties as the Common Model, but it
    allows for statuses to be applied to the object.
    """
    STATUS_OPTIONS = (('D', 'Draft'), ('P', 'Published'), ('H', 'Hidden'))

    status = models.CharField("Status", max_length=1,
            choices=STATUS_OPTIONS, default='P')
    expire_date = models.DateField("Expiration Date", **BLANK)
    pub_date = models.DateField("Published Date", default=datetime.date.today,
        help_text="Date to be published")

    objects = StatusManager()

    class Meta:
        abstract = True

    def is_published(self):
        """ This returns True if the object is published, and False otherwise.
        """
        today = datetime.date.today()
        return self.status == 'P' and self.pub_date <= today and \
            (self.expire_date is None or self.expire_date > today)
