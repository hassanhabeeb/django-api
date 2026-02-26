from rest_framework import serializers
from apps.home.models import MainBannerImage, MainBreathVideo, TestimonialVideo
from breathline.helpers.helper import base64_file_extension, base64_to_file, get_object_or_none, get_token_user_or_none
import uuid


def base64withextension(file):
    extension = base64_file_extension(file)
    converted_file = base64_to_file(file)
    return f'{uuid.uuid4()}.{extension}', converted_file


class CreateOrUpdateMainBannerImageSerializer(serializers.ModelSerializer):
    id                              = serializers.IntegerField(required=False, allow_null=True)
    banner_image                    = serializers.CharField(allow_null=True, allow_blank=True, required=False)

    class Meta:
        model = MainBannerImage
        fields = ['id', 'banner_image']

    def validate(self, attrs):
        max_size = 1 * 1024 * 1024
        if attrs.get('banner_image'):
            _, file = base64withextension(attrs.get('banner_image'))
            if file.size > max_size:
                raise serializers.ValidationError({"banner_image": "Image size must be less than 1 MB."})
        return super().validate(attrs)

    def create(self, validated_data):
        request       = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        instance                     = MainBannerImage()

        if validated_data.get('banner_image'):
            filename, file = base64withextension(validated_data.get('banner_image'))
            instance.banner_image.save(filename, file, save=False)

        instance.created_by             = user_instance
        instance.modified_by            = user_instance
        instance.save()

        return instance

    def update(self, instance, validated_data):
        request       = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        if validated_data.get('banner_image'):
            filename, file = base64withextension(validated_data.get('banner_image'))
            instance.banner_image.save(filename, file, save=False)

        instance.modified_by            = user_instance
        instance.save()

        return instance
    


class DeleteMainBannerImageSerializer(serializers.ModelSerializer):
    id = serializers.ListField(child=serializers.IntegerField(),required=True)

    class Meta:
        model  = MainBannerImage
        fields = ['id'] 
    


class CreateOrUpdateMainBreathVideoSerializer(serializers.ModelSerializer): 
    id                              = serializers.IntegerField(required=False, allow_null=True)
    main_video_url                  = serializers.URLField(required=False, allow_null=True)
    main_video                      = serializers.CharField(allow_null=True, allow_blank=True, required=False)

    class Meta:
        model = MainBreathVideo
        fields = ['id', 'main_video_url', 'main_video']

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        request       = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        main_video_url = validated_data.get('main_video_url', None)
        main_video     = validated_data.get('main_video', None)

        instance                     = MainBreathVideo()
        # instance.main_video_url      = validated_data.get('main_video_url', None)

        if main_video_url:
            instance.main_video_url = main_video_url
        else:
            filename, file = base64withextension(main_video)
            instance.main_video.save(filename, file, save=False)
            instance.main_video_url = instance.main_video


        instance.created_by             = user_instance
        instance.modified_by            = user_instance
        instance.save()

        return instance

    def update(self, instance, validated_data):
        request       = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        main_video_url = validated_data.get('main_video_url', None)
        main_video     = validated_data.get('main_video', None)

        if main_video_url:
            instance.main_video_url = main_video_url
            instance.main_video = ""
        else:
            filename, file = base64withextension(main_video)
            print(filename)
            print(file)
            instance.main_video.save(filename, file, save=False)
            instance.main_video_url = instance.main_video

        instance.modified_by            = user_instance
        instance.save()

        return instance
    


class DeleteMainBreathVideoSerializer(serializers.ModelSerializer):
    id = serializers.ListField(child=serializers.IntegerField(),required=True)

    class Meta:
        model  = MainBreathVideo
        fields = ['id'] 
    


class CreateOrUpdateTestimonialVideoSerializer(serializers.ModelSerializer): 
    id                              = serializers.IntegerField(required=False, allow_null=True)
    testimonial_url                 = serializers.URLField(required=False, allow_null=True)

    class Meta:
        model = TestimonialVideo
        fields = ['id', 'testimonial_url']

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        request       = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        instance                     = TestimonialVideo()
        instance.testimonial_url     = validated_data.get('testimonial_url', None)

        instance.created_by             = user_instance
        instance.modified_by            = user_instance
        instance.save()

        return instance

    def update(self, instance, validated_data):
        request       = self.context.get('request', None)
        user_instance = get_token_user_or_none(request)

        instance.testimonial_url     = validated_data.get('testimonial_url', instance.testimonial_url)

        instance.modified_by            = user_instance
        instance.save()

        return instance
    


class DeleteTestimonialVideoSerializer(serializers.ModelSerializer):
    id = serializers.ListField(child=serializers.IntegerField(),required=True)

    class Meta:
        model  = TestimonialVideo
        fields = ['id'] 