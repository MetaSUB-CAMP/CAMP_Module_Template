.. highlight:: shell

============
Installation
============


Stable release
--------------

1. Clone repo from `github <https://github.com/{{ cookiecutter.github_username }}/camp_{{ cookiecutter.module_slug }}>_`. 

2. Set up the conda environment (contains, Snakemake) using ``configs/conda/camp_{{ cookiecutter.module_slug }}.yaml``. 

3. Make sure the installed pipeline works correctly. ``pytest`` only generates temporary outputs so no files should be created.
::
    cd camp_{{ cookiecutter.module_slug }}
    conda env create -f configs/conda/camp_{{ cookiecutter.module_slug }}.yaml
    conda activate camp_{{ cookiecutter.module_slug }}
    pytest .tests/unit/

