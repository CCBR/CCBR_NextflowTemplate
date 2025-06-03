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

    docs: https://ccbr.github.io/TOOL_NAME

    For more options, run:
    tool_name [command] --help"""
    pass


help_msg_extra = """
\b
Nextflow options:
-profile <profile>    Nextflow profile to use (e.g. test)
-params-file <file>   Nextflow params file to use (e.g. assets/params.yml)
-preview              Preview the processes that will run without executing them

\b
EXAMPLES:
Execute with slurm:
  tool_name run --output path/to/outdir --mode slurm
Preview the processes that will run:
  tool_name run --output path/to/outdir --mode local -preview
Add nextflow args (anything supported by `nextflow run`):
  tool_name run --output path/to/outdir --mode slurm -profile test
  tool_name run --output path/to/outdir --mode slurm -profile test -params-file assets/params.yml
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
    hidden=True,
)
@click.option(
    "--output",
    help="Output directory path for tool_name init & run. Equivalient to nextflow launchDir. Defaults to your current working directory.",
    type=click.Path(file_okay=False, dir_okay=True, writable=True),
    default=pathlib.Path.cwd(),
    show_default=False,
)
@click.option(
    "--mode",
    "_mode",
    help="Run mode (slurm, local)",
    type=str,
    default="slurm",
    show_default=True,
)
@click.option(
    "--forceall",
    "-F",
    "force_all",
    help="Force all processes to run (i.e. do not use nextflow -resume)",
    is_flag=True,
    default=False,
    show_default=True,
)
@click.argument("nextflow_args", nargs=-1)
def run(main_path, output, _mode, force_all, **kwargs):
    """
    Run the workflow

    Note: you must first run `tool_name init --output <output_dir>` to initialize
    the output directory.

    docs: https://ccbr.github.io/TOOL_NAME
    """
    if (  # this is the only acceptable github repo option for tool_name
        main_path != "CCBR/TOOL_NAME"
    ):
        # make sure the path exists
        if not os.path.exists(main_path):
            raise FileNotFoundError(
                f"Path to the tool_name main.nf file not found: {main_path}"
            )
    output_dir = output if isinstance(output, pathlib.Path) else pathlib.Path(output)
    if not output_dir.is_dir() or not (output_dir / "nextflow.config").exists():
        raise FileNotFoundError(
            f"output directory not initialized: {output_dir}. Hint: you must initialize the output directory with `tool_name init --output {output_dir}`"
        )
    current_wd = os.getcwd()
    try:
        os.chdir(output_dir)

        ccbr_tools.pipeline.nextflow.run(
            nextfile_path=main_path,
            mode=_mode,
            force_all=force_all,
            pipeline_name="TOOL_NAME",
            **kwargs,
        )
    finally:
        os.chdir(current_wd)


@click.command()
@click.option(
    "--output",
    help="Output directory path for tool_name init & run. Equivalient to nextflow launchDir. Defaults to your current working directory.",
    type=click.Path(file_okay=False, dir_okay=True, writable=True),
    default=pathlib.Path.cwd(),
    show_default=False,
)
def init(output, **kwargs):
    """Initialize the working directory by copying the system default config files"""
    output_dir = output if isinstance(output, pathlib.Path) else pathlib.Path(output)
    ccbr_tools.pkg_util.msg_box(f"Initializing TOOL_NAME in {output_dir}")
    (output_dir / "log/").mkdir(parents=True, exist_ok=True)
    paths = ("nextflow.config", "conf/", "assets/")
    ccbr_tools.pipeline.util.copy_config(paths, repo_base=repo_base, outdir=output_dir)


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
