nextflow.enable.dsl = 2

// Modules
include { FASTQC } from "./modules/local/qc.nf"
include { BWA_MEM } from './modules/CCBR/bwa/mem'

// Plugins
include { validateParameters; paramsSummaryLog } from 'plugin/nf-schema'


workflow.onComplete {
    if (!workflow.stubRun && !workflow.commandLine.contains('-preview')) {
        def message = Utils.spooker(workflow)
        if (message) {
            println message
        }
    }
}

workflow version {
    println "TOOL_NAME ${workflow.manifest.version}"
}

workflow LOG {
    log.info """\
            TOOL_NAME $workflow.manifest.version
            =============
            cmd line     : $workflow.commandLine
            start time   : $workflow.start
            launchDir    : $workflow.launchDir
            input        : ${params.input}
            genome       : ${params.genome}
            """
            .stripIndent()
    log.info paramsSummaryLog(workflow)
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
    LOG()
    yeet | view
}
