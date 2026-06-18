# Spectral Analysis for Geophysical Data Cookbook

<img src="thumbnails/icon.png" alt="thumbnail" width="300"/>

[![nightly-build](https://github.com/ProjectPythia/spectral-analysis-cookbook/actions/workflows/nightly-build.yaml/badge.svg)](https://github.com/ProjectPythia/spectral-analysis-cookbook/actions/workflows/nightly-build.yaml)
[![Binder](https://binder.projectpythia.org/badge_logo.svg)](https://binder.projectpythia.org/v2/gh/ProjectPythia/spectral-analysis-cookbook/main?labpath=notebooks)
[![DOI](https://zenodo.org/badge/475509405.svg)](https://zenodo.org/badge/latestdoi/475509405)

This Project Pythia Cookbook covers ... (replace `...` with the main subject of your cookbook ... e.g., _working with radar data in Python_)

## Motivation

(Add a few sentences stating why this cookbook will be useful. What skills will you, "the chef", gain once you have reached the end of the cookbook?)

## Authors

Juan Diego Mantilla, Sreedevi Puthiyamadam Vasu, Robert R. Ford, Suyue Li, Alex Blackmer, Yiqun Tian, Arman Oliazadeh

### Contributors

<a href="https://github.com/ProjectPythia/spectral-analysis-cookbook/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ProjectPythia/spectral-analysis-cookbook" />
</a>

## Structure

### Data Analysis Methods

(Add content for this section, e.g., "The foundational content includes ... ")

### Data Analysis Applications

(Add content for this section, e.g., "Example workflows include ... ")

## Running the Notebooks

You can either run the notebooks in the Cookbook using [Binder](https://binder.projectpythia.org/) or on your local machine.

### Running on Binder

The simplest way to interact with a Jupyter Notebook is through
[Binder](https://binder.projectpythia.org/), which enables "one click"
execution in the cloud. Simply navigate your mouse to
the top right corner of the book chapter you are viewing and click
on the rocket ship icon (see screenshots [here](https://foundations.projectpythia.org/preamble/how-to-use/#running-pythia-foundations-examples)),
and a text box will appear. Type or paste the Pythia Binder link
(`https://binder.projectpythia.org`) and click "Launch".
After a few moments you should be presented with a
notebook that you can interact with. You’ll be able to execute code
and even change the example programs. At first the code cells
have no output, until you execute them by pressing
{kbd}`Shift`\+{kbd}`Enter`. Complete details on how to interact with
a live Jupyter notebook are described in the Pythia Foundations chapter [Getting Started with
Jupyter](https://foundations.projectpythia.org/foundations/getting-started-jupyter).

Note, not all Cookbook chapters are executable. If you do not see
the rocket ship icon, such as on this page, you are not viewing an
executable book chapter.


### Running on Your Own Machine

If you are interested in running this material locally on your computer, you will need to follow this workflow:

(Replace "cookbook-example" with the title of your cookbooks)

1. Clone the `https://github.com/ProjectPythia/spectral-analysis-coobook` repository:

   ```bash
    git clone https://github.com/ProjectPythia/spectral-analysis-coobook.git
   ```

1. Move into the `spectral-analysis-coobook` directory
   ```bash
   cd spectral-analysis-coobook
   ```
1. Create and activate your conda environment from the `environment.yml` file
   ```bash
   conda env create -f environment.yml
   conda activate spectral-cookbook-dev
   ```
1. Move into the `notebooks` directory and start up Jupyterlab
   ```bash
   cd notebooks/
   jupyter lab
   ```
