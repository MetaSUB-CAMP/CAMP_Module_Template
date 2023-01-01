{% set is_open_source = cookiecutter.open_source_license != 'Not open source' -%}

{% for _ in cookiecutter.module_name %}={% endfor %}
============
CAMP {{ cookiecutter.module_name }}
============
{% for _ in cookiecutter.module_name %}={% endfor %}

{% if is_open_source %}
.. image:: https://readthedocs.org/projects/camp-{{ cookiecutter.module_slug }}/badge/?version=latest
        :target: https://camp-{{ cookiecutter.module_slug }}.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status
{%- endif %}

.. image:: https://img.shields.io/badge/version-0.1.0-brightgreen


Overview
--------

This module is designed to function as both a standalone MAG {{ cookiecutter.module_name }} pipeline as well as a component of the larger CAMP metagenome analysis pipeline. As such, it is both self-contained (ex. instructions included for the setup of a versioned environment, etc.), and seamlessly compatible with other CAMP modules (ex. ingests and spawns standardized input/output config files, etc.). 

{{ cookiecutter.module_short_description }}

.. ..

 <!--- 
 Add longer description of your workflow's algorithmic contents 
 --->


Installation
------------

1. Clone repo from `Github <https://github.com/MetaSUB-CAMP/camp_{{ cookiecutter.module_slug }}>`_. 

2. Set up the conda environment using ``configs/conda/{{ cookiecutter.module_slug }}.yaml``. 

3. Update the locations of the test datasets in ``samples.csv``, and the relevant parameters in ``configs/parameters.yaml``.

4. Make sure the installed pipeline works correctly. 
::
    # Create and activate conda environment 
    cd camp_{{ cookiecutter.module_slug }}
    conda create -f configs/conda/{{ cookiecutter.module_slug }}.yaml
    conda activate {{ cookiecutter.module_slug }}
    # Run tests on the included sample dataset
    python /path/to/camp_{{ cookiecutter.module_slug }}/workflow/{{ cookiecutter.module_slug }}.py \
    -d /path/to/camp_{{ cookiecutter.module_slug }}/test_out \
    -s /path/to/camp_{{ cookiecutter.module_slug }}/test_data/samples.csv \
    -p /path/to/camp_{{ cookiecutter.module_slug }}/test_data/parameters.yaml \
    -r /path/to/camp_{{ cookiecutter.module_slug }}/test_data/resources.yaml \
    --cores 20


Using the Module
----------------

**Input**: ``/path/to/samples.csv`` provided by the user.

**Output**: 1) An output config file summarizing 2) the module's outputs. 

- ``/path/to/work/dir/{{ cookiecutter.module_slug }}/final_reports/samples.csv`` for ingestion by the next module (ex. quality-checking)
.. ..

 <!--- 
 Add description of your workflow's output files 
 --->

**Structure**:
::
    └── workflow
        ├── Snakefile
        ├── {{ cookiecutter.module_slug }}.py
        ├── utils.py
        └── __init__.py
* ``workflow/{{ cookiecutter.module_slug }}.py``: Click-based CLI that wraps the ``snakemake`` and other commands for clean management of parameters, resources, and environment variables.
* ``workflow/Snakefile``: The ``snakemake`` pipeline. 
* ``workflow/utils.py``: Sample ingestion and work directory setup functions, and other utility functions used in the pipeline and the CLI.

1. Make your own ``samples.csv`` based on the template in ``configs/samples.csv``. Sample test data can be found in ``test_data/``. 
    - ``ingest_samples`` in ``workflow/utils.py`` expects Illumina reads in FastQ (may be gzipped) form and de novo assembled contigs in FastA form
    - ``samples.csv`` requires either absolute paths or paths relative to the directory that the module is being run in

2. Update the relevant parameters in ``configs/parameters.yaml``.

3. Update the computational resources available to the pipeline in ``resources.yaml``. 

