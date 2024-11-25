log.info """\
TOOL_NAME $workflow.manifest.version
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
include { BWA_MEM } from './modules/CCBR/bwa/mem'

workflow.onComplete {
    if (!workflow.stubRun && !workflow.commandLine.contains('-preview')) {
        def message = Utils.spooker(workflow)
        if (message) {
            println message
        }
    }
}

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
