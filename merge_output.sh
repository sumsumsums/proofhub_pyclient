#!bash

# Example usage:
# if you put your output in "output/" directory, and you want to merge all "tasks", use command below.
# ./merge_output.sh -d output -o tasks > tasks.json

while getopts d:o: flag
do
    case "${flag}" in
        d) directory=${OPTARG};;
        o) object=${OPTARG};;
    esac
done

find $directory/ -type f -name "*$object.json" -exec cat {} +