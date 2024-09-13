"""
Entrypoint for TOOL_NAME CLI

Check out the wiki for a detailed look at customizing this file:
https://github.com/beardymcjohnface/Snaketool/wiki/Customising-your-Snaketool
"""
import cffconvert.cli.cli
import click
import os
import pathlib

import ccbr_tools.pkg_util
import ccbr_tools.pipeline.util
import ccbr_tools.pipeline.nextflow


def repo_base(*paths):
    basedir = pathlib.Path(__file__).absolute().parent.parent
    return basedir.joinpath(*paths)


def print_citation_flag(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    ccbr_tools.pkg_util.print_citation(
        citation_file=repo_base("CITATION.cff"), output_format="bibtex"
    )
    ctx.exit()


def common_options(func):
    """Common options decorator for use with click commands."""
    options = [
        click.argument("nextflow_args", nargs=-1),
    ]
    for option in reversed(options):
        func = option(func)
    return func


@click.group(
    cls=ccbr_tools.pkg_util.CustomClickGroup,
    context_settings=dict(help_option_names=["-h", "--help"]),
)
@click.version_option(
    ccbr_tools.pkg_util.get_version(repo_base=repo_base),
    "-v",
    "--version",
    is_flag=True,
)
@click.option(
    "-c",
    "--citation",
    callback=print_citation_flag,
    is_eager=True,
    is_flag=True,
    expose_value=False,
    help="Print the citation in bibtex format and exit.",
)
def cli():
    """TODO oneline description of TOOL_NAME

    For more options, run:
    tool_name [command] --help"""
    pass


help_msg_extra = """
\b
EXAMPLES:
Execute with slurm:
    tool_name run ... --mode slurm
Preview the processes that will run:
    tool_name run ... --mode local -preview
Add nextflow args (anything supported by `nextflow run`):
    tool_name run ... -work-dir path/to/workDir
Run with a specific installation of tool_name:
    tool_name run --main path/to/tool_name/main.nf ...
Run with a specific tag, branch, or commit from GitHub:
    tool_name run --main CCBR/TOOL_NAME -r v0.1.0 ...
"""


@click.command(
    epilog=help_msg_extra,
    context_settings=dict(
        help_option_names=["-h", "--help"], ignore_unknown_options=True
    ),
)
@click.option(
    "--main",
    "main_path",
    help="Path to the tool_name main.nf file or the GitHub repo (CCBR/TOOL_NAME). Defaults to the version installed in the $PATH.",
    type=str,
    default=repo_base("main.nf"),
    show_default=True,
)
@click.option(
    "--mode",
    "_mode",
    help="Run mode (slurm, local)",
    type=str,
    default="local",
    show_default=True,
)
@common_options
def run(main_path, _mode, **kwargs):
    """Run the workflow"""
    if (  # this is the only acceptable github repo option for tool_name
        main_path != "CCBR/TOOL_NAME"
    ):
        # make sure the path exists
        if not os.path.exists(main_path):
            raise FileNotFoundError(
                f"Path to the tool_name main.nf file not found: {main_path}"
            )

    ccbr_tools.pipeline.nextflow.run(
        nextfile_path=main_path,
        mode=_mode,
        pipeline_name="TOOL_NAME",
        **kwargs,
    )


@click.command()
def init(**kwargs):
    """Initialize the working directory by copying the system default config files"""
    paths = ("nextflow.config", "conf/", "assets/")
    ccbr_tools.pipeline.util.copy_config(paths, repo_base=repo_base)
    os.makedirs("log", exist_ok=True)


@click.command()
@click.argument(
    "citation_file",
    type=click.Path(exists=True),
    required=True,
    default=repo_base("CITATION.cff"),
)
@click.option(
    "--output-format",
    "-f",
    default="bibtex",
    help="Output format for the citation",
    type=cffconvert.cli.cli.options["outputformat"]["type"],
)
def cite(citation_file, output_format):
    """
    Print the citation in the desired format

    citation_file : Path to a file in Citation File Format (CFF) [default: the CFF for ccbr_tools]
    """
    ccbr_tools.pkg_util.print_citation(
        citation_file=citation_file, output_format=output_format
    )


cli.add_command(run)
cli.add_command(init)
cli.add_command(cite)


def main():
    cli()


cli(prog_name="tool_name")

if __name__ == "__main__":
    main()
