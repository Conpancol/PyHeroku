from common.FrontendTexts import FrontendTexts

view_texts = FrontendTexts('materials')
labels = view_texts.getComponent()['selector']['choices']

ACTION_CHOICES = (
    (1, labels['edit']),
    (2, labels['weight'])
)

UNIT_CHOICES = (
    (1, "M"),
    (2, "M2"),
    (3, "M3"),
    (4, "EA")
)
