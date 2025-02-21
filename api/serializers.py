from rest_framework.serializers import ModelSerializer, SerializerMethodField

from news.models import NewsPost


class NewsPostSerializer(ModelSerializer):

    channel_name  = SerializerMethodField()
    newspost_link = SerializerMethodField()


    class Meta:
        model  = NewsPost
        fields = [
            'header',
            'channel_name',
            'newspost_link',
        ]

    def get_channel_name(self, obj):
        return obj.channel.name

    ## TODO Maybe rework it all to Django Model Properties?
    def get_newspost_link(self, obj):
        if obj.channel and obj.channel.social:
            return obj.channel.social.tag_template.format(channel_tag = obj.channel.tag, post_id = str(obj.post_id))
        return None
