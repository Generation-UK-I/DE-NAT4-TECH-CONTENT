# Bash Scripting

## Bash variables

```sh
#!/bin/bash -eu
name="John"
echo "Hi $name"
echo 'Hi $name'
```

## Substitution and capturing outputs

```sh
#!/bin/bash
set -eu

old_text="I love python"

# Run other commands in an execution block "$(....)"
new_text=$( echo ${old_text} | sed 's/python/bash/' )

echo ${new_text}
```

## Bash conditionals

```sh
#!/bin/bash -eu

echo -n "Enter a number: "
read var

if [[ $var -gt 10 ]]
then
  echo "The variable is greater than 10."
else
  echo "The variable is equal to or less than 10"
fi
```

## Bash for loops

```sh
#!/bin/bash -eu
for i in 1 2 3 4 5
do
   echo "Welcome $i times"
done
for i in {1..5}
do
   echo "Goodbye $i times"
done
```

### Other For loop example

```sh
#!/bin/bash 
set -eu

foldersPath="."
echo "You are here: $(pwd)"

for folder in $(ls -d ${foldersPath}/*/)
do
    echo "...Child folder=${folder}"
    echo "...Child folder '${folder}' contains:"
    ls -la ${folder}
done

echo "Done!"
```

## Bash while loop

```sh
#!/bin/bash -eu
c=1
while [ $c -le 5 ]
do
    echo "Welcome $c times"
    (( c++ ))
done
```
