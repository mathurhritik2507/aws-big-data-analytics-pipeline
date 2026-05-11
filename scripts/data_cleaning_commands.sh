#!/bin/bash

# Data cleaning and AWS/EMR command reference.
# Do not commit PEM keys or private AWS credentials to GitHub.

# Remove header row from original CSV before Hive loading.
tail -n +2 2008.csv > 2008_clean.csv

# Example S3 upload command.
aws s3 cp 2008_clean.csv s3://hritik-cs673-project-2008/cs673_project/
aws s3 cp airports.csv s3://hritik-cs673-project-2008/cs673_project/
aws s3 cp carriers.csv s3://hritik-cs673-project-2008/cs673_project/

# SSH into EMR primary node.
chmod 400 /Users/Hritik/Downloads/CS673_AWS_Assignment.pem
ssh -i /Users/Hritik/Downloads/CS673_AWS_Assignment.pem hadoop@<EMR-public-DNS>

# Start Hive.
hive

# Download exported sample file from EMR to local machine.
scp -i /Users/Hritik/Downloads/CS673_AWS_Assignment.pem \
  hadoop@<EMR-public-DNS>:/home/hadoop/hritik_sample_output/hritik_sample_2008.csv \
  ~/Downloads/
