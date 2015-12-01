'''
visci.py

Visualization file structure for continuous integration.

'''

from visci.utils import find_visci, validate, load_visci
from visci.template import read_template, get_template, save_render, sub_template
from glob import glob
import os
import imp

base_dir = os.getcwd()

def run():

     # Search for all visci.json to identify a visualization directory
     vis_directories = find_visci(base_dir)

     # Validate vis_directories
     valid_dir = [x for x in vis_directories if validate(x)]

     # Run each to generate output
     index_paths = [generate(x,base_dir) for x in valid_dir]

     # Render paths to indices into a main portal index
     #generate_index(index_paths)


def generate(visci_folder,base_dir):

    # Load the visci folder
    meta = load_visci(visci_folder)

    # If the data directory is missing, make it
    data_output = "%s/data" %visci_folder
    if not os.path.exists(data_output):
        os.mkdir(data_output)

    # If a run script exisits, run it
    run_script = "%s/runX.py" %visci_folder
    if os.path.exists(run_script):     
        module = imp.load_source("main", run_script)
        os.chdir(visci_folder)
        module.main()
        os.chdir(base_dir)

    # generate a visualization for each data
    data_files = glob("%s/*" %(data_output))
    if len(data_files) > 0:
        template_file = "%s/%s" %(visci_folder,meta["template"])
        vis_files = generate_vis(template_file,data_files,visci_folder)

    # Render into the index
    index_path = generate_vis_index(vis_files,base_dir)
    return index_path


def generate_vis(template_file,data_files,output_folder):
    # We will save a list of the output files
    visualization_files = []
    template = read_template(template_file)  
    for data_file in data_files:
        try:
            relative_path = data_file.replace(output_folder,"") 
            if relative_path[0] == "/":
                relative_path = relative_path[1:]  
            filename = os.path.basename(data_file).split(".")[0]
            sub = sub_template(template,{"DATA":relative_path})
            vis_file = "%s/%s.html" %(output_folder,filename)
            save_render(sub,vis_file)
            visualization_files.append(vis_file)
        except:
            print "Error with file %s. Skipping." %(data_file)

    return visualization_files

def generate_vis_index(vis_files,base_dir):
    template = get_template("index")
    # For each vis file, generate link to it
    visci_select = ""
    for vis_file in vis_files:
        relative_path = vis_file.replace(base_dir,"")
        if relative_path[0] == "/":
            relative_path = relative_path[1:]  
        visci_select = '\n%s<option value="%s">%s</option>' %(visci_select,relative_path,relative_path)
    substitutions = {"VISCI_SELECT":visci_select,
                     "VISUALIZATION_ONE":relative_path}
    template = sub_template(template,substitutions)
    save_render(template,"%s/index.html" %base_dir)

def generate_index(index_paths):
    template = get_template("main_index")

