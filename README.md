<div align="center">

# evative7-app-template0

A project template for writing modern and distributable Python + vite apps, while ensuring unity of style and focus on code.

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

<!-- TODO: Finish this if you need badges
Replace: `YOURNAME`, `YOURREPO`

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/YOURNAME/YOURREPO/package.yml)](https://github.com/YOURNAME/YOURREPO/actions)
[![Coverage Status](https://coveralls.io/repos/YOURNAME/YOURREPO/badge.svg?branch=develop&service=github)](https://coveralls.io/github/YOURNAME/YOURREPO?branch=master)

-->
</div>

<!-- TODO: Remove below -->

## Quickstart

### Initialize

1. Generate a new project with this template
1. Settings → Actions → General → Workflow permissions, set `Read and write permissions` and enable `Allow GitHub Actions to create and approve pull requests` on Github
1. Replace `evative7-template0-app` to your app name
1. Install dependencies: `uv sync --all-groups` in `backend` and `pnpm install` in `frontend`

### Manage

- Backend uses `uv` as Python packages and project management tool
- Frontend uses `pnpm` as project management tool

### Then

Finish docs, README.md, AGENTS.md, LICENSE, TODOs and codes

### Commit

Follow the **Conventional Commit** rules strictly when writing commit messages.

### Build, Release and Version

- `uv run .\script\build.py` to build locally
- `release-please` will automatically manage version updates and releases based on commits by **SemVer**.
- When commits trigger a version change, `release-please` will create a release PR. Merge that PR to publish the new version and release.
- To manually specify a version in a commit, add `Release-As: x.x.x` in the commit body.
