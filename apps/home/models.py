from django.db import models
from django.utils.translation import gettext_lazy as _
from breathline.models import AbstractDateTimeFieldBaseModel



class MainBannerImage(AbstractDateTimeFieldBaseModel):
    banner_image                     = models.FileField(_('Banner Image'), blank=True, null=True, upload_to='main_banner/banner_image')




class MainBreathVideo(AbstractDateTimeFieldBaseModel):
    main_video_url                        = models.URLField(_('Service Video URL'), max_length=1024, null=True, blank=True)
    main_video                            = models.FileField(_('Main Video'),null=True,blank=True, upload_to='main_breath_video/main_video')




class TestimonialVideo(AbstractDateTimeFieldBaseModel):
    testimonial_url                        = models.URLField(_('Testimonial Video URL'), max_length=1024, null=True, blank=True)




