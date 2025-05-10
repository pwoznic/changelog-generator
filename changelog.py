import os
import requests
from collections import defaultdict
from datetime import datetime
import argparse

# Custom environment variable for the token
TOKEN_ENV_VAR = os.getenv("CHANGELOG_TOKEN_ENV", "CHANGELOG_TOKEN")
GITHUB_TOKEN = os.getenv(TOKEN_ENV_VAR) or os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise EnvironmentError(f"{TOKEN_ENV_VAR} or GITHUB_TOKEN environment variable is not set.")

# GitHub Repository (default placeholder)
REPO = os.getenv("CHANGELOG_REPO", "username/repository")

# Label to Section Mapping
LABELS = {
    "New Features": "### ✨ New Features",
    "API Changes": "### 📚 API Changes",
    "Documentation and Feature Enhancements": "### 📝 Documentation Changes",
    "Information Architecture Changes": "### 📝 Documentation Changes",
    "Documentation Fixes": "### 📝 Documentation Changes",
    "Deprecated": "### 🗑 Deprecated",
    "Example Updates": "### 📋 Example Updates",
    "Platform Updates": "### 🛠 Documentation Platform Updates",
    "Skip Changelog": "Skip Changelog",
}

CATEGORY_ORDER = [
    "### ✨ New Features",
    "### 📚 API Changes",
    "### 📝 Documentation Changes",
    "### 📋 Example Updates",
    "### 🗑 Deprecated",
    "### 🛠 Documentation Platform Updates"
]

def fetch_pull_requests(repo, token):
    """Fetch all merged pull requests from the repository."""
    url = f"https://api.github.com/repos/{repo}/pulls"
    headers = {"Authorization": f"token {token}"}
    params = {
        "state": "closed",
        "per_page": 100,
    }
    prs = []
    while url:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        prs.extend(data)
        url = response.links.get('next', {}).get('url')  # Handle pagination
    
    print(f"Fetched {len(prs)} pull requests")
    
    return [pr for pr in prs if pr.get("merged_at")]  # Only merged PRs

def group_prs_by_month_and_label(prs):
    """Group PRs by month and label, consolidating multiple labels only for Documentation Changes."""
    changelog = defaultdict(lambda: defaultdict(list))

    for pr in prs:
        merged_at = datetime.strptime(pr["merged_at"], "%Y-%m-%dT%H:%M:%SZ")
        month_key = merged_at.strftime("%B %Y")
        pr_labels = {label["name"] for label in pr["labels"]}

        # Skip PRs with the "Skip Changelog" label
        if "Skip Changelog" in pr_labels:
            continue

        # Clean PR title
        title_cleaned = pr['title'].split(": ", 1)[-1]

        # Track PRs already added to Documentation Changes to prevent duplicates
        doc_changes_seen = set()

        for label in pr_labels:
            if label in LABELS:
                category = LABELS[label]

                if category == "### 📝 Documentation Changes":
                    # Prevent duplicates in Documentation Changes
                    if title_cleaned not in doc_changes_seen:
                        changelog[month_key][category].append(f"- {title_cleaned} (#{pr['number']})")
                        doc_changes_seen.add(title_cleaned)
                else:
                    # Allow duplicates in other categories
                    changelog[month_key][category].append(f"- {title_cleaned} (#{pr['number']})")

    return changelog

def generate_changelog(changelog):
    header_lines = [
        "# Changelog",
        "",
        "This changelog is auto-generated from merged pull requests.",
        "",
    ]

    lines = header_lines + [""]

    sorted_months = sorted(
        changelog.items(),
        key=lambda x: datetime.strptime(x[0], "%B %Y"),
        reverse=True
    )

    for month, categories in sorted_months:
        if len(lines) > len(header_lines):
            lines.append("")
            lines.append("---")
            lines.append("")

        lines.append(f"## {month}\n")

        seen_categories = set()

        for category in CATEGORY_ORDER:
            if category in categories and category not in seen_categories:
                seen_categories.add(category)

                # Deduplicate PR entries
                seen_prs = set()
                unique_entries = []
                for line in categories[category]:
                    pr_number = line.split("(#")[-1].rstrip(")")
                    if pr_number not in seen_prs:
                        seen_prs.add(pr_number)
                        unique_entries.append(line)

                if unique_entries:
                    lines.append(f"{category}")
                    lines.extend(unique_entries)
                    lines.append("")

        lines.append("")

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Generate a changelog from GitHub PRs.")
    parser.add_argument("--repo", default=REPO, help="GitHub repository (e.g., username/repository)")
    parser.add_argument("--token-env", default=TOKEN_ENV_VAR, help="Environment variable for GitHub token")
    parser.add_argument("--output", default="CHANGELOG.md", help="Output changelog file")
    args = parser.parse_args()

    global GITHUB_TOKEN, REPO, TOKEN_ENV_VAR
    REPO = args.repo
    TOKEN_ENV_VAR = args.token_env
    GITHUB_TOKEN = os.getenv(TOKEN_ENV_VAR) or os.getenv("GITHUB_TOKEN")

    if not GITHUB_TOKEN:
        raise EnvironmentError(f"{TOKEN_ENV_VAR} or GITHUB_TOKEN environment variable is not set.")

    print(f"Fetching pull requests for repository: {REPO}")
    prs = fetch_pull_requests(REPO, GITHUB_TOKEN)
    print(f"Fetched {len(prs)} pull requests.")
    
    changelog = group_prs_by_month_and_label(prs)
    formatted_changelog = generate_changelog(changelog)
    
    with open(args.output, "w") as file:
        file.write(formatted_changelog)
    
    print(f"Changelog generated: {args.output}")

if __name__ == "__main__":
    main()
