from apify_client import ApifyClient

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_wjt7aOzxFZu7Ca4aVaYr2z4m6iX1rg0A0qfF")

# Prepare the actor input
run_input = {
    "handle": ["narendramodi"],
    "mode": "own",
    "tweetsDesired": 10,
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

# Fetch and print actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item["full_text"])
