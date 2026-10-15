
import re
import requests

BASE_URL = "https://api.github.com"
TIMEOUT = (3.05, 10)
PER_PAGE = 100


def valid_username(username):
    if len(username) > 39:
        return False

    return re.fullmatch(
        r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*",
        username
    ) is not None


def fetch_json(url, params=None):
    try:
        response = requests.get(
            url,
            params=params,
            timeout=TIMEOUT,
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"
            }
        )
    except requests.exceptions.Timeout:
        print("Request timed out. Check your connection and try again.")
        return None
    except requests.exceptions.RequestException as error:
        print(f"Network error: {error}")
        return None

    if response.status_code == 404:
        print("The requested GitHub resource was not found.")
        return None

    if response.status_code in (403, 429):
        remaining = response.headers.get("X-RateLimit-Remaining")

        if remaining == "0":
            print("GitHub API rate limit reached. Try again later.")
        else:
            print("GitHub rejected the request. Check the API response.")
        return None

    if not response.ok:
        print(f"GitHub API returned HTTP {response.status_code}.")
        return None

    try:
        return response.json()
    except ValueError:
        print("GitHub returned an invalid JSON response.")
        return None


def get_user(username):
    url = f"{BASE_URL}/users/{username}"
    return fetch_json(url)


def get_repos(username):
    url = f"{BASE_URL}/users/{username}/repos"
    repos = []
    page = 1

    while True:
        params = {
            "per_page": PER_PAGE,
            "page": page
        }

        page_repos = fetch_json(url, params=params)

        if page_repos is None:
            return None

        if not isinstance(page_repos, list):
            print("Unexpected response while fetching repositories.")
            return None

        repos.extend(page_repos)

        if len(page_repos) < PER_PAGE:
            break

        page += 1

    return repos


def print_profile(data):
    print("\n=== GitHub Profile ===")
    print("Name:", data.get("name") or "Not provided")
    print("Username:", data.get("login"))
    print("Bio:", data.get("bio") or "Not provided")
    print("Location:", data.get("location") or "Not provided")
    print("Public Repositories:", data.get("public_repos", 0))
    print("Followers:", data.get("followers", 0))
    print("Following:", data.get("following", 0))
    print("Account Created:", data.get("created_at"))
    print("Profile URL:", data.get("html_url"))


def analyze_repos(repos):
    print("\n=== Repository Analysis ===")

    languages = {}
    total_stars = 0
    total_forks = 0

    if not repos:
        print("No public repositories found.")
        return languages, total_stars, total_forks

    for repo in repos:
        name = repo.get("name", "Unknown")
        stars = repo.get("stargazers_count") or 0
        forks = repo.get("forks_count") or 0
        language = repo.get("language")

        print(f"\nRepository: {name}")
        print("URL:", repo.get("html_url"))
        print("Stars:", stars)
        print("Forks:", forks)
        print("Primary Language:", language or "Not specified")

        total_stars += stars
        total_forks += forks

        if language:
            languages[language] = languages.get(language, 0) + 1

    print("\n=== Primary Language Distribution ===")

    if languages:
        for language, count in sorted(
            languages.items(),
            key=lambda item: item[1],
            reverse=True
        ):
            print(f"{language}: {count} repositories")
    else:
        print("No primary languages reported.")

    print("\nTotal Stars:", total_stars)
    print("Total Forks:", total_forks)

    return languages, total_stars, total_forks


def calculate_score(user_data, repos, total_stars, languages):
    # This is an experimental activity score, not a measure of skill.
    score = 0

    public_repos = user_data.get("public_repos") or 0
    followers = user_data.get("followers") or 0

    score += min(public_repos * 5, 30)
    score += min(followers * 10, 20)
    score += min(total_stars * 2, 30)
    score += min(len(languages) * 10, 20)

    return min(score, 100)


def main():
    username = input("Enter GitHub username: ").strip()

    if not valid_username(username):
        print("Invalid username format.")
        return

    print("\nFetching GitHub profile...")

    user_data = get_user(username)

    if user_data is None:
        return

    if not isinstance(user_data, dict):
        print("Unexpected response while fetching the profile.")
        return

    print_profile(user_data)

    print("\nFetching public repositories...")

    repos = get_repos(username)

    if repos is None:
        print("Could not complete repository analysis.")
        return

    languages, total_stars, total_forks = analyze_repos(repos)

    score = calculate_score(
        user_data,
        repos,
        total_stars,
        languages
    )

    print("\n=== Experimental Activity Score ===")
    print(f"Score: {score}/100")
    print("This score reflects simple profile statistics only.")
    print("It does not measure trustworthiness or cybersecurity skill.")


if __name__ == "__main__":
    main()
