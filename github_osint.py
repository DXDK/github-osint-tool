import requests

BASE_URL = "https://api.github.com/users/"


def get_user(username):
    url = BASE_URL + username
    r = requests.get(url)

    if r.status_code != 200:
        print("User not found or API limit reached")
        return None

    return r.json()


def get_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    r = requests.get(url)

    if r.status_code != 200:
        print("Failed to fetch repositories")
        return []

    return r.json()


def print_profile(data):
    print("\n=== GitHub Profile Intel ===")
    print("Name:", data.get("name"))
    print("Username:", data.get("login"))
    print("Bio:", data.get("bio"))
    print("Location:", data.get("location"))
    print("Public Repos:", data.get("public_repos"))
    print("Followers:", data.get("followers"))
    print("Following:", data.get("following"))
    print("Account Created:", data.get("created_at"))
    print("Profile URL:", data.get("html_url"))


def analyze_repos(repos):
    print("\n=== Repositories Analysis ===")

    languages = {}

    for repo in repos:
        print("\nRepo Name:", repo.get("name"))
        print("Stars:", repo.get("stargazers_count"))
        print("Forks:", repo.get("forks_count"))
        print("Language:", repo.get("language"))

        lang = repo.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1

    print("\n=== Language Distribution ===")
    for lang, count in languages.items():
        print(f"{lang}: {count}")


def calculate_score(user_data, repos):
    score = 0

    # repos factor
    score += min(user_data.get("public_repos", 0) * 5, 30)

    # followers factor
    score += min(user_data.get("followers", 0) * 10, 20)

    # repo stars
    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
    score += min(total_stars * 2, 30)

    # language diversity
    languages = set(repo.get("language") for repo in repos if repo.get("language"))
    score += min(len(languages) * 10, 20)

    return min(score, 100)


def main():
    username = input("Enter GitHub username: ")

    data = get_user(username)

    if data:
        print_profile(data)

        repos = get_repos(username)
        analyze_repos(repos)

        score = calculate_score(data, repos)

        print("\n=== OSINT Intelligence Score ===")
        print("Score:", score, "/100")


if __name__ == "__main__":
    main()