4. To run CAMP on the command line, use the following, where ``/path/to/work/dir`` is replaced with the absolute path of your chosen working directory, and ``/path/to/samples.csv`` is replaced with your copy of ``samples.csv``. 
    - The default number of cores available to Snakemake is 1 which is enough for test data, but should probably be adjusted to 10+ for a real dataset.
    - Relative or absolute paths to the Snakefile and/or the working directory (if you're running elsewhere) are accepted!
::

    python /path/to/camp_{{ cookiecutter.module_slug }}/workflow/{{ cookiecutter.module_slug }}.py \
        (-c max_number_of_local_cpu_cores) \
        -d /path/to/work/dir \
        -s /path/to/samples.csv
* Note: This setup allows the main Snakefile to live outside of the work directory.

5. To run CAMP on a job submission cluster (for now, only Slurm is supported), use the following.
    - ``--slurm`` is an optional flag that submits all rules in the Snakemake pipeline as ``sbatch`` jobs. 
    - In Slurm mode, the ``-c`` flag refers to the maximum number of ``sbatch`` jobs submitted in parallel, **not** the pool of cores available to run the jobs. Each job will request the number of cores specified by threads in ``configs/resources/slurm.yaml``.
::

    sbatch -J jobname -o jobname.log << "EOF"
    #!/bin/bash
    python /path/to/camp_{{ cookiecutter.module_slug }}/workflow/{{ cookiecutter.module_slug }}.py --slurm \
        (-c max_number_of_parallel_jobs_submitted) \
        -d /path/to/work/dir \
        -s /path/to/samples.csv
    EOF

6. After checking over ``final_reports/`` and making sure you have everything you need, you can delete all intermediate files to save space. 
::

    python /path/to/camp_{{ cookiecutter.module_slug }}/workflow/{{ cookiecutter.module_slug }}.py cleanup \
        -d /path/to/work/dir \
        -s /path/to/samples.csv

7. If for some reason the module keeps failing, CAMP can print a script containing all of the remaining commands that can be run manually. 
::

    python /path/to/camp_{{ cookiecutter.module_slug }}/workflow/{{ cookiecutter.module_slug }}.py --dry_run \
        -d /path/to/work/dir \
        -s /path/to/samples.csv > cmds.txt
    python /path/to/camp_{{ cookiecutter.module_slug }}/workflow/{{ cookiecutter.module_slug }}.py commands cmds.txt

Updating the Module
--------------------

What if you've customized some components of the module, but you still want to update the rest of the module with latest version of the standard CAMP? Just do the following from within the module's home directory:
    - The flag with the setting ``-X ours`` forces conflicting hunks to be auto-resolved cleanly by favoring the local (i.e.: your) version.
::
    cd /path/to/camp_{{ cookiecutter.module_slug }}
    git pull -X ours


Extending the Module
--------------------

We love to see it! This module was partially envisioned as a dependable, prepackaged sandbox for developers to test their shiny new tools in. 

These instructions are meant for developers who have made a tool and want to integrate or demo its functionality as part of the standard {{ cookiecutter.module_name }} workflow, or developers who want to integrate an existing tool. 

1. Write a module rule that wraps your tool and integrates its input and output into the pipeline. 
    - This is a great `Snakemake tutorial <https://bluegenes.github.io/hpc-snakemake-tips/>`_ for writing basic Snakemake rules.
    - If you're adding new tools from an existing YAML, use ``conda env update --file configs/conda/existing.yaml --prune``.
    - If you're using external scripts and resource files that i) cannot easily be integrated into either `utils.py` or `parameters.yaml`, and ii) are not as large as databases that would justify an externally stored download, add them to ``workflow/ext/`` or ``workflow/ext/scripts/`` and use ``rule external_rule`` as a template to wrap them. 
2. Update the ``make_config`` in ``workflow/Snakefile`` rule to check for your tool's output files. Update ``samples.csv`` to document its output if downstream modules/tools are meant to ingest it. 
    - If you plan to integrate multiple tools into the module that serve the same purpose but with different input or output requirements (ex. for alignment, Minimap2 for Nanopore reads vs. Bowtie2 for Illumina reads), you can toggle between these different 'streams' by setting the final files expected by ``make_config`` using the example function ``workflow_mode``.
    - Update the description of the ``samples.csv`` input fields in the CLI script ``workflow/{{ cookiecutter.module_slug }}.py``. 
3. If applicable, update the default conda config using ``conda env export > config/conda/{{ cookiecutter.module_slug }}.yaml`` with your tool and its dependencies. 
    - If there are dependency conflicts, make a new conda YAML under ``configs/conda`` and specify its usage in specific rules using the ``conda`` option (see ``first_rule`` for an example).
4. Add your tool's installation and running instructions to the module documentation and (if applicable) add the repo to your `Read the Docs account <https://readthedocs.org/>`_ + turn on the Read the Docs service hook.
5. Run the pipeline once through to make sure everything works using the test data in ``test_data/`` if appropriate, or your own appropriately-sized test data. 
    * Note: Python functions imported from ``utils.py`` into ``Snakefile`` should be debugged on the command-line first before being added to a rule because Snakemake doesn't port standard output/error well when using ``run:``.

6. Increment the version number of the modular pipeline.
::

    bump2version --allow-dirty --commit --tag major workflow/__init__.py \
                 --current-version A.C.E --new-version B.D.F

7. If you want your tool integrated into the main CAMP pipeline, send a pull request and we'll have a look at it ASAP! 
    - Please make it clear what your tool intends to do by including a summary in the commit/pull request (ex. "Release X.Y.Z: Integration of tool A, which does B to C and outputs D").

.. ..

 <!--- 
 Bugs
 ----
 Put known ongoing problems here
 --->

Credits
-------

{% if is_open_source %} 
* This package was created with `Cookiecutter <https://github.com/cookiecutter/cookiecutter>`_ as a simplified version of the `project template <https://github.com/audreyr/cookiecutter-pypackage>`_.
* Free software: {{ cookiecutter.open_source_license }} License
* Documentation: https://{{ cookiecutter.module_slug | replace("_", "-") }}.readthedocs.io. 
{% endif %}


