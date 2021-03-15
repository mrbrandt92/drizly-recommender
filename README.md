# drizly-recommender
for take-home interview assignment

## About the Application
This is a simple recommender that takes exactly 1 `user_id_hash` and recommends 4 Drizly products that the user might be interested. The returned products are assigned a "score," which is the cosine similarity between the user's past purchasing habits and some catalog item text features. In order to recommend products most similar to the user's history, the returned dictionary of products is sorted on "score" from highest to lowest (closer to 1 = most similar, closer to 0 = least similar). 

NOTE: This can take 1 and only 1 user id of type string, and this user must be a user from within the original data set provided. The app does not take and store new users, it can only pull from the pre-loaded MySQL database hosted by the author.


## How to Run

1. Ensure you have Docker loaded to your machine and running. Please see [Docker's site](https://docs.docker.com/get-docker/) for more information.
2. Run `git clone https://github.com/mrbrandt92/drizly-recommender`.
3. Once cloned, run `python run_script.py`. This will build and run a Docker image that in turn will serve as a host for the API.
4. Pass in your cURL call - this should look like: `curl -d '{"user_id_hashes":["b9cbac77a336d62efd54404d2bccaecd"]}' -H "Content-Type: application/json" -X POST http://0.0.0.0:8080/invocations`

That's it!
