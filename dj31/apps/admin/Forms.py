from django import forms
from news.models import Tag ,News

#后台文章验证
class NewsPubForm(forms.ModelForm):
    """clean"""
    image_url = forms.URLField(label='文章图片URL',error_messages={'required':'文章图片url不能为空'})
    tag = forms.ModelChoiceField(queryset=Tag.objects.only('id').filter(is_delete=False),error_messages={'required':'文章ID不能为空'})

    class Meta:
        model = News
        # 指明字段
        fields = ['title','digest','content']
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
        }