import json

import requests


def read_bing_key():
	bing_api_key = None

	try:
		with open("bing.key", "r") as file:
			bing_api_key = file.readline()
	except:
		raise IOError("bing.key file not found")

	return bing_api_key


def run_query(search_terms):
	bing_api_key=read_bing_key()

	if not bing_api_key:
		raise KeyError("Bing Key Not Found")

	root_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
	
	params = {

		"q": search_terms,
		"count":15,
		"offset":0,
		"mkt":"en-US"
	}
	headers = {"Ocp-Apim-Subscription-Key": bing_api_key}
	response = requests.get(root_url, params=params, headers=headers)
	print(f"url: {response.request.url}")
	response = json.loads(response.content)

	return response


def main():
	user_input = input("Enter your query: ")
	run_query(user_input)


if __name__ == "__main__" :
	main()