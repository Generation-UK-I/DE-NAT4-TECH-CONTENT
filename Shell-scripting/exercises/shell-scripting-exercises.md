### Exercise

- Write a script that will run your test suite and then do a git commit if the tests pass.

The script should meet the following requirements:

1. Be executable from the shell by running it with `./` e.g. `./test-and-commit.sh`
1. Fail immediately on any error or unset variables
1. Run your tests, and proceed to perform a commit only if tests pass
1. Accept a commit message argument, which is passed from the shell/terminal, when the script is executed
1. Stage all unstaged files, and perform a git commit of those files with the provided commit message

As a stretch goal, the script could also include the following validation check:

1. Script should define a variable as part of the script which is set to the expected path to your project directory.
1. If the directory from which the script is run is not the expected project directory, it should print a message to indicate the directory is wrong, and automatically change to the correct directory before continuing.
