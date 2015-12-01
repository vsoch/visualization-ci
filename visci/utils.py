'''
utils.py: Part of the visci python package
visualization file structure for continuous integration.

'''
    
from glob import glob
import json
import os
import re

def find_directories(base_dir,fullpath=True):
    '''find_directories
    Return directories at one level specified by user (not recursive)
    :param base_dir: the base directory to start searching from
    '''
    directories = []
    for item in os.listdir(base_dir):
        # Don't include hidden directories
        if not re.match("^[.]",item):
            if os.path.isdir(os.path.join(base_dir, item)):
                if fullpath:
                    directories.append(os.path.abspath(os.path.join(base_dir, item)))
                else:
                    directories.append(item)
    return directories


def find_subdirectories(base_dir):
    '''find_subdirectories
    :param base_dir: the base directory to start searching from
    Return directories (and sub) starting from a base

    '''
    directories = []
    for root, dirnames, filenames in os.walk(base_dir):
        new_directories = ["%s/%s" %(root,d) for d in dirnames if d not in directories]
        directories = directories + new_directories
    return directories


def find_visci(base_dir):
    '''find_visci
    Return visualization directories based on finding visci.json
    :param base_dir: the base directory to start searching from
    '''
    directories = find_subdirectories(base_dir)
    vis_directories = []
    for directory in directories:
        files = [os.path.basename(x) for x in glob("%s/*" %directory)]
        if "visci.json" in files:
            vis_directories.append(directory)
    return vis_directories


def get_validation_fields():
    '''get_validation_fields
    Returns a list of tuples (each a field)

    ..note:: 

          specifies fields required for a valid json
          (field,value,type)
          field: the field name
          value: indicates minimum required entires
                 0: not required, no warning
                 1: required, not valid
                 2: not required, warning      
          type: indicates the variable type

    '''
    return [("name",2,str),
            ("template",1,str),
            ("tag",0,str), 
            ("author",0,str),
            ("publish",0,int)]


def notvalid(reason):
    print reason
    return False

def dowarning(reason):
    print reason


def validate(visci_folder,warning=True):
    '''validate
    :param visci_folder: full path to folder with visci.json
    :param warning: issue a warning for empty fields with level 2 (warning)

    ..note::

        takes an visci folder, and looks for validation based on:
    
        - visci.json
    
    '''
    try:
        meta = load_visci(visci_folder)
        folder_name = os.path.basename(visci_folder)
    except:
        return notvalid("%s: visci.json is not loadable." %(visci_folder))

    fields = get_validation_fields()

    for field,value,ftype in fields:

        # Field must be in the keys
        if field not in meta.keys():
            return notvalid("%s: visci.json is missing field %s" %(folder_name,field))

        # Check if folder should be rendered, period
        if field == "publish":
            if meta[field] == "False":
                return notvalid("%s: visci.json specifies not production ready." %folder_name)

        # Below is for required parameters
        if value == 1:
            if meta[field] == "":
                return notvalid("%s: visci.json must be defined for field %s" %(folder_name,field))
            # Field value must have minimum of value entries
            if not isinstance(meta[field],list):
                tocheck = [meta[field]]
            else:
                tocheck = meta[field]
            if len(tocheck) < value:
                return notvalid("%s: visci.json must have >= %s for field %s" %(folder_name,value,field))
        
        # Below is for warning parameters
        elif value == 2:
            if meta[field] == "":
                if warning == True:
                    dowarning("WARNING: visci.json is missing value for field %s: %s" %(field,folder_name))

        # Template must exist!
        if field == "template":
            if not os.path.exists("%s/%s" %(visci_folder,meta[field])):
                return notvalid("%s: %s is specified in visci.json but missing." %(folder_name,script))
    return True   



def load_visci(visci_folder):
    '''load_visci
    reads in the visci.json for an
    :param visci_folder: full path to folder with visci.json
    '''
    fullpath = os.path.abspath(visci_folder)
    configjson = "%s/visci.json" %(fullpath)
    if not os.path.exists(configjson):
        return notvalid("visci.json could not be found in %s" %(visci_folder))
    try: 
        meta = json.load(open(configjson,"r"))
        meta = remove_unicode_dict(meta[0])
        return meta
    except ValueError as e:
        print "Problem reading visci.json, %s" %(e)
        raise

def remove_unicode_dict(input_dict,encoding="utf-8"):
    '''remove_unicode_dict
    remove unicode keys and values from dict, encoding in utf8
    :param input_dict: input dictionary
    :param encoding: encoding to use, default is utf-8
    '''
    output_dict = dict()
    for key,value in input_dict.iteritems():
        if isinstance(input_dict[key],list):
            output_new = [x.encode(encoding) for x in input_dict[key]]
        elif isinstance(input_dict[key],int):
            output_new = input_dict[key]
        elif isinstance(input_dict[key],float):
            output_new = input_dict[key]
        else:
            output_new = input_dict[key].encode(encoding)
        output_dict[key.encode(encoding)] = output_new
    return output_dict
