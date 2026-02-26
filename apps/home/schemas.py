from rest_framework import serializers
from apps.home.models import MainBannerImage, MainBreathVideo, TestimonialVideo



class GetMainBannerImageAPISchema(serializers.ModelSerializer):

    class Meta:
        model = MainBannerImage
        fields = ['id', 'banner_image']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key in data.keys():
            try:
                if data[key] is None:
                    data[key] = ""
            except KeyError:
                pass
        return data
    

class GetMainBreathVideoAPISchema(serializers.ModelSerializer):
    main_video_url = serializers.SerializerMethodField()

    class Meta:
        model = MainBreathVideo
        fields = ['id', 'main_video_url']

    def get_main_video_url(self, instance):
        request = self.context.get('request')
        if instance.main_video and request:
            return request.build_absolute_uri(instance.main_video.url)
        return instance.main_video_url

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key in data.keys():
            try:
                if data[key] is None:
                    data[key] = ""
            except KeyError:
                pass
        return data


class GetTestimonialVideoAPISchema(serializers.ModelSerializer):

    class Meta:
        model = TestimonialVideo
        fields = ['id', 'testimonial_url']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key in data.keys():
            try:
                if data[key] is None:
                    data[key] = ""
            except KeyError:
                pass
        return data
