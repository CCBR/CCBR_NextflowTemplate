name: Bug report
description: Report something that is broken or incorrect
labels: bug
body:
  - type: markdown
    attributes:
      value: |
        Before you post this issue, please check the documentation:

        - [pipeline documentation: troubleshooting](https://ccbr.github.io/CCBR_NextflowTemplate/troubleshooting/) # TODO replace CCBR_NextflowTemplate in this link with TOOL_NAME

  - type: textarea
    id: description
    attributes:
      label: Description of the bug
      description: A clear and concise description of what the bug is.
    validations:
      required: true

  - type: textarea
    id: command_used
    attributes:
      label: Command used and terminal output
      description: Steps to reproduce the behaviour. Please paste the command you used to launch the pipeline and the output from your terminal.
      render: console
      placeholder: |
        $ nextflow run ...

        Some output where something broke

  - type: textarea
    id: files
    attributes:
      label: Relevant files
      description: |
        Please drag and drop any relevant files here. Create a `.zip` archive if the extension is not allowed.
        Your verbose log file `.nextflow.log` is often useful _(this is a hidden file in the directory where you launched the pipeline)_ as well as custom Nextflow configuration files.
        If the bug is related to a GUI, add screenshots to help explain your problem.

  - type: textarea
    id: system
    attributes:
      label: System information
      description: |
        * Nextflow version _(eg. 21.10.3)_
        * Hardware _(eg. HPC, Desktop)_
        * Executor _(eg. slurm, local, awsbatch)_
        * Container engine: _(e.g. Docker, Singularity)_
        * OS _(eg. Ubuntu Linux, macOS)_
        * Version of CCBR/TOOL_NAME _(eg. 1.0, 1.8.2)_
