<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/TUW-GEO/canvodpy/main/docs/assets/logo/canvodpy_logo_dark_mode.svg">
    <img alt="canVODpy logo" src="https://raw.githubusercontent.com/TUW-GEO/canvodpy/main/docs/assets/logo/canvodpy_logo_bright_mode.svg" width="312">
  </picture>
</p>

# copier-canvod

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)

**A [copier](https://copier.readthedocs.io/) template for a new `canvod-*`
package for [canVODpy](https://canvodpy.eu/).** It creates a repository
of its own that is built exactly like
[canvodpy-extensions](https://github.com/TUW-GEO/canvodpy-extensions),
reduced to one package: the same uv workspace, `just` recipes, git hooks,
GitHub Actions, Zensical docs site and coding-agent files. The package
can start private, stay on its own, or move into canvodpy-extensions or
canvodpy later by copying its folder.

## Create a package

You need [uv](https://docs.astral.sh/uv/), [just](https://github.com/casey/just)
and git.

```bash
uvx copier copy --trust gh:TUW-GEO/copier-canvod canvod-<name>
cd canvod-<name>
just sync          # one .venv, plus the pre-commit, commit-msg and pre-push hooks
just check && just test && just docs-build
git commit -m "chore: generate from copier-canvod"
```

Once the repository exists on GitHub, `just labels` creates the labels
canvodpy uses: `needs-triage`, `needs-info`, `ready-for-agent`,
`ready-for-human` (issue forms and triage) and `ci`, `dependencies`,
`python` (Dependabot). GitHub drops labels that don't exist.

`--trust` lets copier run the template's three tasks after copying:
`git init`, `uv lock` and `git add`. copier asks:

| Question | Example | Used for |
|---|---|---|
| `dist_name` | `canvod-science-viz` | Distribution name, tag prefix `canvod-science-viz-v1.0.0` |
| `short_name` | `science-viz` | Commit scope, docs folder `docs/packages/science-viz/` |
| `module_name` | `science_viz` | `import canvod.science_viz` (a namespace package, like canvodpy's) |
| `description` | one sentence | `pyproject.toml`, READMEs, docs, `CITATION.cff` |
| `canvodpy_deps` | `canvod-grids`, `canvod-viz` | Dependencies, bound `>=1.0.0,<2` |
| `target` | canvodpy-extensions | Where it should end up (`MOVING.md`) |
| `github_owner`, `repo_name` | your user, `canvod-science-viz` | Every link |
| `author_name`, `author_email`, `author_orcid`, `affiliation` | | `pyproject.toml`, `NOTICE`, `SECURITY.md`, `CITATION.cff`, `REUSE.toml` |
| `author_family_name` | `van der Berg` | `CITATION.cff`: the end of `author_name`, with any particles |
| `github_handle` | your GitHub user (not an organisation) | Code owner of every file (`.github/CODEOWNERS`) |
| `copyright_year` | `2026` | `NOTICE`, `REUSE.toml` |
| `ci_enabled` | `false` | Whether GitHub Actions run automatically (see below) |
| `docs_domain`, `impressum_url` | empty | GitHub Pages domain, legal notice in the docs footer |

The answers are kept in `.copier-answers.yml`. When this template changes
(a new ruff or Python version, a new hook, a fixed workflow), take the
change into your package with:

```bash
uvx copier update --trust
```

copier merges the template's change into your files and leaves your own
edits in place; a conflict shows up as conflict markers to resolve.

## What a package gets

```text
canvod-<name>/
├── packages/canvod-<name>/        the package: moves as it is
│   ├── src/canvod/<module>/       code (canvod is a namespace package)
│   ├── tests/
│   ├── pyproject.toml  README.md  AGENTS.md  CLAUDE.md  Justfile  LICENSE  NOTICE
├── docs/                          Zensical site: packages/<short>/, api/, releasing, contributing
├── release-notes/                 marimo notebook per minor or major release
├── tools/  scripts/               checks run by the hooks and CI, agent git guard
├── .github/                       workflows, issue and pull request forms, Dependabot
├── .claude/                       agent settings and task guides (skills)
├── AGENTS.md  CODING_STANDARDS.md  CONTRIBUTING.md  MOVING.md  SECURITY.md
└── pyproject.toml  Justfile  cliff.toml  zensical.toml  lychee.toml  .vale.ini  REUSE.toml  CITATION.cff
```

### Tools on your machine

| Tool | What it does here | Run it with |
|---|---|---|
| [uv](https://docs.astral.sh/uv/) | Workspace (`packages/*`), one `.venv`, `uv.lock`. Takes only PyPI files at least a week old (`exclude-newer`), except canvodpy's own packages | `just sync` |
| [just](https://github.com/casey/just) | Every recurring task is a recipe; the recipes are canvodpy-extensions' | `just --list` |
| [ruff](https://docs.astral.sh/ruff/) | Lint and format | `just check` |
| [ty](https://docs.astral.sh/ty/) | Type check | `just check-types` |
| [pytest](https://docs.pytest.org/) + pytest-cov | Tests with coverage | `just test`, `just test-package` |
| [pre-commit](https://pre-commit.com/) | Git hooks, below | `just hooks` |
| [commitizen](https://commitizen-tools.github.io/commitizen/) | Conventional commit messages (commit-msg hook) | on every commit |
| [git-cliff](https://git-cliff.org/) | The package's `CHANGELOG.md` from the commits | `just changelog`, `just release` |
| [marimo](https://marimo.io/) | Release notebooks | `just check-release-notes` |
| [Zensical](https://zensical.org/) + [mkdocstrings](https://mkdocstrings.github.io/) | Docs site, API pages from the docstrings (numpy style) | `just docs`, `just docs-build` |
| [Vale](https://vale.sh/) | Language of the docs pages (Google style, canVODpy vocabulary) | `just docs-lint` |
| [lychee](https://lychee.cli.rs/) | Links of the built docs site | `just docs-links` |
| [REUSE](https://reuse.software/) | License and copyright of every file (`REUSE.toml`) | `just check-reuse` |

**Git hooks** (`.pre-commit-config.yaml`). On every commit: ruff lint
and format, `uv lock` up to date, trailing whitespace, end of file, large
files, private keys, and the agent docs check (every path and `just`
recipe named in `AGENTS.md` files and skills must exist). On the commit
message: commitizen. Before a push: ty.

### GitHub Actions

| Workflow | When | What it does |
|---|---|---|
| `ci.yml` | pull request, push to `main`, weekly | Calls the three below and sums them up in one check, `ci-ok`. A pull request that changes only docs skips ty and the tests (`tools/ci_changes.py`) |
| `code_quality.yml` | from `ci.yml` | `uv.lock` up to date, ruff lint and format, ty, release notebook format, agent docs check against the locked canvodpy |
| `test_platforms.yml` | from `ci.yml` | pytest on Linux, macOS and Windows; coverage to Coveralls and as a pull request comment |
| `docs_quality.yml` | from `ci.yml`, or by hand | Vale on the changed docs pages; lychee on the built site (links between pages on every run, external links weekly, opening an issue when one fails) |
| `codeql.yml` | pull request, push, weekly | GitHub CodeQL security and quality analysis of the Python code |
| `scorecard.yml` | push, weekly | OpenSSF Scorecard: supply-chain security practices of the repository |
| `fair-software.yml` | pull request, push | howfairis: the [fair-software.eu](https://fair-software.eu) recommendations |
| `wait_exemptions.yml` | when the exemptions change, weekly | The one-week wait exemptions name exactly canvodpy's released packages |
| `release.yml` | a pushed tag `canvod-*-v*` | Checks the tag against the version, drafts a GitHub release from the changelog and links the release notebook |
| `deploy_docs.yml` | a published release, or by hand | Builds the docs and deploys them to GitHub Pages |

Every action is pinned to a commit, with read-only permissions unless a
job needs more. **Dependabot** proposes weekly updates of the actions, the
pre-commit hooks and the uv dependencies; the uv updates wait a week, as
`uv lock` does.

**Off by default.** A private repository pays for GitHub Actions minutes
beyond a free monthly quota, so with `ci_enabled: false` (the default)
every workflow is still there but runs only when started by hand
(`gh workflow run ci.yml`). Run `just check` and `just test` before every
pull request instead. When the repository goes public, switch them on:

```bash
uvx copier update --trust --data ci_enabled=true
```

Coveralls needs a `COVERALLS_REPO_TOKEN` secret in a private repository.

### Coding agents

`AGENTS.md` (root and package; `CLAUDE.md` imports it) says where things
live, the canvodpy code to read first and the rules. Task guides for
releasing and for changing the canvodpy dependency are in
`.claude/skills/`. `.claude/settings.json` and `scripts/agent_git_guard.py`
stop Claude Code from merging, pushing `main` or tags, force-pushing and
skipping hooks. `just agent-skills` installs the agent workflow canVODpy
uses (the mattpocock-skills plugin).

Commits, pull requests and issues follow canvodpy: conventional commits
checked by commitizen, `Co-Authored-By:` for substantial agent help
(`CODING_STANDARDS.md`), the same pull request template (summary,
evidence, merge danger, checklist), the same bug and feature forms, and
the same triage labels (`docs/agents/triage-labels.md`).

## What it doesn't do

- **No PyPI, no Zenodo.** There is no publish workflow and no
  `.zenodo.json`. The `canvod-*` names on PyPI and the canVODpy records
  on Zenodo belong to the canVODpy maintainers; a package is published
  once it is part of canvodpy or canvodpy-extensions. Until then, users
  install a release from its git tag.
- **No fuzzing.** canvodpy-extensions fuzzes its parsers with atheris; a
  harness is specific to a parser. Add it when the package parses files.

## Moving a package into canvodpy-extensions or canvodpy

`MOVING.md` in the generated repository lists what moves (the package
folder, its docs pages and release notebooks) and what stays, and how to
keep the history with `git subtree`. The canVODpy maintainers decide
whether a package moves; open an issue there first.

## Developing this template

The template lives in `template/`; files ending in `.jinja` are rendered.
The Jinja delimiters are `[[ ]]`, `[% %]` and `[# #]`, so GitHub Actions'
`${{ }}`, just's `{{ }}` and git-cliff's templates stay untouched; a TOML
array of tables is written `[[ '[[' ]]name]]`. Most files are
canvodpy-extensions' own: change them there first, then here.

```bash
just test          # generate four packages and check each; bad answers must be refused
```

`just test` generates a package with CI off, one with CI on, one with
awkward answers (a long name, a family name with particles, every
optional answer set, several dependencies) and one with a one-word author
name. For each it checks that every TOML, YAML, `CITATION.cff` file and
Markdown front matter parses (`tests/check_generated.py`), then runs
`just check`, `just test`, `just check-release-notes`, `just check-reuse`
and the docs build. Last, it checks that copier refuses answers that
would break a package: canvodpy's own names, Python keywords, quotes in
answers that go into TOML or YAML strings.

### Releasing the template

The template is released as git tags `v<version>` with a GitHub release,
and `copier copy` and `copier update` take the newest tag. Versions
follow canvodpy's rules, applied to the template:

| Change | Goes into |
|---|---|
| A fix: a wrong file, hook or text in generated packages | the next patch version |
| A new question, file or recipe, or a question marked as going away | the next minor version |
| A question renamed or removed, or a change that breaks `copier update` of existing packages | the next major version |

If it is unclear which, ask the maintainers instead of guessing.

```bash
git switch -c chore/release-0.2.0
just changelog                                  # changes since the last release
just release minor                              # or patch, major, or a version such as 0.2.0rc1
git push --no-follow-tags -u origin chore/release-0.2.0
# open the PR, merge it, then on an up-to-date main:
just tag                                        # tags main and pushes the tag
```

`just release` runs `just test`, then writes the new section of
`CHANGELOG.md` from the commits. Pushing the tag drafts a GitHub release
from that section; publish it by hand. From a pre-release such as
`0.2.0rc1`, give the final version (`just release 0.2.0`), since
`minor` would skip it.

## License

Licensed under the [Apache License 2.0](LICENSE).
