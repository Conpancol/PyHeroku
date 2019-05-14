from common.FrontendTexts import FrontendTexts
view_texts = FrontendTexts('providers')

category_labels = view_texts.getComponent()['creator']['choices']
action_labels = view_texts.getComponent()['selector']['choices']

CATEGORY_CHOICES = (
    (1, category_labels['materials']),
    (2, category_labels['transporters']),
)

ACTION_CHOICES = (
    (1, action_labels['edit']),
    (2, action_labels['comment']),
)

# ... country list extracted from file

