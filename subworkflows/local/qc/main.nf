include { FASTQC } from "../../../modules/local/fastqc/"

workflow qc {
    take:
        ch_input

    main:
        Channel.fromPath(ch_input)
            | map { file -> tuple(file.simpleName, file) }
            | FASTQC
        ch_fastqc_html = FASTQC.html

    emit:
        fastqc_html = ch_fastqc_html
}
