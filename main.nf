nextflow.enable.dsl = 2

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
    validateParameters()
    yeet | view
}
