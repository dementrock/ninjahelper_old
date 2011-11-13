from django import template
from django.template import resolve_variable
from django.template.base import NodeList

register = template.Library()

def get_node_list(parser, token, tag_name):
    nodelist_true = parser.parse(('else', 'end' + tag_name))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('end' + tag_name, ))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return nodelist_true, nodelist_false

class IfBased(template.Node):
    child_nodelists = ('nodelist_true', 'nodelist_false')

    def __init__(self, nodelist_true, nodelist_false):
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false

    def __iter__(self):
        for node in self.nodelist_true:
            yield node
        for node in self.nodelist_false:
            yield node

    def render(self, context, cond):
        if cond:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)
            

class IfLoggedIn(IfBased):
    def render(self, context):
        user = resolve_variable('request', context).user
        return super(IfLoggedIn, self).render(context, user.is_authenticated())

@register.tag
def ifloggedin(parser, token):
    nodelist_true, nodelist_false = get_node_list(parser, token, 'ifloggedin')
    return IfLoggedIn(nodelist_true, nodelist_false)
