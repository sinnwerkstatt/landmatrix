from django import forms

class CommaSeparatedSelectInteger(forms.MultipleChoiceField):
    pass
    #def to_python(self, value):
    #    if not value:
    #        return ''
    #    elif not isinstance(value, (list, tuple)):
    #        raise ValidationError(
    #            self.error_messages['invalid_list'], code='invalid_list'
    #        )
    #    return ','.join([str(val) for val in value])

    #def validate(self, value):
    #    """
    #    Validates that the input is a string of integers separeted by comma.
    #    """
    #    if self.required and not value:
    #        raise forms.ValidationError(
    #            self.error_messages['required'], code='required'
    #        )
#
    #    # Validate that each value in the value list is in self.choices.
    #    for val in value.split(','):
    #        if not val:
    #            continue
    #        if not self.valid_value(int(val)):
    #            raise forms.ValidationError(
    #                self.error_messages['invalid_choice'],
    #                code='invalid_choice',
    #                params={'value': val},
    #            )

    #def prepare_value(self, value):
    #    """ Convert the string of comma separated integers in list"""
    #    return ','.join(value or [])