from django import forms
from django.utils.safestring import mark_safe


class TagSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = 'widgets/tag_select_multiple.html'

    def __init__(self, *args, tags_color = 'bg-primary', **kwargs):
        super().__init__(*args, **kwargs)
        self.tags_color = tags_color

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['value'] = value or []
        context['widget']['tags_color'] = self.tags_color
        return context

