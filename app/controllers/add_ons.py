import requests


def get_random_joke(category="Any"):
    url = f"https://v2.jokeapi.dev/joke/{category}?blacklistFlags=nsfw,religious"
    response = requests.get(url)
    joke_data = response.json()

    if joke_data["error"]:
        return "Error fetching joke."

    if joke_data["type"] == "single":
        return joke_data["joke"]
    elif joke_data["type"] == "twopart":
        return f"{joke_data['setup']} - {joke_data['delivery']}"


# Example usage
print(get_random_joke())
