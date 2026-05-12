### Sample Solution

```bash
#!/bin/bash
set -eu

project_dir="${HOME}/mini-project" # use a value correct for your machine!
current_folder=$(pwd)
commit_message=${1}

# Check current folder matches what we expect
if [[ ${current_folder} != ${project_dir} ]];
then
    echo -e "Not in project directory. Changing directory to ${project_dir}\n"
    cd ${project_dir}
else
    echo "Current folder matches expected"
fi

# Run python unit tests (example for (MacOS / Unix))
if $(python3 -m pytest);
then
    echo "Tests passed, committing..."
    git add .
    git commit -am "${commit_message}"
else
    echo "Tests failed, skipping commit!"
fi
```
