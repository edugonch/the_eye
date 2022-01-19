from rest_framework import serializers
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import re

def baseHostValidator(key, object):
    if key in object.keys():
        validate_url = URLValidator()
        try:
            validate_url(object[key])
        except ValidationError:
            message = f"{key} is not in the correct format {object[key]}."
            raise serializers.ValidationError(message)            
    else:
        message = f"Missing {key} keyworkd on payload {object}."
        raise serializers.ValidationError(message)

def basePathValidator(key, object):
    if key in object.keys():
        if not re.match(r"^(\/).?(.*)?\/?(.)*", object[key]):
            message = f"{key} is not in the correct format {object[key]}"
            raise serializers.ValidationError(message)
    else:
        message = f"Missing {key} keyworkd on payload {object}"
        raise serializers.ValidationError(message)

class PageViewEventValidator:
    requires_context = True

    def __call__(self, value, validator):
        baseHostValidator("host", value)
        basePathValidator("path", value)

class CtaClickEventValidator:
    requires_context = True

    def __call__(self, value, validator):
        baseHostValidator("host", value)
        basePathValidator("path", value)
        if not 'element' in value.keys():
            message = f"Missing element keyworkd on payload {value}"
            raise serializers.ValidationError(message)

class FormInteractionEventValidator:
    requires_context = True

    def __call__(self, value, validator):
        baseHostValidator("host", value)
        basePathValidator("path", value)
        if 'form' in value.keys():
            if not isinstance(value["form"], dict):
                message = f"Form is not in the correct format {value['form']}"
                raise serializers.ValidationError(message)
        else:
            message = f"Missing element keyworkd on payload {value}"
            raise serializers.ValidationError(message)