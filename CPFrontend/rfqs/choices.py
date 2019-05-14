from common.FrontendTexts import FrontendTexts
view_texts = FrontendTexts('rfqs')

INCOTERMS_CHOICES = (
    (1, "FOB"),
    (2, "CFR"),
    (3, "CIF"),
    (4, "EXW"),
)

labels = view_texts.getComponent()['selector']['choices']

ACTION_CHOICES = (
    (1, labels['edit']),
    (2, labels['reload']),
    (3, labels['basic_analyzer'])
)
