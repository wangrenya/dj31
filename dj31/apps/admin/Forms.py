from django import forms
from news.models import Tag ,News
from docs.models import Doc
from courses.models import Course

#后台文章验证
class NewsPubForm(forms.ModelForm):
    """clean"""
    image_url = forms.URLField(label='文章图片URL',error_messages={'required':'文章图片url不能为空'})
    tag = forms.ModelChoiceField(queryset=Tag.objects.only('id').filter(is_delete=False),error_messages={'required':'文章ID不能为空'})

    class Meta:
        model = News
        # 指明字段
        fields = ['title','digest','content','image_url']
        error_messages = {
            'title':{
                'max_length':'文章标题长度不能低于150',
                'min_length':'文章标题长度不能低于1',
                'required':'文章标题不能为空'
            },
            'digest': {
                'max_length': '文章摘要长度不能低于200',
                'min_length': '文章摘要长度不能低于1',
                'required': '文章摘要不能为空'
            },
            'content':{
                'required': '文本内容不能为空'
            },
            'image_url': {
                'required': 'url内容不能为空'
            },
        }
#后台文章验证
class DocsPubForm(forms.ModelForm):
    """
    """
    image_url = forms.URLField(label='文档缩略图url',
                               error_messages={"required": "文档缩略图url不能为空"})

    file_url = forms.URLField(label='文档url',
                               error_messages={"required": "文档url不能为空"})

    class Meta:
        model = Doc  # 与数据库模型关联
        # 需要关联的字段
        # exclude 排除
        fields = ['title', 'desc', 'file_url', 'image_url']
        error_messages = {
            'title': {
                'max_length': "文档标题长度不能超过150",
                'min_length': "文档标题长度大于1",
                'required': '文档标题不能为空',
            },
            'desc': {
                'required': '文档描述不能为空',
            },
        }


class CoursePubForm(forms.ModelForm):
    """
    """
    cover_url = forms.URLField(label='视频缩略图url',
                               error_messages={"required": "视频图片url不能为空"})

    video_url = forms.URLField(label='视频地址url',
                               error_messages={"required": "视频地址url不能为空"})

    class Meta:
        model = Course  # 与数据库模型关联
        # 需要关联的字段
        # exclude 排除
        fields = ['title', 'cover_url', 'video_url', 'outline']
        error_messages = {
            'title': {
                'max_length': "课程标题长度不能超过20",
                'min_length': "课程标题长度大于1",
                'required': '文档标题不能为空',
            },
            'cover_url': {
                'required': '课程描述不能为空',
            },
            'video_url': {
                'required': '课程描述不能为空',
            },
            'outline': {
                'required': '课程描述不能为空',
            },
        }