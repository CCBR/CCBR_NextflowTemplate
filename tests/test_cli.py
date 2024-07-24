import pytest
import subprocess


def test_help():
    output = subprocess.run(
        "bin/tool_name --help", capture_output=True, shell=True, text=True
    ).stdout
    assert "TOOL_NAME" in output


def test_version():
    output = subprocess.run(
        "bin/tool_name --version", capture_output=True, shell=True, text=True
    ).stdout
    assert "tool_name, version " in output


def test_citation():
    output = subprocess.run(
        "bin/tool_name --citation", capture_output=True, shell=True, text=True
    ).stdout
    assert "@misc{" in output


def test_subcommands_help():
    assert all(
        [
            f"tool_name {cmd} [OPTIONS]"
            in subprocess.run(
                f"bin/tool_name {cmd} --help",
                capture_output=True,
                shell=True,
                text=True,
            ).stdout
            for cmd in ["run", "init"]
        ]
    )
