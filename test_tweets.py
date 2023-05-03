from apify_client import ApifyClient

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_wjt7aOzxFZu7Ca4aVaYr2z4m6iX1rg0A0qfF")

# Prompt the user for input
handle = input("Enter a Twitter handle to scrape: ")

# Prepare the actor input with user-provided handle
run_input = {
    "handle": [handle],
    "mode": "own",
    "tweetsDesired": 5,
    "searchMode": "top",
    "profilesDesired": 1,
    "relativeToDate": "",
    "relativeFromDate": "",
    "proxyConfig": {"useApifyProxy": True},
    "extendOutputFunction": """async ({ data, item, page, request, customData, Apify }) => {
  return item;
}""",
    "extendScraperFunction": """async ({ page, request, addSearch, addProfile, _, addThread, addEvent, customData, Apify, signal, label }) => {

}""",
    "customData": {},
    "handlePageTimeoutSecs": 500,
    "maxRequestRetries": 6,
    "maxIdleTimeoutSecs": 60,
}

# Run the actor and wait for it to finish
run = client.actor("quacker/twitter-scraper").call(run_input=run_input)
tweets = ''

# Fetch and concatenate actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    tweets += str(item["full_text"])

# Print the final concatenated string
print(tweets)
