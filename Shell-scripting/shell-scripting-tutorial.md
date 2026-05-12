# Shell Scripting Tutorial

The following tutorial will work through creating three shell scripts which illustrate the value of automation to save time on simple repetitive, but necessary processes.

You may first wish to review the script you created when we first covered Linux LINK_NEEDED

## Create Company Directory Structure

With modern cloud-based solutions new resources are created and destroyed frequently, therefore when new VMs are deployed it can be necessary to configure them each time. This may involve deploying apps (which you've done previously), configuring the OS, or in this case deploying a standard directory structure which aligns with organisational requirements.

```bash
#!/bin/bash

ROOT_DIR="company_demo"

mkdir -p "$ROOT_DIR"/{HR,Finance,IT,Marketing}

mkdir -p "$ROOT_DIR"/IT/{Project_Apollo,Project_Zeus,Project_Orion}

mkdir -p "$ROOT_DIR"/Shared/{Reports,Logs,Archives}

touch "$ROOT_DIR"/HR/employees.txt
touch "$ROOT_DIR"/Finance/budget_2026.xlsx
touch "$ROOT_DIR"/Marketing/campaign_notes.txt

touch "$ROOT_DIR"/IT/Project_Apollo/app.py
touch "$ROOT_DIR"/IT/Project_Zeus/config.yaml
touch "$ROOT_DIR"/IT/Project_Orion/readme.md

touch "$ROOT_DIR"/Shared/Reports/monthly_report.txt
touch "$ROOT_DIR"/Shared/Logs/system.log

echo "Demo company directory structure created successfully."
```

This is a simple script, using commands you should already be familiar with.

- Can you identify what is happening?
- What about the `-p` option?

<details><summary>Reveal</summary>

- `mkdir`: make directory
  - `-p`: create parent directories if they don't exist.
- `touch`: create a new file (or update mod time if exists)
- `echo`: display on stdout.

</details>

Once you've created the files, are there any additional changes you need make in order to execute the script?

<details><summary>Reveal</summary>

`chmod u+x [filename]`

</details>

This example only uses three commands, one option, and several different arguments.

The `ROOT_DIR` variable means that the script could be easily re-used or modified to deploy into a different directory without having to change every line.

### Challenge

Re-write or modify the above script, but try to model a scenario where you need to repeatedly deploy an application.

1. Your script should create an application directory with a suitable name, and three sub-directories called `img`, `data`, and `src`.
2. Add files:

    - `app.py` into `src`
    - `image_1.jpg` into `img`
    - `users.csv` into `data`.

#### Bonus challenge

See if you can figure out how to write your script locally, then transfer it directly to the VM from your host - if you manage it, you could do it for the following scripts too.

<details><summary>Hint:</summary>

scp

</details>

## Log File Aggregation

In the real-world, when troubleshooting, debugging, or simply reviewing activity, you can spend a lot of time working with log files. In this task you create some sample log files, then write a script to consolidate the contents of the files into one place for easier review (rather than manually accessing each individual file).

**Script 1:** Create some sample log files:

```bash
#!/bin/bash

ROOT_DIR="company_demo"

# Create sample log entries
echo "HR system started successfully" > "$ROOT_DIR"/HR/hr.log

echo "Finance database backup completed" > "$ROOT_DIR"/Finance/finance.log

echo "Apollo deployment completed" > "$ROOT_DIR"/IT/Project_Apollo/apollo.log

echo "Sample log files created."
```

Do you recall what `>` does?

<details><summary>Reveal</summary>

**Redirection** - instead of 'echo-ing' to **stdout**, it is redirected to the target file.

</details>

---

**Script 2:** Create the script to consolidate the log files

```bash
#!/bin/bash

ROOT_DIR="company_demo"
OUTPUT_FILE="$ROOT_DIR/Shared/Logs/consolidated.log"

> "$OUTPUT_FILE"

find "$ROOT_DIR" -name "*.log" ! -name "consolidated.log" | while read logfile
do
    echo "===== $logfile =====" >> "$OUTPUT_FILE"
    cat "$logfile" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
done

echo "Logs consolidated into $OUTPUT_FILE"
```

Try figure out what's going on - you know many different commands, and you know the purpose of the script.

<details><summary>Reveal</summary>

After the shebang we define our root directory and output file in variables.
- `> "$OUTPUT_FILE"`
- `find`: Searches for files and directories.
- `-name "*.log"`: Finds all files ending in .log
- `! -name "consolidated.log"`: Excludes the output file from the search.
- `|`: Pipe the previous output into...
- ` while read logfile`
  - `while`: initiate a loop
  - `read`: reads the input from `find` line by line
  - `logfile`: appends to a variable called logfile
- `do...done`: the actions to be completed in the while loop
- `echo "===== $logfile ====="`: This simply echos a string of "=" with the current value of `logfile` embedded (Remember the value is a file name)
- `>> "$OUTPUT_FILE"`: Append the previous string to our output file. NOTE: `>` overwrites, `>>` appends
- `cat "$logfile"`: displays the contents of the current file
- `>> "$OUTPUT_FILE"`: same as previous, appends the output of cat to the output file
- There are a couple of extra echos that should be clear

**Summary**: Find returns the names of log files, each one on a different line, and these results are piped through to `while read`; In the `while` loop, `read` will add the current filename to the `logfile` variable, and the logic in the loop runs i.e. read the contents of the file, and append it to the output file; This repeats for the next log file, until there are none left.
</details>

**Extension Task**: 

Add some additional log files within the file structure, add some text to them, and re-run the script to verify that they're picked up and aggregated.

## Archive Old Project Files

This script compresses project directories into timestamped archive files for backup purposes.

```bash
#!/bin/bash

ROOT_DIR="company_demo"
ARCHIVE_DIR="$ROOT_DIR/Shared/Archives"

# Generate a timestamp
DATE=$(date +%Y-%m-%d)

# Loop through IT projects
for project in "$ROOT_DIR"/IT/*
do
    PROJECT_NAME=$(basename "$project")

    tar -czf "$ARCHIVE_DIR/${PROJECT_NAME}_$DATE.tar.gz" "$project"

    echo "Archived $PROJECT_NAME"
done

echo "All projects archived successfully."
```

What's going on in this script?

<details><summary>Reveal</summary>

After the shebang we define our root directory and the location for our archives to be created.

- `DATE=$(date +%Y-%m-%d)`: DATE is a variable, and it's value is assigned using command substitution. In this case we run the `date` command, and the following values indicate the desired formatting (review `man date` for more options)
  - Command substitution `$( )` runs the command in the brackets first, in this case the output of the `date` command is allocated to the `DATE` variable.
- `for project in "$ROOT_DIR"/IT/*`: initiates a `for` loop over the different directories in `./IT`.
- `do...done`: the actions to be completed in the for loop
- `PROJECT_NAME=$(basename "$project")`: In each loop basename will strip any suffix or prefix from the directory name, and it's assigned to PROJECT_NAME
- `tar -czf "$ARCHIVE_DIR/${PROJECT_NAME}_$DATE.tar.gz" "$project"`: Tar is an archive utility which packages multiple files and directories into one - like a ZIP file. It has various options which you can review on the `man tar` page. The structure of the command is: `tar [options] [new_archive] [existing_files]`.

    In this case we create the file path and name for the archive by combining our different variables `ARCHIVE_DIR`, `PROJECT_NAME`, and `DATE`, then provide the source files for the archive through the `project` variable.

- Again, there are a couple of echo commands to confirm success.

</details>

**Extension Tasks**:

1. Add some additional directories under `./IT/`, add some test files to them, and re-run the script to verify that they're picked up and archived.
2. Try to figure out how to unpack the archives.
