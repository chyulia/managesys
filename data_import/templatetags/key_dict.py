#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template

register = template.Library()

def key_dict(d, key_name):
    try:
        value = d[key_name]
    except KeyError:
        from django.conf import settings

        value = settings.TEMPLATE_STRING_IF_INVALID

    return value
key = register.filter('key_dict', key_dict)