# Time analysis for first approved review of merged pull requests
File: pr_review_time_analysis.py

Purpose of this script is to extract last N merged from the organization and repo and find out the first approved reviewer for each of that request.
This is followed by finding the time taken for that first approved review and plot the histrgram of all N timings in 3 buckets: less than 1 hour, between 1 hour and 1 day, more than 1 day.
Save the ouptput in encoded json file as output.json 
