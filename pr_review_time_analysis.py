import requests
import datetime
import matplotlib.pyplot as plt
import numpy as np
import json
import sys

# Main class with the entry point to the script accepting 2 arguments
# For a provided Github organisation and repository (default nodejs/node)
# will produce histogram data for the time that it took the last N (default 10) merged pull requests
# to receive their first approved review, with the buckets: less than 1 hour, between 1 hour and 1 day, more than 1 day.
# Print result as JSON string
# @arg1 - organization/repo into which to search for merged pull requests
# @arg2 - N specifies number of merged pull requests to retrieve
if __name__ == "__main__":
    org_repo = "nodejs/node"        # default
    N = 10                          # default

    if len(sys.argv) > 1:
        arg1 = sys.argv[1]
        if arg1 != "":
            org_repo = arg1
            arg2 = sys.argv[2]
            if arg2 != "":
                N = int(arg2)

    page_no = 0                     # counter to search merged pull request in particular page
    last_n_merged_requests = []     # This will store the retrieved merged pull requests

    # Optional header to provide auth token to prevent exceeding GIT request limit
    # Add this as argument to each request if required
    headers = {
        'Authorization': 'token <OAuthToken>',
    }

    # Keep searching in pages until we've retrieved N merged pull requests or no further data exist
    while len(last_n_merged_requests) != N:
        page_no += 1

        # Retrieve pull requests that are in 'closed' state with '100' requests per page on specified page number
        params = {'state': 'closed', 'per_page': '100', 'page': page_no, 'accept': 'application/vnd.github.v3+json'}

        url = 'https://api.github.com/repos/' + org_repo + '/pulls'
        response = requests.get(url, params=params)
        print(response)
        if response.status_code == 200:
            closed_pull_requests = response.json()
        else:
            break

        # Search for merged ones in all closed pull requests
        for req in closed_pull_requests:
            if req['merged_at'] is not None:
                last_n_merged_requests.append(req)          # Add to our list if the request is merged
                if len(last_n_merged_requests) == N:        # Finish searching if N requests are retrieved
                    break

    review_times = []                   # Store the time taken for first review of each merged pull request
    one_hour_threshold = 60 * 60        # seconds in one hour
    one_day_threshold = 60 * 60 * 24    # seconds in one day

    output = []                         # Store the output that will be dumped to json encoded string

    # Loop through all retrieved merged pull requests and get their first approved review
    # Calculate the time taken between pull request creation time and review submission time
    for req in last_n_merged_requests:
        req_number = req['number']
        creation_time = req['created_at']
        url = 'https://api.github.com/repos/nodejs/node/pulls/' + str(req_number) + '/reviews'

        # Retrieve only first review of this request
        params = {'per_page': '1', 'page': '1', 'accept': 'application/vnd.github.v3+json'}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            review_request = response.json()
            first_review_time = review_request[0]['submitted_at']

            # Parse time values and calculate required time taken
            time_taken = datetime.datetime.strptime(
                first_review_time, "%Y-%m-%dT%H:%M:%SZ"
            ).timestamp() - datetime.datetime.strptime(
                creation_time, "%Y-%m-%dT%H:%M:%SZ"
            ).timestamp()

            # Store time in all timings for the generation of histogram
            review_times.append(int(time_taken))

            # Add tuple of request url, review url and time taken to output
            output.append({"pull_request_url": req['url'], "first_review_url": review_request[0]['html_url'], "time_taken": str(int(time_taken))})
        else:
            break

    # Generate json encoded string of output and print it
    output_json = json.dumps(output)
    with open('output.json', 'w') as outfile:
        json.dump(output, outfile)
    print(output_json)

    # Generate histogram by putting various timings in given buckets
    ylabel = "Number of requests (Total = " + str(N) + ")"
    fig, ax = plt.subplots()
    n_bins = [0, one_hour_threshold, one_day_threshold, max(review_times)]
    hist, bin_edges = np.histogram(review_times, n_bins)
    ax.bar(range(len(hist)), hist, align='edge', width=1, tick_label=["0", "1 hour", "1 day"])
    plt.xlabel("Time taken for first approved review")
    plt.ylabel(ylabel)
    plt.show()
