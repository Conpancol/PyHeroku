from common.FrontendTexts import FrontendTexts
view_texts = FrontendTexts('quotes')

labels = view_texts.getComponent()['selector']['choices']

ACTION_CHOICES = (
    (1, labels['edit']),
    (2, labels['edit_materials'])
)
