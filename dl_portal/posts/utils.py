# Миксин, заменяющий label_suffix для форм, связанных с моделью
class LabelSuffixMixin:
    def __init__(self, *args, **kwargs):
        if 'label_suffix' not in kwargs:
            kwargs['label_suffix'] = ''
        super(LabelSuffixMixin, self).__init__(*args, **kwargs)
