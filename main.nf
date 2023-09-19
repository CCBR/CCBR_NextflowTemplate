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
input        : ${params.input}
"""
.stripIndent()

include { FASTQC } from "./modules/local/qc.nf"

workflow qc {
    raw_fastqs = Channel
                .fromPath(params.input)
                .map { file -> tuple(file.simpleName, file) }
    raw_fastqs | FASTQC
}

process yeet {
    container "${params.containers.base}"

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
