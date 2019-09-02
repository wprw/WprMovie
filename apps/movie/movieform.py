from django import forms


# 评论校验
class CommentForm(forms.Form):
    '''
    校验：请求不为空；不能出现敏感词
    '''
    content = forms.CharField(required=True)

    def clean(self):
        # 从通过第一次校验的数据中获得评论内容进行二次校验
        content = self.cleaned_data.get('content')
        if '垃圾' in content:
            self.add_error('content', '请尊重每一部电影!!')
        return self.cleaned_data
