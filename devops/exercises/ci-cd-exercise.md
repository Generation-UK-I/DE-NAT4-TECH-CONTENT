## DevOps CI/CD Exercise

### Introduction

In this exercise you will implement a GitHub Actions workflow to output a report on the number of lines of code in your mini project when it is committed.

This exercise will prepare you for implementing a CI/CD pipeline using GitHub actions for your group's final project.

For more information on GitHub Actions, refer to the [Documentation & Getting Started Guide](https://docs.github.com/en/actions)

### Exercise

### 1. Create a Workflow

Do this in your personal Mini Project repository.

1. Create a folder called `.github/workflows`
1. Create a new GitHub actions workflow using the provided `handouts/example-action.yml` file
    1. Copy it to the `.github/workflows` folder
    1. So that it is automatically located and loaded by github, the file must be exactly here:
    1. `.github/workflows/example-action.yml`

### 2. Trigger the Workflow

1. Add, Commit and Push your changes
1. In GitHub, navigate to the Actions for your repository and validate that the workflow has been created
1. Commit a minor change (e.g. add a new file or make an addition to your project README.md) and validate that the action is triggered by the commit
1. Validate the workflow lists the files in your project as expected

### 3. Extend the workflow's functionality

1. Restrict the workflow to trigger only when a push is made to `main` branch, not any other
1. Extend the workflow with new step(s) to perform a count of lines of code in the project (using `pygount` - see below)
    1. You will need to look this up in your breakout room

Requirements:

- Line counting will be achieved by the [pygount package](https://pypi.org/project/pygount/)
    - You will need a workflow step to install the package before it can be used
- Line count should produce a tabular output similar to the following:

```text
  Language    Files    %     Code    %     Comment    %
------------  -----  ------  ----  ------  -------  ------
Python            2   40.00    62   84.93        7  100.00
Text only         1   20.00     6    8.22        0    0.00
Transact-SQL      1   20.00     4    5.48        0    0.00
Markdown          1   20.00     1    1.37        0    0.00
------------  -----  ------  ----  ------  -------  ------
Sum total         5            73                7
```
