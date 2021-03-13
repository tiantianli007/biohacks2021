# BioHacks 2021

This is our BCBSU BioHacks 2021 submission. Authors: Tiantian Li, John Liu.

## Introduction

This short guide details how to prepare your environment, gather the necessary data, and run the program on the data.

## Installation

First, start by preparing your environment.
- Anaconda with Python 3.7
- Mayavi, tool for visualization
- wxPython, UI backend for Mayavi

Next, download the datasets tool at https://www.ncbi.nlm.nih.gov/datasets/docs/command-line-start/. We use this free tool to get data from the National Library of Medicine. Extract the tool to the root of this repository and run the following command:
`./datasets download virus genome taxon 2697049 --released-since 03/10/2021 --filename SARS2-all-031021.zip`

 This will download all the SARS-CoV-2 genomes since March 10, 2021. Feel free to change this date. Note that the filesize can be quite large (in the gigabytes!). When finished, extract the ncbi_dataset folder inside the ZIP to the root directory of this repository.

