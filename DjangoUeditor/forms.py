# coding: utf-8

from django import forms
from widgets import UEditorWidget
from DjangoUeditor.models import UEditorField as ModelUEditorField


class UEditorField(forms.CharField):
    def __init__(self, label, width=600, height=300, toolbars="full", imagePath="", filePath="",
                 upload_settings={}, settings={}, command=None, event_handler=None, *args, **kwargs):

        # 一口气把当前所有的局部参数都读取进来
        uSettings = locals().copy()
        del uSettings["self"], uSettings["label"], uSettings["args"], uSettings["kwargs"]

        # FormFiled获取的widget本来可以是db Field传递过来的，但是这里直接忽视了
        # 对应关系: 直接自己指定 Widget
        # XXX: 完成了参数从FormField到Widget的传递
        kwargs["widget"] = UEditorWidget(attrs=uSettings)
        kwargs["label"] = label
        super(UEditorField, self).__init__(*args, **kwargs)


def update_upload_path(model_form, model_inst=None):
    """ 遍历model字段，如果是UEditorField则需要重新计算路径 """
    if model_inst is not None:
        try:
            for field in model_inst._meta.fields:
                if isinstance(field, ModelUEditorField):
                    # 更新widget中的path
                    model_form.__getitem__(field.name).field.widget.recalc_path(model_inst)
        except:
            pass


class UEditorModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UEditorModelForm, self).__init__(*args, **kwargs)
        # Form存在的意义: 就是为了方便内部的Field的参数能有调整的机会
        try:
            if kwargs.has_key("instance"):
                update_upload_path(self, kwargs["instance"])
            else:
                update_upload_path(self, None)
        except Exception:
            pass
