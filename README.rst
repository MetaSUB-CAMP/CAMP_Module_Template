====================
CAMP Module Template
====================

Overview
--------

The Cookiecutter template for all CAMP (**C**ore **A**nalysis **M**etagenomics **P**ipeline) modules. 

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

Step 1: Setting up the Pipeline Barebones
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install Cookiecutter (version 1.4.0 or higher).

::
	conda install -c conda-forge cookiecutter # or...
	pip install -U cookiecutter

2. Use this template to generate a barebones CAMP analysis module and follow the prompts.

:: 
	cookiecutter https://github.com/lauren-mak/CAMP_Module_Template.git

Step 2: Writing Pipeline Steps (Rules)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

3. Develop Snakemake rules to wrap your analysis scripts and/or external programs. There is an example (``sample_rule``) and two rule templates in ``Snakefile`` as guidelines. 

4. Customize the ``make_config`` rule in ``Snakefile`` according to intermediate rule output files to make your final output ``samples.csv`` as well as return any other analysis files you might want into the ``final_reports`` directory.

Step 3: Setting up Input/Output and Directory Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

5. Customize the structure of ``configs/samples.csv`` to match your input and output data, and then ``ingest_samples()`` in ``utils.py`` to properly load them. 
	- The example present summarizes Illumina paired-end FastQs and an a set of de novo assembled contigs in a FastA. 

6. Fill out your module's work subdirectory structure in ``utils.py``, specifically ``dirs.OUT``, which is where all of the intermediate and final output files go, and ``dirs.LOG``, which is where all of the logs go. 

7. Add any workflow-specific Python scripts to ``utils.py`` so that they can be called in workflow rules. This keeps the ``Snakefile`` workflow clean. 

8. If applicable, use symlinks in ``utils.py`` between your (original) input data as described in ``samples.csv`` to the temporary directory (``dirs.TMP``) so that they're easy to find and won't be destroyed. 

Step 4: Setting up Pipeline Configs and Environment Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

9. Customize the amount of memory and CPUs allocated to each rule in the YAMLs under the ``configs/resources`` directory. 

10. Some rules in the pipeline probably use constants for ``shell`` or ``run`` parameters. Add these to ``configs/parameters.yaml`` for easy toggling. 
	- In the future, it will be possible to set specific sets of parameter configurations (i.e.: one of different copies of ``configs/parameters.yaml``) from the command line.

11. If applicable, update the default conda config using ``conda env export > config/conda/camp_{{ cookiecutter.module_slug }}.yaml`` with your tools and their dependencies.
     - If there are dependency conflicts, make a new conda YAML under ``configs/conda`` and specify its usage in specific rules using the ``conda`` option (see ``first_rule`` for an example).

Step 5: Write Documentation and Debug Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

12. Add your module's installation and running instructions to the ``README.rst`` and the module documentation. Then, add the repo to your `Read the Docs account <https://readthedocs.org/>`_ + turn on the Read the Docs service hook.

13. Make the default conda environment, and run the pipeline once through to make sure everything works using the test data in ``test_data/``. Then, generate unit tests to ensure that others can sanity-check their installations.
::
    python /path/to/camp_binning/workflow/binning.py generate_unit_tests \
        -w /path/to/camp_binning/workflow/Snakefile \
        -d /path/to/work/dir \
        -s /path/to/samples.csv

14. If you want your module integrated into the main CAP2/CAMP pipeline, send a pull request and we'll have a look at it ASAP! 
    - Please make it clear what your module intends to do by including a summary in the commit/pull request (ex. "Release X.Y.Z: Module A, which does B to input C and outputs D").

Immediate Tasklist
------------------

* Make a table of existing CAMP modules and their input/output data
* Make a user manual-style Read the Docs 

Credits
-------

* This package was created with `Cookiecutter <https://github.com/cookiecutter/cookiecutter>`_ as a simplified version of the `audreyr/cookiecutter-pypackage project template <https://github.com/audreyr/cookiecutter-pypackage>`_.
* Free software: MIT License
* Documentation: TBA
