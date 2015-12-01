## Visualization with Continuous Integration (VISCI)

[![Circle CI](https://circleci.com/gh/vsoch/visualization-ci/tree/master.svg?style=svg)](https://circleci.com/gh/vsoch/visualization-ci/tree/master)

A lot of research happens on Github, but visualization to go along with these pipelines is not a "solved problem." Data changes. We may want to visualize this data, but we don't have a server. We may also want to test different ways of visualizing the same data, but that's annoying to do locally and over many data inputs. Thus, this is what I am calling Visualization-CI - a standard of running visualizations to go along with continuous integration. 


### How does it work?
Setting up `visci` integration into your repo should be as simple as dropping configuration files into one or more folders of your repo, and adding a line to your circle.yml (or other continuous integration script). The visualizations should be produced as artifacts each time a PR or commit is triggered. `visci` can produce the same visualization for many data inputs, or different visualizations for the same data input, for one or more folders anywhere in your repo.

Visci is also agnostic to the formats of your inputs, and your visualizations. The only requirement is that your template is a web-based thing (.html, ipython notebook will be supported soon), and that a single input data file is specified in your template (to be read in as a file) using the {{data}} tag.


#### File Structure

The structure of a visualization-ci repo could be as follows:

    setup.py
    visci
        data.py
        analysis.py
    cognitiveatlas
        template.html
        visci.json
        run.py
        data
           input_file1.json
           input_file2.json
           input_file3.json

1. Right now the package itself is included and installed with the repo, and this would be changed to install with pip by specifying in the requirements.txt, and then triggering the visualization build in circle.yml.

2. Each visualization to be done is contained within some folder of your analysis, for example, `cognitiveatlas`. These folders are identified based on the presence of a configuration file called `visci.json.` The minimum requirement beyond this file is a template, (for example `template.html`) that is specified in the configuration file. The two optional files are `run.py` and the folder `data`. The high level idea is that data in this folder will be piped into the template to produce one visualization per data file. This means you have several choices for generating this data:

- You can include the data folder in the repo. This could be a good use if you want to dynamically alter the template.html, and produce different visualizations for the same data.
- You can generate the data in some fashion from your analysis, and output to this directory.
- In the case that you don't even have a visualization pipeline, you can generate the files with a script called `run.py` that will be run if it exists. The requirement for this script is that your main analysis falls under a function called main().

3. Within each visualization folder, you are free to include subfolders and dependencies (eg, other javascript or flat files) to be linked from your output. You can assume that your visualizations defined in `template.html` will be relative to this file. 


### Before Continuous Integration is Run

The repo might look like this

    circle.yml
    cognitiveatlas
        template.html
        visci.json
        run.py
    requirements.txt

### After Continuous Integration is Run

    circle.yml
    cognitiveatlas
        visci.json
        index.html
        template.html
        run.py
        data
             input_file1.json
             input_file2.json
             input_file3.json
    index.html
    requirements.txt

You will notice only two changes - the presence of `index.html` files in the base directory, and each subdirectory. The upper level index.html acts as a portal into each of the lower level visualizations, and the lower level serves to navigate over the different data objects.

### visci.json

The visci.json specifies the variables that we've already talked about. The reason for this file is that as this integration is developed, we can do things like give the user more options for customization, or generate multiple visualizations for one folder. 


### Reproducibility
The underlying purpose of a standard like this is reproducibility. The larger idea is that we must have tools that are flexible enough to be easily extended to different data or method.  This means that I can generate an analysis pipeline, and you can run your data through it simply by cloning my repo, changing the input data, and doing a PR. You could also take my data, and edit the method (in this case, it's a visualization template) to see how the result varies. This particular implementation is for visualziation, and deployment with continuous integration, but you should see that a general framework like this would work equivalently in some other computational environment. You might also intuit that 

- A researcher 

If we can add steps along 


### Notes
 - can we have email notifications when it finishes with links to result?
 - pushing content back to gh-pages? Would require authentication, likely one step too much.
 - Circle.ci will "time out" if there is no output >10 minutes (something to keep in mind)
