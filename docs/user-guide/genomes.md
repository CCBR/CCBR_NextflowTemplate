# Genomes

<!--
This file is created by concatenating _genomes_tail.md and the auto-generated genomes list.
Do not edit guide/genomes.md manually.
-->

## Supported reference genomes

These genomes are available on biowulf.

### Reference Genomes

These genomes can be passed to the `--genome` parameter.

#### `hg38`

- species: `Homo sapiens`
- fasta: `${params.index_dir}/hg38_basic/hg38_basic.fa`
- genes_gtf: `${params.index_dir}/hg38_basic/genes.gtf`
- blacklist_index: `${params.index_dir}/hg38_basic/indexes/blacklist/hg38.blacklist_v3.chrM.chr_rDNA.*`
- reference_index: `${params.index_dir}/hg38_basic/bwa_index/hg38*`
- chromosomes_dir: `${params.index_dir}/hg38_basic/Chromsomes/`
- chrom_sizes: `${params.index_dir}/hg38_basic/indexes/hg38.fa.sizes`
- gene_info: `${params.index_dir}/hg38_basic/geneinfo.bed`
- effective_genome_size: `2700000000`
- meme_motifs: `${projectDir}/assets/HOCOMOCOv11_core_HUMAN_mono_meme_format.tar.gz`
- bioc_txdb: `TxDb.Hsapiens.UCSC.hg38.knownGene`
- bioc_annot: `org.Hs.eg.db`

#### `hg19`

- species: `Homo sapiens`
- fasta: `${params.index_dir}/hg19_basic/hg19.fa`
- genes_gtf: `${params.index_dir}/hg19_basic/genes.gtf`
- blacklist_index: `${params.index_dir}/hg19_basic/indexes/blacklist/hg19.blacklist.*`
- reference_index: `${params.index_dir}/hg19_basic/bwa_index/hg19.*`
- chromosomes_dir: `${params.index_dir}/hg19_basic/Chromosomes`
- chrom_sizes: `${params.index_dir}/hg19_basic/Chromosomes/chrom.sizes`
- gene_info: `${params.index_dir}/hg19_basic/geneinfo.bed`
- effective_genome_size: `2700000000`
- meme_motifs: `${projectDir}/assets/HOCOMOCOv11_core_HUMAN_mono_meme_format.tar.gz`
- bioc_txdb: `TxDb.Hsapiens.UCSC.hg38.knownGene`
- bioc_annot: `org.Hs.eg.db`

#### `mm10`

- species: `Mus musculus`
- fasta: `${params.index_dir}/mm10_basic/mm10_basic.fa`
- genes_gtf: `${params.index_dir}/mm10_basic/genes.gtf`
- blacklist_index: `${params.index_dir}/mm10_basic/indexes/blacklist/mm10.blacklist.chrM.chr_rDNA.*`
- reference_index: `${params.index_dir}/mm10_basic/indexes/reference/mm10*`
- chromosomes_dir: `${params.index_dir}/mm10_basic/Chromsomes/`
- chrom_sizes: `${params.index_dir}/mm10_basic/indexes/mm10.fa.sizes`
- gene_info: `${params.index_dir}/mm10_basic/geneinfo.bed`
- effective_genome_size: `2400000000`
- meme_motifs: `${projectDir}/assets/HOCOMOCOv11_core_MOUSE_mono_meme_format.tar.gz`
- bioc_txdb: `TxDb.Mmusculus.UCSC.mm10.knownGene`
- bioc_annot: `org.Mmu.eg.db`

### Spike-in Genomes

These genomes can be passed to the `--spike_genome` parameter.

#### `dmelr6.32`

- species: `Drosophila melanogaster`
- fasta: `${params.index_dir}/dmelr6.32/indexes/dmelr6.32.fa`
- reference_index: `${params.index_dir}/dmelr6.32/indexes/bwa/Drosophila_melanogaster.*`
- blacklist_index: `${params.index_dir}/dmelr6.32/indexes/blacklist/dmelr6.32.blacklist.*`
- blacklist_bed: `${params.index_dir}/dmelr6.32/indexes/dm6-blacklist.v2.no_chr.bed.gz`
- effective_genome_size: `142573017`
- chrom_sizes: `${params.index_dir}/dmelr6.32/chrom_dmelr6.28.sizes`

#### `ecoli_k12`

- species: `Escherichia coli K-12`
- fasta: `${params.index_dir}/ecoli_k12/indexes/ecoli_k12.fa`
- reference_index: `${params.index_dir}/ecoli_k12/indexes/ecoli_k12.*`
- blacklist_bed: `NO_FILE`
- effective_genome_size: `4641652`
- chrom_sizes: `${params.index_dir}/ecoli_k12/Chromosomes/chrom.sizes`
