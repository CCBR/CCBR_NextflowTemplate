
process FASTQC {
    tag { sample_id }

    container "${params.containers.base}"

    input:
        tuple val(sample_id), path(fastq)
    output:
        tuple val(sample_id), path("${sample_id}*.html"), emit: html
        tuple val(sample_id), path("${sample_id}*.zip"),  emit: zip

    script:
    """
    fastqc \
        $fastq \
        -t $task.cpus \
        -o .
    """
}
