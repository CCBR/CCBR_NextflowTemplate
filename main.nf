log.info """\
TOOL_NAME
=============
NF version   : $nextflow.version
runName      : $workflow.runName
username     : $workflow.userName
configs      : $workflow.configFiles
profile      : $workflow.profile
cmd line     : $workflow.commandLine
start time   : $workflow.start
projectDir   : $workflow.projectDir
launchDir    : $workflow.launchDir
workDir      : $workflow.workDir
homeDir      : $workflow.homeDir
reads        : ${params.reads}
"""
.stripIndent()

process yeet {
    output:
    stdout

    script:
    """
    echo ${params.input}
    """
}

workflow {
    yeet | view
}
