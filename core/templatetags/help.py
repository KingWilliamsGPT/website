import builtins as _builtins
import pprint as _pprint
import importlib

from django import template
from django.utils.html import escape
from django.urls import reverse_lazy, reverse

register = template.Library()

NEW_LINE = "\n"

def _isvalidtag(tag):
    return True # come back to this


@register.filter
def dir(value, arg="pre"):
    tag = str(arg)
    if arg and _isvalidtag(tag):
        code_f = '<{tag}>{txt}</{tag}>'
    else:
        return _builtins.dir(value)
    try:
        return code_f.format(tag=tag, txt=escape(_pprint.pformat(_builtins.dir(value))))
    except Exception as e:
        return "Error in formatting: %s: %s" % (e.__class__.__name__, e)


@register.filter
def stat(value, arg=False):
    # details about an object *arg* represents presence of privates attributes
    types = {}
    show_privates = arg
    for i in _builtins.dir(value):
        name, _type = i, getattr(value, i).__class__.__name__
        if not show_privates and i.startswith('_'):
            continue
        types.setdefault(_type, [])
        types[_type].append(name)
    buffer = ["Documentation on <b>" + escape(repr(value)) + '</b>', "--No doc" or getattr(value, '__doc__')]
    append = buffer.append
    append("-- Objects")
    append(_pprint.pformat(types))
    return '<pre>' + NEW_LINE.join(buffer) + '</pre>'


@register.filter(name="type")
def gettype(value, arg=None):
    return type(value)



# tagsclass 

from django.template.defaulttags import Node


class LoadURLS(Node):
    def render(self, context):
        import churchel.request_context.siteconfig as siteconfig
        links = siteconfig.site_info(context['request'])['site_links']
        for link in links:
            try:
                new_link = reverse(link)
                # print('reverse of', link, 'is', new_link)
                link_name = link.split(':')[-1] + '_link' # second param after the colon core:index
                context[link_name] = new_link
            except Exception: #NoReverseMatch
                pass
            
        return ""


@register.tag
def set_links(parser, token):
    return LoadURLS()
    