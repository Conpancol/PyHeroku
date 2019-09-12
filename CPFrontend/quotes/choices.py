from common.FrontendTexts import FrontendTexts
view_texts = FrontendTexts('quotes')

labels = view_texts.getComponent()['selector']['choices']

ACTION_CHOICES = (
    (1, labels['edit']),
    (2, labels['edit_materials'])
)

PROVIDER_CHOICES = (
    (1, "MP100001 - Conpancol Ingenieros"),
    (2, "MP100002 - Maasteel UK")
)


