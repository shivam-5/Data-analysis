# Time analysis for first approved review of last N merged pull requests
File: pr_review_time_analysis.py

Purpose of this script is to extract last N merged from the organization and repo and find out the first approved reviewer for each of that request.
This is followed by finding the time taken for that first approved review and plot the histrgram of all N timings in 3 buckets: less than 1 hour, between 1 hour and 1 day, more than 1 day.
Save the output in encoded json file as output.json 

Script was written in python 3.8 environment with following dependency installations might be required: "matplotlib" and "requests"

Run the script in command prompt with following command: python pr_review_time_analysis.py nodejs/node 10

First argument nodejs/node specifies the organization and repository to retrieve the request from.
Second argument 10 specifies the number of requests to analyze the data from.

Note: It would be better if either both arguments are specified or none. 
Documentation is provided inline in code
