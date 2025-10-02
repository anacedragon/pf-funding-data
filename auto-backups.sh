#!/bin/bash

# git backup
git add --all
git commit --message="funds `date`"
git push origin main
