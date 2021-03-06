====================
CAMP Module Template
====================

Overview
--------

The Cookiecutter template for all CAMP (**C**\ ore **A**\ nalysis **M**\ etagenomics **P**\ ipeline) modules. 

Features
--------

* Standardized Snakemake pipelining structure with preset input/output formats for metagenomics sample data
* Integrated Slurm and command-line modes
* Click command line interface for easy parameter management
* Unit-testing with pytest and simulated 2-species sequencing data
* Read the Docs-compatible automated documentation
* Pre-configured version bumping with a single command

Making a New Module
-------------------

These instructions are only for developers that want to create an module for a **new** analysis purpose i.e.: ingests new formats of input or output data. To use or extend existing analysis modules, see TBA. 

Part 1: Setting up the Pipeline Barebones
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Have `conda <https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html>`_ and Cookiecutter (version 1.4.0 or higher) installed in some environment. 

::

	conda install -c conda-forge cookiecutter # or...
	pip install -U cookiecutter

2. Use this template to generate a barebones CAMP analysis module and follow the prompts.

::

	cookiecutter https://github.com/lauren-mak/CAMP_Module_Template.git

3. Set up the module environment.

::

	conda env create -f configs/conda/{{ cookiecutter.module_slug }}.yaml
	conda activate {{ cookiecutter.module_slug }}

Part 2: Writing Pipeline Steps (Rules)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

4. Develop Snakemake rules to wrap your analysis scripts and/or external programs. There is an example (``sample_rule``) and two rule templates in ``Snakefile`` as guidelines. 

5. Customize the ``make_config`` rule in ``Snakefile`` according to intermediate rule output files to make your final output ``samples.csv`` as well as return any other analysis files you might want into the ``final_reports`` directory.

Part 3: Setting up Input/Output and Directory Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

6. Customize the structure of ``configs/samples.csv`` to match your input and output data, and then ``ingest_samples()`` in ``utils.py`` to properly load them. 
	- The example present summarizes Illumina paired-end FastQs and an a set of de novo assembled contigs in a FastA. 

7. Fill out your module's work subdirectory structure in ``utils.py``, specifically ``dirs.OUT``, which is where all of the intermediate and final output files go, and ``dirs.LOG``, which is where all of the logs go. 

8. Add any workflow-specific Python scripts to ``utils.py`` so that they can be called in workflow rules. This keeps the ``Snakefile`` workflow clean. 

9. If applicable, use symlinks in ``utils.py`` between your (original) input data as described in ``samples.csv`` to the temporary directory (``dirs.TMP``) so that they're easy to find and won't be destroyed. 
	- To support relative paths for input files, the symlinking example uses ``abspath()``. However, this will only work if the input files are in **subdirectories** of the current directory. 

Part 4: Setting up Pipeline Configs and Environment Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

10. Customize the amount of memory and CPUs allocated to each rule in the YAMLs under the ``configs/resources`` directory. 

11. Some rules in the pipeline probably use constants for ``shell`` or ``run`` parameters. Add these to ``configs/parameters.yaml`` for easy toggling. 
	- In the future, it will be possible to set specific sets of parameter configurations (i.e.: one of different copies of ``configs/parameters.yaml``) from the command line.

12. If applicable, update the default conda config using ``conda env export > config/conda/{{ cookiecutter.module_slug }}.yaml`` with your tools and their dependencies.
     - If there are dependency conflicts, make a new conda YAML under ``configs/conda`` and specify its usage in specific rules using the ``conda`` option (see ``first_rule`` for an example).

Part 5: Write Documentation and Debug Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

13. Add your module's installation and running instructions to the ``README.rst`` and the module documentation. Then, add the repo to your `Read the Docs account <https://readthedocs.org/>`_ + turn on the Read the Docs service hook.

14. Make the default conda environment, and run the pipeline once through to make sure everything works using the test data in ``test_data/``. Then, generate unit tests to ensure that others can sanity-check their installations.
::
    python /path/to/camp_binning/workflow/binning.py generate_unit_tests \
        -w /path/to/camp_binning/workflow/Snakefile \
        -d /path/to/work/dir \
        -s /path/to/samples.csv

15. If you want your module integrated into the main CAP2/CAMP pipeline, send a pull request and we'll have a look at it ASAP! 
    - Please make it clear what your module intends to do by including a summary in the commit/pull request (ex. "Release X.Y.Z: Module A, which does B to input C and outputs D").

Immediate Tasklist
------------------

* Make a table of existing CAMP modules and their input/output data
* Cleanup of ``dirs.TMP`` directory
