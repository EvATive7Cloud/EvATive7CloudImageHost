---
description: Sync the current project with the latest version of the evative7-app-template0 template repository
---

# Sync Template

This project was generated from `https://github.com/EvATive7/evative7-app-template0`, which is a simple Python + Vite project template for quickly developing applications.

Sync updates from the upstream template into the current project, including infrastructure changes such as CI, packaging logic, and toolchain code. For logic unique to the current project, ask the user for confirmation.

## Your Task

1. Check whether `.temp/evative7-app-template0` exists. If it does not exist, clone https://github.com/EvATive7/evative7-app-template0 to `.temp/evative7-app-template0`; if it already exists, run `git fetch --tags` to update it.
2. Get the latest git tag version number in `.temp/evative7-app-template0`, and compare it with the version number recorded in the `.evative7-app-template/.version` file in the current project.
3. If the versions are the same, the current project is already up to date, and the task ends.
4. If the versions are different, use `git diff <current version tag>..<latest version tag>` in `.temp/evative7-app-template0` to view all changes between the two versions.
5. Review the changes one by one, and introduce updates related to template infrastructure (CI workflow, packaging logic, toolchain configuration, dependency management, skills or instructions for AI agents, etc.) into the current project. For changes where it cannot be determined whether they should be introduced, or parts involving logic unique to the current project, the user must be asked for confirmation. Follow the principle of minimizing self-determined decisions: ask the user whenever there is any doubt.
6. After all changes have been introduced, update the `.evative7-app-template/.version` file to the latest template version number.
