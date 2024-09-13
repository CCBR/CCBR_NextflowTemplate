process BWA_MEM {
    tag { meta.id }
    label 'process_high'

    container 'nciccbr/ccbr_ubuntu_base_20.04:v5'

    input:
        tuple val(meta), path(fastq)
        tuple val(meta_idx), path(index_files)

    output:
        tuple val(meta), path("*.bam"), path("*.bai"), emit: bam
        path  "versions.yml"                         , emit: versions

    when:
        task.ext.when == null || task.ext.when

    script:
    def prefix = task.ext.prefix ?: "${meta.id}"
    """
    # current working directory is a tmpdir when 'scratch' is set
    TMP=tmp/
    mkdir \$TMP
    trap 'rm -rf "\$TMP"' EXIT

    INDEX=`find -L ./ -name "*.amb" | sed 's/\\.amb\$//'`

    bwa mem \\
      -t ${task.cpus} \\
      -o \$TMP/align.bam \\
      \$INDEX \\
      ${fastq}

    samtools sort \\
      -@ ${task.cpus} \\
      -m 2G \\
      -T \$TMP \\
      --write-index \\
      -o ${prefix}.bam##idx##${prefix}.bam.bai \\
      \$TMP/align.bam

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        bwa: \$(echo \$(bwa 2>&1) | sed 's/^.*Version: //; s/Contact:.*\$//')
        samtools: \$(echo \$(samtools --version 2>&1) | sed 's/^.*samtools //; s/Using.*\$//')
    END_VERSIONS
    """

    stub:
    """
    touch ${meta.id}.bam ${meta.id}.bam.bai versions.yml
    """
}
