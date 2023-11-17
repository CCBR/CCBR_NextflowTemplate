from cffconvert.cli.create_citation import create_citation
from cffconvert.cli.validate_or_write_output import validate_or_write_output
from time import localtime, strftime

import click
import collections.abc
import os
import pprint
import shutil
import stat
import subprocess
import sys
import yaml


def nek_base(rel_path):
    basedir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
    return os.path.join(basedir, rel_path)


def get_version():
    with open(nek_base("VERSION"), "r") as f:
        version = f.readline()
    return version


def print_citation(context, param, value):
    citation = create_citation(nek_base("CITATION.cff"), None)
    # click.echo(citation._implementation.cffobj['message'])
    validate_or_write_output(None, "bibtex", False, citation)
    context.exit()


def msg(err_message):
    tstamp = strftime("[%Y:%m:%d %H:%M:%S] ", localtime())
    click.echo(tstamp + err_message, err=True)


def msg_box(splash, errmsg=None):
    msg("-" * (len(splash) + 4))
    msg(f"| {splash} |")
    msg(("-" * (len(splash) + 4)))
    if errmsg:
        click.echo("\n" + errmsg, err=True)


def append_config_block(nf_config="nextflow.config", scope=None, **kwargs):
    with open(nf_config, "a") as f:
        f.write(scope.rstrip() + "{" + "\n")
        for k in kwargs:
            f.write(f"{k} = {kwargs[k]}\n")
        f.write("}\n")


def copy_config(config_paths, overwrite=True):
    msg(f"Copying default config files to current working directory")
    for local_config in config_paths:
        system_config = nek_base(local_config)
        if os.path.isfile(system_config):
            shutil.copyfile(system_config, local_config)
        elif os.path.isdir(system_config):
            shutil.copytree(system_config, local_config, dirs_exist_ok=overwrite)
        else:
            raise FileNotFoundError(f"Cannot copy {system_config} to {local_config}")


def read_config(file):
    with open(file, "r") as stream:
        _config = yaml.safe_load(stream)
    return _config


def update_config(config, overwrite_config):
    def _update(d, u):
        for key, value in u.items():
            if isinstance(value, collections.abc.Mapping):
                d[key] = _update(d.get(key, {}), value)
            else:
                d[key] = value
        return d

    _update(config, overwrite_config)


def write_config(_config, file):
    msg(f"Writing runtime config file to {file}")
    with open(file, "w") as stream:
        yaml.dump(_config, stream)


def chmod_bins_exec():
    """Ensure that all files in bin/ are executable.

    It appears that setuptools strips executable permissions from package_data files,
    yet post-install scripts are not possible with the pyproject.toml format.
    So this function will run when `run()` is called.
    Without this hack, nextflow processes that call scripts in bin/ fail.

    https://stackoverflow.com/questions/18409296/package-data-files-with-executable-permissions
    https://github.com/pypa/setuptools/issues/2041
    https://stackoverflow.com/questions/76320274/post-install-script-for-pyproject-toml-projects
    """
    bin_dir = nek_base("bin/")
    for filename in os.listdir(bin_dir):
        bin_path = os.path.join(bin_dir, filename)
        if os.path.isfile(bin_path):
            file_stat = os.stat(bin_path)
            # below is equivalent to `chmod +x`
            os.chmod(
                bin_path, file_stat.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
            )


class OrderedCommands(click.Group):
    """Preserve the order of subcommands when printing --help"""

    def list_commands(self, ctx: click.Context):
        return list(self.commands)


def scontrol_show():
    scontrol_dict = dict()
    scontrol_out = subprocess.run(
        "scontrol show config", shell=True, capture_output=True, text=True
    ).stdout
    if len(scontrol_out) > 0:
        for line in scontrol_out.split("\n"):
            line_split = line.split("=")
            if len(line_split) > 1:
                scontrol_dict[line_split[0].strip()] = line_split[1].strip()
    return scontrol_dict


hpc_options = {
    "biowulf": {"profile": "biowulf", "slurm": "assets/slurm_header_biowulf.sh"},
    "fnlcr": {
        "profile": "frce",
        "slurm": "assets/slurm_header_frce.sh",
    },
}


def get_hpc():
    scontrol_out = scontrol_show()
    if "ClusterName" in scontrol_out.keys():
        hpc = scontrol_out["ClusterName"]
    else:
        hpc = None
    return hpc


def run_nextflow(
    nextfile_path=None,
    merge_config=None,
    threads=None,
    nextflow_args=None,
    mode="local",
):
    """Run a Nextflow workflow"""
    nextflow_command = ["nextflow", "run", nextfile_path]

    hpc = get_hpc()
    if mode == "slurm" and not hpc:
        raise ValueError("mode is 'slurm' but no HPC environment was detected")
    # add any additional Nextflow commands
    args_dict = dict()
    prev_arg = ""
    for arg in nextflow_args:
        if arg.startswith("-"):
            args_dict[arg] = ""
        elif prev_arg.startswith("-"):
            args_dict[prev_arg] = arg
        prev_arg = arg
    # make sure profile matches biowulf or frce
    profiles = (
        set(args_dict["-profile"].split(","))
        if "-profile" in args_dict.keys()
        else set()
    )
    if mode == "slurm":
        profiles.add("slurm")
    if hpc:
        profiles.add(hpc_options[hpc]["profile"])
    args_dict["-profile"] = ",".join(sorted(profiles))
    nextflow_command += list(f"{k} {v}" for k, v in args_dict.items())

    # Print nextflow command
    nextflow_command = " ".join(str(nf) for nf in nextflow_command)
    msg_box("Nextflow command", errmsg=nextflow_command)

    if mode == "slurm":
        slurm_filename = "submit_slurm.sh"
        with open(slurm_filename, "w") as sbatch_file:
            with open(nek_base(hpc_options[hpc]["slurm"]), "r") as template:
                sbatch_file.writelines(template.readlines())
            sbatch_file.write(nextflow_command)
        run_command = f"sbatch {slurm_filename}"
        msg_box("Slurm batch job", errmsg=run_command)
    elif mode == "local":
        if hpc:
            nextflow_command = f'bash -c "module load nextflow && {nextflow_command}"'
        run_command = nextflow_command
    else:
        raise ValueError(f"mode {mode} not recognized")
    # Run Nextflow!!!
    subprocess.run(run_command, shell=True, check=True)
