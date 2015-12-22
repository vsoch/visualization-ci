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

    # Cognitive Atlas tasks we are interested in from NeuroVault tags
    task_uids = ['trm_553e77e53497d','trm_4f2457a8b0bc8', 'trm_553ebfc390256', 'trm_553e88a66b676', 'trm_553fd2fc7a648', 'trm_4ebd482eba5b1', 'trm_4ebc98cc77e7b', 'trm_4ebc728326a13', 'trm_4ebc6a6b75ebf', 'trm_4ebc9d2e397f2', 'trm_553fce5d21da7', 'trm_553fcbbe974ba', 'trm_4da890594742a', 'trm_4d559bcd67c18', 'trm_4cacee4a1d875', 'trm_4c898c0786246', 'trm_4ebd47b8bab6b', 'tsk_4a57abb949a4f', 'trm_4f2456027809f', 'trm_553e73e29cf7d', 'trm_4c8a834779883', 'trm_4cacf22a22d80', 'trm_4e8dd3831f0cc', 'trm_53c4465b0466f', 'trm_553fbbf79ebc5', 'trm_5542841f3dcd5', 'trm_5346938eed092', 'trm_534692ef3b5df', 'trm_534690b0e9dc5', 'trm_5346927710e88', 'trm_4f244ad7dcde7', 'trm_551b1460e89a3', 'trm_553e6b8e33da4', 'trm_553e85265f51e', 'tsk_4a57abb949bf6', 'trm_4f24179122380', 'tsk_4a57abb949e1a', 'trm_4cacf3fbc503b', 'trm_5181f83b77fa4', 'trm_5181f863d24f4', 'trm_553eb45e2b709', 'trm_550b5b066d37b', 'trm_550b50095d4a3', 'trm_550b53d7dd674', 'trm_550b5c1a7f4db', 'trm_550b54a8b30f4', 'trm_550b557e5f90e', 'trm_550b5a47aa23e', 'trm_553eb28436233', 'trm_50df0dd9d0b6f', 'trm_553fc858cacc5','trm_553ec64e6cb1b']

    # Functions for making nodes
    def make_node(nid,name,color):
        return {"nid":nid,"name":name,"color":color}

    for task in tasks.json:
        if task["name"] != "":
            print "Parsing task %s..." %task["name"]
            task_name = task["name"].replace(" ","_").replace("/","_").lower()
            if task["id"] in task_uids:
                task_node = make_node(task["id"],task["name"],"#63506d")
                single_task = get_task(id=task["id"]).json[0]
                # We only want to see contrasts with associated concepts
                task_contrasts = single_task["contrasts"]
                task_concepts = []
                for contrast in task_contrasts:
                    try:
                        contrast_node = make_node(contrast["id"],contrast["contrast_text"],"#d89013")
                        contrast_concepts = get_concept(contrast_id=contrast["id"])
                        children = []
                        for concept in contrast_concepts.json:
                            children.append(make_node(concept["id"],concept["name"],"#3c7263"))
                        contrast_node["children"] = children
                        # Only append contrast if it has children
                        if len(children) > 0:
                            task_concepts.append(contrast_node)
                    except:
                        pass
                task_node["children"] = task_concepts
                # Save to file if we have children
                if len(task_concepts) > 0:
                    filey = open('%s/%s.json' %(output_folder,task_name),'w')
                    filey.write(json.dumps(task_node, sort_keys=True,indent=4, separators=(',', ': ')))
                    filey.close()
