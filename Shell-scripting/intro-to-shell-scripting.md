# Intro to Shell Scripting

Shell scripts are a powerful automation tool in Linux environments, allowing us to write our shell commands in a text file, and have them executed automatically.

## Linux Recap

You've now spent a good few weeks working with Linux, hopefully to a point where some of the basic commands and actions are becoming familiar.

But just in case, let's briefly recap...

### Linux Commands

Which commands can you recall?

<details>
<summary>Reveal</summary>Examples could be:

- `mkdir`: make directory
- `ls`: list contents of directory
- `cd`: change directory
- `pwd`: present working directory
- `mv`: move (also rename)
- `cp`: copy
- `rm`: remove (delete) file
- `rmdir`: remove directory
- `touch`: create file (update last mod' time)
- `man`: view the manual for a command
- `nano`: open the nano text editor (if installed)
  - `CTRL+O`: save file
  - `CTRL+X`: exit nano
- `chmod`: change access modes (permissions)
- `cat`: view the contents of a file (or concatenate)
- `sudo`: run command as root
- `dnf`/`yum`: manage packages
- `grep`: search for text strings (global regex print)

</details>

You have used all of these commands and more previously, but some of them perhaps only once or twice. Don't worry, nobody remembers every Linux command.

We previously discussed the structure of Linux commands:

|Command|Options|Arguments|
|---|---|---|
|The command you want to run|Modifiers which affect the behaviour/output|The object you want the command to act against|
|`ls`: the list command|`-al`: all files (*includes hidden*), long list format|`/etc` at this location|

Options and arguments are sometimes required, for example you can't add a new user without providing a username, but they're often optional.

### The Linux Filesystem

**Linux uses a single-root filesystem** - In Windows you are likely familiar with each storage device on your system having a drive letter assignment, typically the disk on which Windows is installed is assigned `c:`, subsequent ones are `d:`, `e:`, and so on. Each of these storage disks then has it's own filesystem of directories and files which you can navigate around, and move from one drive to another.

Linux is different, it has a filesystem which unifies everything under one structure, including multiple storage devices if attached. The very top of the structure is called **root**, and is represented by `/`.

>If you need a deeper revisit [here is our previous](https://github.com/Generation-UK-I/DE-NAT4-TECH-CONTENT/blob/main/Linux-Docker/Linux-filesystem.md) Linux filesystem module.

### Absolute and Relative Paths

- **Relative paths** define the location to a resource from the current location.
- **Absolute paths** define the location to a resource from the root of a filesystem.

```text
# Relative path
my_project/my_file

# Absolute path
/home/centos/my_project/my_file


# |-------absolute-path---------|
#             |--relative-path--|
# /home/centos/my_project/my_file
```

Use relative paths when you want to point to resources within a directory, but the entire directory may need to be moved, for example to share or collaborate; In these cases the absolute path may differ from system to system.

>Absolute paths may be suitable in sceanrios where you're making a resource which will be duplicated exactly, such as VMs or containers.

### Users, Groups, and Permissions

In Linux we primary consider three types of account:

- **Standard user accounts** are created and allocated to human users who require access to the system.
- **System accounts** which are used by applications and services to carry out their operations.
- **Root user account** is the most powerful account on the system, it can carry out any action on the system, and cannot easily be restricted. **It should be used with caution**.

Every file in Linux has an owner, and belongs to a group. We can assign permissions to these files defining who can access what.

We have three available permissions (known as modes):

- `r`: read
- `w`: write
- `x`: execute

Each file has three categories of user:

- `u`: the owner of the file
- `g`: users who are in the same group as the file
- `o`: other users not in the previous categories

We can manage permissions in two ways:

#### Symbolic mode

Symbolic mode allows you to use the above characters, along with `+`, `-`, and `=` to change the permissions on a file with the `chmod` command:

```bash
chmod u+x my_file
chmod g-w my_file
```

#### Absolute mode

When using absolute mode each type of user: **owner**, **group**, and **other**, is represented by 3 bits of binary, which in turn align with the three available permissions: `r`, `w`, `x`.

We then set each binary bit according to our desired permission set, and convert the resulting binary to octal, giving us 3 numbers between 0 and 7.

```bash
chmod 777 my_file # Gives U/G/O full permissions to a file - DON'T DO THIS
chmod 644 my_file # U=RW; G=R; O=R; These are the default permissions for a new file
```

>If you need a deeper revisit [here is our previous](https://github.com/Generation-UK-I/DE-NAT4-TECH-CONTENT/blob/main/Linux-Docker/users-groups-permissions.md) Linux users, groups, and permissions module.

## The Linux Shell

The Shell is the application which receives the commands from the user, and passes them through to the kernel. The Shell is displayed through the standard out, which for a local machine would be the monitor; when connecting to a remote machine `stdout` is typically an SSH terminal.

In addition to passing commands to the kernel, and returning output, the Shell also provides lots of functionality to facilitate complex multi-step operations to be performed with your Linux commands, such as `find`, `grep` and `pipe` (`|`).

>If you need a deeper revisit of the Linux shell and the additional features [here is our previous](https://github.com/Generation-UK-I/DE-NAT4-TECH-CONTENT/blob/main/Linux-Docker/introduction-linux.md) introduction to Linux module.

## Shell Scripting

A script is simply a text file, which contains commands which will be executed automatically, following the order or logic you define. We've created plenty of Python scripts, defining variables, loops, operators, outputs, etc.

Generally, almost anything we could do with manual commands on the command line can be made into a script.

In Linux the most common Shell is called Bash, when we write scripts for this Shell we call them Bash scripts.

In the introduction to Linux module you created a Bash script to automatically configure a web server on your VM, revisit it if needed; We're now going to dissect and explore Bash scripts in greater depth.

### Advantages of Shell Scripts

Why don't we just write a program in Python, or Java, or something else?

- Unix shell is available anywhere, on any Linux machine
- No dependencies required, so we know our scripts are always going to work
- Allows us to use all the powerful tools and commands that are available in Unix
- Almost anything we can do with manual commands on the command line we can do in a script

Shell scripts are often used for basic tasks where writing a full app may be overkill

They may also be used to do things like set up the dependencies and environment required by a more complex app to allow that app to then run

### Example of a Shell Script

```sh
#!/bin/bash
set -eu

timeout=120
retry_delay=1

query_with_timeout () {
    echo "Triggering with timeout"
    curl --retry $timeout --retry-connrefused --retry-delay $retry_delay 'google.com' &> /dev/null
}

print_online () {
    echo "we're online!"
}

query_with_timeout && print_online
```

What do you think is happening?

Focus on the parts of the script you CAN understand then try to GUESS based on observation and intuition what this script is doing.

As engineers, our problem-solving approach should first be to focus on the parts we understand, rather than being intimidated and overwhelmed by the parts we do not.

>`/dev/null` is a void where the output will just disappear, good for capturing unwanted output without showing it on the screen.

### How to write shell scripts

We can save our script commands to a file, and run it from the ba**sh** shell.

To run a script you must have the execution permissions set.

```sh
chmod +x script.sh
```

A script can be run by using `./` in front of the filename in your shell terminal, if you're in the same directory as the script - *Remember `.` is an alias for the current directory*.

```sh
./script.sh
```

The `sh` file extension indicates a **Sh**ell script

#### Shebang

You will often see `#!/bin/bash` or `#!/usr/bin/bash` at the start of shell scripts.

This is the **Shebang** - It tells the shell what interpreter to run the script with. With it we can run scripts with `./my_script.sh`.

>Without the shebang we can run our scripts explicitly with bash e.g. `bash my_script.sh`, just like running Python scripts from the terminal by prefixing the the filename with `python` or `python3`.

The shebang is always on the first line

#### Double vs Single Quotes

Strings wrapped in single quotes are used exactly as they appear by the shell.

String wrapped in double quotes will have variable names replaced with the value of that variable.

```sh
#!/bin/bash
set -eu

name="John"
echo "Hi $name"  #=> Hi John
echo 'Hi $name'  #=> Hi $name
```

## Parts of a Script

### Options

Options control how the shell will run the script. They can be set by using `set` in your script. Common options you might use include:

- `-e`: Exit immediately if a command fails
  - **It's best practice to always fail a script the moment a command fails**
- `-u`: Treat unset variables and parameters as an error

### Variables

Similar to variables in Python, they have a name and can be given a value with `=`; Do not leave any whitespace around the `=` because Bash will try to treat the name and value as separate commands.

```sh
timeout=120
```

Reference a variable by using `$` in front of the variable name

```sh
$<variable_name>
```

Variables inside a script should have lowercase names (*to avoid accidentally overwriting **global** or **environment** variables*)

### Comments

Anything on a line after `#` will be commented out.

**Don't forget to comment your scripts.** It's good practice to write what the script does at the top after the shebang.

Try to include a help command, and explain how to invoke the script by giving an example

Comments `#` are different from the shebang `#!`

### Arguments

Values can be passed into scripts from outside the script with the use of arguments.

Arguments are assigned an index number (1, 2, 3...) based on the order they appear.

Arguments can be accessed by using that index number after a `$`

```sh
$<index of argument>
```

**Arguments Example**:

Create the script

```py
#!/bin/bash
set -eu

name=${1}
echo "Hi $name"
```

Invoke the script with an argument:

```sh
./say-hi.sh "Jane Doe"
```

Expected output:

```sh
Hi Jane Doe
```

### Environment Variables

Environment variables are a different type of variable that is **inherited** inside a script from the outside **environment** in which that script runs.

>You may have used environment variables already with Python: When connecting to a DB the connection details and credentials were declared as environment variables, then imported into our app.

We do not need to explicitly pass environment variables into a script like arguments, they are available automatically. Unlike Python, which requires an external library (`dotenv`) to achieve the same thing.

Environment variables are created by various sources:

- The operating system itself
- Your `~/.bashrc` or `~/.zshrc` where custom environment variables are set
- Other scripts or programs which may set new environment variables

Some examples of environment variable include:

- `$SHELL` - What shell you are using.
- `$USER` - Who you're logged in as.
- `$HOME` - Path to your home directory.
- `$TEMP` - Path to a suitable directory to write temporary files.

Environment variables are **UPPERCASE**

You can see other environment variables by using the `env` command.

You should not change the value of existing environment variables (without good reason) because it might break things that depend on those values.

### Conditionals

Similar behaviour to Python, just different syntax.

The `if` condition is inside square brackets `[[ ]]` and must evaluate to `true` or `false`.

An `if` condition is ended by `fi` (if backwards):

```sh
#!/bin/bash
set -eu

echo -n "Enter a number: "
read var

if [[ $var -gt 10 ]]
then
    echo "The variable is greater than 10."
fi
```

#### Conditional Operator Examples

Numerical Conditional operators:

- `-gt` : Greater than
- `-ge` : Greater than or equal
- `-eq` : Equals
- `-ne` : Not Equal
- `-lt` : Less than
- `-le` : Less than or equal

String Conditional operators:

- `=` or `==` : Strings are equal
- `!=` : Strings are not equal
- `-z` : String has zero length
- `-n` or no operator : String has non-zero length

File Conditional operators:

- `-e` or `-a` : File exists
- `-f` : File exists and is regular file
- `-d` : File exists and is directory
- `-s` : File exists and is not empty
- `-r` : File is readable
- `-w` : File is writable
- `-x` : File is executable

```sh
if [[ -f "$filename" ]]; 
then
    echo "$filename exists!"
fi
```

### Else Conditionals

```sh
#!/bin/bash
set -eu

echo -n "Enter a number: "
read var

if [[ $var -gt 10 ]]
then
    echo "The variable is greater than 10."
else
    echo "The variable is equal to or less than 10"
fi
```

Like in Python, we can add more 'else-if' conditions to our chain of conditional checks.

```sh
#!/bin/bash
set -eu

echo -n "Enter a number: "
read var

if [[ $var -gt 10 ]]
then
    echo "The variable is greater than 10."
elif [[ $var -eq 10 ]]
then
    echo "The variable is 10."
else
    echo "The variable is less than 10"
fi
```

### For Loop

Can be defined as specific values or as a range.

```sh
#!/bin/bash
set -eu

for i in {1..5};
do
    echo "Welcome ${i}"
done
```

Must include a **done** to denote when the loop ends.

For loop Example:

```sh
#!/bin/bash
set -eu

reposPath="/home/linus/myrepos"
for repoDir in $(ls -d ${reposPath}/*/)
do
    cd ${repoDir}
    git pull
    cd ../
done
```

This example is complex but people do this; What do you think it is doing?

<details><summary>Reveal</summary>
Switch into every git repo directory under a path, pull the latest changes, then switch back to the parent directory to repeat the process

How long could this take if you had a dozen repos to pull manually?
</details>

### While Loop

Much like python, will loop until condition evaluates to false.

While loop Example:

```sh
#!/bin/bash
set -eu

urlsFile=${1}
while IFS= read -r url
do
    echo -e "\n\n...CHECKING ${url} IS UP...\n\n"
    ping -c 3 ${url}
done < "${urlsFile}"
```

This example is complex but people do this; What do you think it is doing?

<details><summary>Reveal</summary>
Read a list of URLs from an input file, for each URL ping the url to check it is working

How long could this take if you had a dozen repos to pull manually?
</details>

### Substitution

We can substitute function output for variables.

Any output value produced by a function inside an execution block `$( )` can be used as if it were a variable:

```sh
#!/bin/bash
set -eu

old_text="I love python"

echo $( echo $old_text | sed 's/python/bash/' )
```

What do you think is happening here?

<details><summary>Reveal</summary>

`sed s/python/bash` replaces "python" with "bash" in the input it is given, which is piped in from the echo command.

</details>

The important bit is noticing the execution block.

### Exit codes

When any Unix application finishes running, it returns an `exit code`.

There are many exit codes, but 0 means success, and any other code (e.g. 1, 2, 3) is an error.

In `if` conditions, the exit code 0 evaluates to `true`, anything else is considered `false`:

```sh
#!/bin/bash
set -eu
if ! which python3;
then
    apt-get install python3
fi
```

## Exercises

Follow scripting practical tutorial
