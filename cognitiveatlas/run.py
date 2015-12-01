#!/usr/bin/python

# run.py

# An example of a visualization folder run script that is used to generate the data structures to go
# into the visualizations. This is done so that we can generate the data dynamicaly with any commit/PR
# to see an updated visualization

from cognitiveatlas.api import get_concept, get_task
import json
import os


def main():

    tasks = get_task()

    output_folder = os.path.abspath("data")

    print "Generating Cognitive Atlas Data..."

    # Functions for making nodes
    def make_node(nid,name,color):
        return {"nid":nid,"name":name,"color":color}

    for task in tasks.json:
        if task["name"] != "":
            print "Parsing task %s..." %task["name"]
            task_name = task["name"].replace(" ","_").replace("/","_").lower()
            task_node = make_node(task["id"],task["name"],"#63506d")
            single_task = get_task(id=task["id"]).json[0]
            # We only want to see contrasts with associated concepts
            task_contrasts = single_task["contrasts"]
            task_concepts = []
            for contrast in task_contrasts:
                contrast_node = make_node(contrast["id"],contrast["contrast_text"],"#d89013")
                try:
                    contrast_concepts = get_concept(contrast_id=contrast["id"])
                    children = []
                    for concept in contrast_concepts.json:
                        children.append(make_node(concept["id"],concept["name"],"#3c7263"))
                    contrast_node["children"] = children
                    task_concepts.append(contrast_node)
                except:
                    pass
            task_node["children"] = task_concepts
            # Save to file
            filey = open('%s/%s.json' %(output_folder,task_name),'w')
            filey.write(json.dumps(task_node, sort_keys=True,indent=4, separators=(',', ': ')))
            filey.close()
