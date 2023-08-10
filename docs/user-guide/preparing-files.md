This should describe any input files needed, including config files, manifest files, and sample files. An example is provided below.

# 2. Preparing Files

The pipeline is controlled through editing configuration and manifest files. Defaults are found in the /WORKDIR/config and /WORKDIR/manifest directories, after initialization.

## 2.1 Configs

The configuration files control parameters and software of the pipeline. These files are listed below:

- config/config.yaml
- resources/cluster.yaml
- resources/tools.yaml

### 2.1.1 Cluster Config

The cluster configuration file dictates the resources to be used during submission to Biowulf HPC. There are two different ways to control these parameters - first, to control the default settings, and second, to create or edit individual rules. These parameters should be edited with caution, after significant testing.

### 2.1.2 Tools Config

The tools configuration file dictates the version of each software or program that is being used in the pipeline.

### 2.1.3 Config YAML

There are several groups of parameters that are editable for the user to control the various aspects of the pipeline. These are :

- Folders and Paths
  - These parameters will include the input and output files of the pipeline, as well as list all manifest names.
- User parameters
  - These parameters will control the pipeline features. These include thresholds and whether to perform processes.
- References
  - These parameters will control the location of index files, spike-in references, adaptors and species calling information.

#### 2.1.3.1 User Parameters

##### 2.1.3.1.1 Duplication Status

Users can select duplicated peaks (dedup) or non-deduplicated peaks (no_dedup) through the user parameter.

```
dupstatus: "dedup, no_dedup"
```

##### 2.1.3.1.2 Macs2 additional option

MACS2 can be run with or without the control. adding a control will increase peak specificity
Selecting "Y" for the `macs2_control` will run the paired control sample provided in the sample manifest

#### 2.1.3.2 References

Additional reference files may be added to the pipeline, if other species were to be used.

The absolute file paths which must be included are:

1. fa: "/path/to/species.fa"
2. blacklist: "/path/to/blacklistbed/species.bed"

The following information must be included:

1. regions: "list of regions to be included; IE chr1 chr2 chr3"
2. macs2_g: "macs2 genome shorthand; IE mm IE hs"

## 2.2 Preparing Manifests

There are two manifests, one which required for all pipelines and one that is only required if running a differential analysis. These files describe information on the samples and desired contrasts. The paths of these files are defined in the snakemake_config.yaml file. These files are:

- samplemanifest
- contrasts

### 2.2.1 Samples Manifest (REQUIRED)

This manifest will include information to sample level information. It includes the following column headers:

- sampleName: the sample name WITHOUT replicate number (IE "SAMPLE")
- replicateNumber: the sample replicate number (IE "1")
- isControl: whether the sample should be identified as a control (IE "Y")
- controlName: the name of the control to use for this sample (IE "CONTROL")
- controlReplicateNumber: the replicate number of the control to use for this sample (IE "1")
- path_to_R1: the full path to R1 fastq file (IE "/path/to/sample1.R1.fastq")
- path_to_R2: the full path to R1 fastq file (IE "/path/to/sample2.R2.fastq")

An example sampleManifest file is shown below:

| sampleName                      | replicateNumber | isControl | controlName                     | controlReplicateNumber | path_to_R1                                                        | path_to_R2                                                        |
| ------------------------------- | --------------- | --------- | ------------------------------- | ---------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- |
| 53_H3K4me3                      | 1               | N         | HN6_IgG_rabbit_negative_control | 1                      | PIPELINE_HOME/.test/53_H3K4me3_1.R1.fastq.gz                      | PIPELINE_HOME/.test/53_H3K4me3_1.R2.fastq.gz                      |
| 53_H3K4me3                      | 2               | N         | HN6_IgG_rabbit_negative_control | 1                      | PIPELINE_HOME/.test/53_H3K4me3_2.R1.fastq.gz                      | PIPELINE_HOME/.test/53_H3K4me3_2.R2.fastq.gz                      |
| HN6_H3K4me3                     | 1               | N         | HN6_IgG_rabbit_negative_control | 1                      | PIPELINE_HOME/.test/HN6_H3K4me3_1.R1.fastq.gz                     | PIPELINE_HOME/.test/HN6_H3K4me3_1.R2.fastq.gz                     |
| HN6_H3K4me3                     | 2               | N         | HN6_IgG_rabbit_negative_control | 1                      | PIPELINE_HOME/.test/HN6_H3K4me3_2.R1.fastq.gz                     | PIPELINE_HOME/.test/HN6_H3K4me3_2.R2.fastq.gz                     |
| HN6_IgG_rabbit_negative_control | 1               | Y         | -                               | -                      | PIPELINE_HOME/.test/HN6_IgG_rabbit_negative_control_1.R1.fastq.gz | PIPELINE_HOME/.test/HN6_IgG_rabbit_negative_control_1.R2.fastq.gz |
