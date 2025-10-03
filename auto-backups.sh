#!/bin/bash

# define variables
home=/home/ubuntu

# copy files from tracker
cp -rup $home/pf-funding-tracker/output/funds* $home/pf-funding-data

# git backup
git add --all
git commit --message="funds `date`"
git push origin main
