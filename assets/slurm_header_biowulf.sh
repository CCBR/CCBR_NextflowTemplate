#!/usr/bin/env bash
#SBATCH --cpus-per-task=1
#SBATCH --mem=1g
#SBATCH --time=1-00:00:00
#SBATCH --parsable
#SBATCH -J "tool_name"
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --output "log/slurm_%j.log"
#SBATCH --output "log/slurm_%j.log"

module load ccbrpipeliner
module load nextflow
NXF_SINGULARITY_CACHEDIR=/data/CCBR_Pipeliner/SIFS
