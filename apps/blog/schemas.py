from rest_framework import serializers
from apps.blog.models import Award, Blog, Event, Gallery, PatientStories, Service



class GetBlogListAPISchema(serializers.ModelSerializer):
    created_date              = serializers.DateTimeField(format="%b %d, %Y") 

    class Meta:
        model = Blog
        fields = ['id', 'title', 'sub_title', 'slug', 'description', 'author', 'blog_image', 'created_date', 'meta_title', 'meta_image_title', 'meta_description', 'meta_keywords', 'og_image']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key in data.keys():
            try:
                if data[key] is None:
                    data[key] = ""
            except KeyError:
                pass
        return data
    


class GetServiceListAPISchema(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ['id', 'service_category', 'service_video_url']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key in data.keys():
            try:
                if data[key] is None:
                    data[key] = ""
            except KeyError:
                pass
        return data



class GetPatientStoriesListAPISchema(serializers.ModelSerializer):

    class Meta:
        model = PatientStories
        fields = ['id', 'name', 'rating', 'description']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key in data.keys():
            try:
                if data[key] is None:
                    data[key] = ""
            except KeyError:
                pass
        return data
    

"""Gallery"""
class GetGalleryListAPISchema(serializers.ModelSerializer):

    class Meta:
        model = Gallery
        fields = ['id', 'image']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key in data.keys():
            try:
                if data[key] is None:
                    data[key] = ""
            except KeyError:
                pass
        return data
    

class GetAwardListAPISchema(serializers.ModelSerializer):

    class Meta:
        model = Award
        fields = ['id', 'award_image']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key in data.keys():
            try:
                if data[key] is None:
                    data[key] = ""
            except KeyError:
                pass
        return data



class GetEventListAPISchema(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['id', 'event_image', 'description']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key in data.keys():
            try:
                if data[key] is None:
                    data[key] = ""
            except KeyError:
                pass
        return data