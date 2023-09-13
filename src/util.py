import sys
import os
import subprocess
import yaml
import collections.abc
from shutil import copyfile
import stat
from time import localtime, strftime

import click


def nek_base(rel_path):
    basedir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
    return os.path.join(basedir, rel_path)


def get_version():
    with open(nek_base("VERSION"), "r") as f:
        version = f.readline()
    return version


def print_citation():
    with open(nek_base("CITATION.cff"), "r") as f:
        for line in f:
            click.echo(line, nl=False, err=True)


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


def copy_config(local_config=None, system_config=None):
    msg(f"Copying system default config to {local_config}")
    copyfile(system_config, local_config)


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
        file_stat = os.stat(bin_path)
        # below is equivalent to `chmod +x`
        os.chmod(
            bin_path, file_stat.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        )


class OrderedCommands(click.Group):
    """Preserve the order of subcommands when printing --help"""

    def list_commands(self, ctx: click.Context):
        return list(self.commands)


def is_biowulf():
    is_biowulf = False
    for env_var in ("HOSTNAME", "SLURM_SUBMIT_HOST"):
        if env_var in os.environ.keys() and os.environ[env_var] == "biowulf.nih.gov":
            is_biowulf = True
    return is_biowulf


def run_nextflow(
    paramsfile=None,
    configfile=None,
    nextfile_path=None,
    merge_config=None,
    threads=None,
    nextflow_args=None,
):
    """Run a Nextflow workfile"""
    nextflow_command = ["nextflow", "run", nextfile_path]

    if paramsfile:
        # copy sys default params if needed
        copy_config(
            local_config=paramsfile,
            system_config=nek_base("params.yaml"),
        )
        # read the params
        nf_config = read_config(paramsfile)
        # merge in command line params if provided
        if merge_config:
            update_config(nf_config, merge_config)
        # update params file
        write_config(nf_config, paramsfile)
        nextflow_command += ["-params-file", paramsfile]
        # display the runtime params
        msg_box("Runtime parameters", errmsg=yaml.dump(nf_config, Dumper=yaml.Dumper))

    if configfile:
        if not os.path.exists(configfile):
            copy_config(
                local_config=configfile,
                system_config=nek_base("nextflow.config"),
            )

        # add threads
        if threads:  # when threads=None, uses max available
            append_config_block(scope="executor", cpus=threads)

        nextflow_command += ["-c", configfile]

        # display the runtime configuration
        # msg_box("Launcher Configuration", errmsg=open(configfile, "r").read()) # TODO verbose flag to toggle printing config?

    # add any additional Nextflow commands
    if nextflow_args:
        nextflow_command += list(nextflow_args)

    # make sure bins are executable for nextflow processes
    chmod_bins_exec()

    # Run Nextflow!!!
    nextflow_command = " ".join(str(nf) for nf in nextflow_command)
    if is_biowulf():
        nextflow_command = f'bash -c "module load nextflow && {nextflow_command}"'
    msg_box("Nextflow command", errmsg=nextflow_command)
    subprocess.run(nextflow_command, shell=True, check=True)
