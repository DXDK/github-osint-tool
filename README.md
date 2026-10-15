
# GitHub OSINT Tool

A lightweight Python tool for collecting and analyzing publicly available GitHub profile and repository information.

The tool retrieves basic profile details, summarizes public repositories, analyzes primary programming languages, and calculates a simple activity score based on public statistics.

## Features

- Retrieve public GitHub profile information.
- List public repositories, including repository URLs, stars, and forks.
- Fetch repositories across multiple API pages.
- Summarize repository primary languages.
- Calculate an experimental activity score using public profile statistics.
- Handle common HTTP errors, request timeouts, and invalid responses.
- Validate GitHub usernames before making API requests.

## Requirements

- Python 3.9 or later
- Internet connection
- `requests` library

## Installation

Clone the repository:

```bash
git clone https://github.com/DXDK/github-osint-tool.git
cd github-osint-tool
```

Install the required dependency:

```bash
python -m pip install requests
```

## Usage

Run the script:

```bash
python github_osint.py
```

Enter a GitHub username when prompted.

Example:

```text
Enter GitHub username: torvalds
```

The tool will display available public profile details, repository statistics, language distribution, and the experimental activity score.

## How the Activity Score Works

The score is calculated from four public statistics:

| Factor | Maximum Points |
|---|---:|
| Public repository count | 30 |
| Followers | 20 |
| Total repository stars | 30 |
| Primary language diversity | 20 |
| **Total** | **100** |

The score is an experimental summary of public activity. It does not measure a developer's technical skill, reputation, trustworthiness, or security expertise.

## Limitations

- Uses GitHub's public REST API without authentication.
- Subject to GitHub API rate limits.
- Analyzes primary repository languages rather than detailed language usage.
- Uses public statistics only; it does not access private repositories.
- The activity score is a simple heuristic, not a validated assessment model.

## Error Handling

The tool handles common situations such as:

- Invalid username formats
- Missing users or resources
- Network errors and request timeouts
- GitHub API rate limits
- Unexpected or invalid API responses

## Disclaimer

This project is intended for educational purposes and for analyzing publicly available GitHub information. Use it responsibly and respect applicable terms of service and privacy expectations.

## Author

**Abdullah Kamal (DXDK)**

GitHub: [@DXDK](https://github.com/DXDK)

---

Built as a hands-on Python project to practice API requests, data processing, input validation, and basic OSINT workflows.
