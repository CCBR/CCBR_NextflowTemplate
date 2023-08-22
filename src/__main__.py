"""
Entrypoint for pipeline CLI

Check out the wiki for a detailed look at customizing this file:
https://github.com/beardymcjohnface/Snaketool/wiki/Customising-your-Snaketool
"""

import os
import click
from .util import (
    nek_base,
    get_version,
    copy_config,
    OrderedCommands,
    run_nextflow,
    print_citation,
)


def common_options(func):
    """Common options decorator for use with click commands."""
    options = [
        click.option(
            "--configfile",
            default="nextflow.config",
            help="Custom config file",
            show_default=True,
        ),
        click.option(  # when threads=None, uses max available
            "--threads",
            help="Number of threads to use",
            default=None,
            show_default=True,
        ),
        click.option(
            "--use-conda/--no-use-conda",
            default=False,
            help="Use conda for Nextflow processes",
            show_default=True,
        ),
        click.option(
            "--conda-frontend",
            type=click.Choice(["mamba", "conda"], case_sensitive=True),
            default="mamba",
            help="Specify Conda frontend",
            show_default=True,
        ),
        click.option(
            "--conda-prefix",
            default=nek_base(os.path.join("conda")),
            help="Custom conda env directory",
            type=click.Path(),
            show_default=False,
        ),
        click.argument("nextflow_args", nargs=-1),
    ]
    for option in reversed(options):
        func = option(func)
    return func


@click.group(
    cls=OrderedCommands, context_settings=dict(help_option_names=["-h", "--help"])
)
@click.version_option(get_version(), "-v", "--version", is_flag=True)
def cli():
    """CHromAtin iMmuno PrecipitAtion sequencinG aNalysis pipEline

    For more options, run:
    tool_name [command] --help"""
    pass


help_msg_extra = """
\b
CLUSTER EXECUTION:
tool_name run ... -profile [profile],[profile],...
For information on Nextflow config and profiles see:
https://www.nextflow.io/docs/latest/config.html#config-profiles
\b
RUN EXAMPLES:
Use singularity:    tool_name run ... -profile singularity
Specify threads:    tool_name run ... --threads [threads]
Enable conda:       tool_name run ... --use-conda
Add NextFlow args:  tool_name run ... -work-dir workDir -with-docker
"""


@click.command(
    epilog=help_msg_extra,
    context_settings=dict(
        help_option_names=["-h", "--help"], ignore_unknown_options=True
    ),
)
@common_options
def run(**kwargs):
    """Run the workflow"""
    # optional: merge config from CLI with nf config
    # run!
    run_nextflow(
        nextfile_path=nek_base(os.path.join("main.nf")),  # Full path to Nextflow file
        **kwargs,
    )


@click.command()
@click.option(
    "--configfile",
    default="nextflow.config",
    help="Copy template config to file",
    show_default=True,
)
def config(configfile, **kwargs):
    """Copy the system default config files"""
    copy_config(
        local_config=configfile,
        system_config=nek_base(os.path.join("workflow", "nextflow.config")),
    )


@click.command()
def citation(**kwargs):
    """Print the citation(s) for this tool"""
    print_citation()


cli.add_command(run)
cli.add_command(config)
# cli.add_command(citation) # TODO uncomment if tool_name is published in a journal or Zenodo


def main():
    cli()


if __name__ == "__main__":
    main()
