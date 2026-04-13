include { FASTQC } from "../../../modules/local/fastqc/"

workflow qc {
    take:
        fastq_files

    main:
        channel.fromPath(fastq_files)
            | map { file -> tuple([id: file.simpleName], file) }
            | FASTQC
        ch_fastqc_html = FASTQC.out.html
        ch_fastqc_zip = FASTQC.out.zip

    emit:
        fastqc_html = ch_fastqc_html
        fastqc_zip = ch_fastqc_zip
}
