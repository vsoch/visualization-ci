'''
template.py: Part of the visci python package
visualization file structure for continuous integration.

'''

import visci.utils
from jinja2 import Template
import string

def read_template(template_file):
    filey = open(template_file,"rb")
    template = "\n".join(filey.readlines())
    template = filter(lambda x: x in string.printable, template)
    filey.close()
    return template.decode("utf-8")


def sub_template(template_str,subs):
    '''sub_template
    Fill in variable substitutions into template, and return a rendered pages
    :param template_str: text str of template, already loaded. Tags should be specified with {{ tag }}.
    :param subs: dict, substitutions, with "key" as variable name, and value as the substitution.
    '''
    template = Template(template_str)
    return template.render(subs)


def save_render(template_str,output_file):
    filey = open(output_file,"w")
    filey.write(template_str)
    filey.close()


def get_template(template_name,extension="html"):
    package_dir = os.path.dirname(visci.utils.__file__)
    template_path = "%s/templates/%s.%s" %(package_dir,template_name,extension)
    return read_template(template_path)
