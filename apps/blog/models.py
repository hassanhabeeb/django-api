from django.db import models
from django.utils.translation import gettext_lazy as _
from breathline.models import AbstractDateTimeFieldBaseModel
from django.utils.text import slugify
from random import randint



class Blog(AbstractDateTimeFieldBaseModel):
    title                         = models.CharField(_('Title'), max_length=250, null=True, blank=True)
    sub_title                     = models.CharField(_('Sub Title'), max_length=250, null=True, blank=True)
    slug                          = models.SlugField(_('Slug'),  max_length=250, editable=False,db_index=True, null=True, blank=True)
    description                   = models.TextField(_('Description'), null=True, blank=True)
    author                        = models.CharField(_('Author'), max_length=250, null=True, blank=True)
    blog_image                    = models.FileField(_('Blog Image'), null=True, blank=True, upload_to='blog/blog_image')

    meta_title                    = models.CharField(_('Meta Title'), max_length=250, null=True, blank=True)
    meta_image_title              = models.CharField(_('Meta Image Title'), max_length=250, null=True, blank=True)
    meta_description              = models.TextField(_('Meta Description'), null=True, blank=True)
    meta_keywords                 = models.TextField(_('Meta Keywords'), null=True, blank=True)
    og_image                      = models.FileField(_('Og Image'), null=True, blank=True, upload_to='blog/og_image')

    def save(self, *args, **kwargs):
        if not self.slug or self.title:
            self.slug = slugify(str(self.title))
            if Blog.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.title)) + '-' + str(randint(1, 9999999))
        super(Blog, self).save(*args, **kwargs)                       
        

    def __str__(self):
        return self.title if self.title else ""
    



class Service(AbstractDateTimeFieldBaseModel):

    class Service_Category(models.TextChoices):
        Sleep_Apnea            = "sleep_apnea"
        ADHD_Treatment         = "adhd_treatment"
        Anxiety_And_Depression = "anxiety_and_depression"
        UARS_Treatment         = "uars_treatment"

    service_category              = models.CharField(_('Service Category'), choices=Service_Category.choices, max_length=250, null=True, blank=True)
    service_video_url             = models.URLField(_('Service Video URL'), max_length=1024, null=True, blank=True)


    def __str__(self):
        return self.service_category if self.service_category else ""
    


class PatientStories(AbstractDateTimeFieldBaseModel):
    name                          = models.CharField(_('Name'), max_length=250, null=True, blank=True)
    rating                        = models.CharField(_('Rating'), max_length=250, null=True, blank=True)
    description                   = models.TextField(_('Description'), null=True, blank=True)


    def __str__(self):
        return self.name if self.name else ""
    

class Gallery(AbstractDateTimeFieldBaseModel):
    image                    = models.FileField(_('Image'), null=True, blank=True, upload_to='gallery/image')
    


class Award(AbstractDateTimeFieldBaseModel):
    award_image                    = models.FileField(_('Award Image'), null=True, blank=True, upload_to='award/award_image')


    

class Event(AbstractDateTimeFieldBaseModel):
    event_image                   = models.FileField(_('Event Image'), null=True, blank=True, upload_to='event/event_image')
    description                   = models.TextField(_('Description'), null=True, blank=True)




class Subscription(AbstractDateTimeFieldBaseModel):
    email                         = models.EmailField(_('email'), max_length = 255, blank = True, null = True)
    is_subscribe                  = models.BooleanField(_('Is Subscribe'), blank=True, null=True, default=True)




class Communication(AbstractDateTimeFieldBaseModel):

    class Service_Category(models.TextChoices):
        Sleep_Apnea            = "sleep_apnea"
        ADHD_Treatment         = "adhd_treatment"
        Anxiety_And_Depression = "anxiety_and_depression"
        UARS_Treatment         = "uars_treatment"


    name                                = models.CharField(_('Name'), max_length=255, blank = True, null = True)
    email                               = models.EmailField(_('Email'), max_length = 255, blank = True, null = True)
    phonenumber                         = models.CharField(_('Phone Number'),max_length=15,null=True,blank=True)
    service_category                    = models.CharField(_('Service Category'), choices=Service_Category.choices, max_length=250, null=True, blank=True)
    message                             = models.TextField(_('Message'), null=True, blank=True)

    class Meta:
        verbose_name          = "Communication"
        verbose_name_plural   = "communication"