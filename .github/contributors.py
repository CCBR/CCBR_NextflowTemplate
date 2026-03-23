#!/usr/bin/env python3
import sys
import warnings

from ccbr_tools.github import get_repo_contributors, get_user_info

CONTRIB_MD = ["# Contributors\n"]


def get_contrib_html(contrib):
    user_html = None
    user_login = contrib["login"]
    try:
        user_info = get_user_info(user_login)
    except ConnectionError as exc:
        warnings.warn(
            f"Skipping contributor '{user_login}': {exc}",
            RuntimeWarning,
        )
        user_html = None
    else:
        user_name = user_info["name"] if user_info["name"] else user_login
        avatar_url = contrib["avatar_url"]
        profile_url = contrib["html_url"]
        if profile_url.startswith("https://github.com/apps/"):
            user_html = None
        else:
            user_html = (
                f"<a href='{profile_url}' title='{user_name}' style='display: inline-block; text-align: center;'>"
                f"<img src='{avatar_url}' alt='{user_name}' style='border-radius: 50%; width: 30%;'>"
                f"<br>{user_name}</a>"
            )
    return user_html


def main(contribs_md=CONTRIB_MD, org_repo="CCBR/CCBR_NextflowTemplate", ncol=3):
    org, repo = org_repo.split("/")
    header = "|" + " |" * ncol + "\n|" + "---|" * ncol
    contribs_str = header
    contribs = get_repo_contributors(repo, org)
    row_cells = []
    for contrib in contribs:
        contrib_html = get_contrib_html(contrib)
        if not contrib_html:
            continue
        row_cells.append(contrib_html)
        if len(row_cells) == ncol:
            contribs_str += "\n| " + " | ".join(row_cells) + " |"
            row_cells = []
    if row_cells:
        contribs_str += "\n| " + " | ".join(row_cells) + " |"
    contribs_md.append(contribs_str)

    contribs_md.append(
        f"\nView the [contributors graph on GitHub](https://github.com/{org_repo}/graphs/contributors) for more details."
    )

    with open("docs/contributors.md", "w") as f:
        f.write("\n".join(contribs_md))


if __name__ == "__main__":
    main(org_repo=sys.argv[1] if len(sys.argv) > 1 else "CCBR/CCBR_NextflowTemplate")
