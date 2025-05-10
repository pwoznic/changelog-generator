# Changelog Generator

A Python script to generate a changelog from merged GitHub pull requests based on labels. It organizes changes into categories like New Features, API Changes, and Documentation Changes, and outputs a Markdown file suitable for documentation.

## Features
- Fetches merged pull requests from a specified GitHub repository.
- Groups PRs by month and label, with deduplication for Documentation Changes.
- Supports categories: New Features, API Changes, Documentation Changes, Example Updates, Deprecated, and Documentation Platform Updates.
- Configurable via command-line arguments or environment variables.
- Outputs a clean Markdown changelog with a customizable header.

## Prerequisites
- Python 3.6+
- A GitHub Personal Access Token with `repo` scope.
- The `requests` library (`pip install requests`).

## Installation
1. Clone or download this repository:
   ```bash
   git clone https://github.com/username/changelog-generator.git
   cd changelog-generator
2. Install the required dependency:
   ```bash
   pip install requests

# Usage

## Running Locally
1. Set your GitHub token as an environment variable:
   ```bash
   export GITHUB_TOKEN="your-personal-access-token"
2. Run the script, specifying your repository:
   ```bash
   python changelog.py --repo "username/repository" --output CHANGELOG.md

Alternatively, use environment variables for configuration:

```bash
export CHANGELOG_REPO="username/repository"
export CHANGELOG_TOKEN="your-personal-access-token"
python changelog.py
```

## Command-Line Options

* `--repo`: GitHub repository (e.g., `username/repository`). Default: `username/repository` or `CHANGELOG_REPO` env variable.
* `--token-env`: Environment variable name for the GitHub token. Default: `CHANGELOG_TOKEN` or `GITHUB_TOKEN`.
* `--output`: Output file for the changelog. Default: `CHANGELOG.md`.

Example with custom token variable:

```bash
python changelog.py --repo "username/repository" --token-env MY_TOKEN --output my-changelog.md
```

## Output

The script generates a `CHANGELOG.md` file (or your specified output file) with the following structure:

# Changelog

This changelog is auto-generated from merged pull requests.

## May 2025

### ✨ New Features
- Added new feature X (#123)

### 📝 Documentation Changes
- Updated guide Y (#124)

---
## April 2025

### 🗑 Deprecated
- Removed deprecated endpoint Z (#125)

# Customization

To use different labels or categories, edit the LABELS and CATEGORY_ORDER variables in changelog.py. The default configuration supports:

* **Labels and Categories:**
  * New Features → ### ✨ New Features
  * API Changes → ### 📚 API Changes
  * Documentation and Feature Enhancements, Information Architecture Changes, Documentation Fixes → ### 📝 Documentation Changes
  * Example Updates → ### 📋 Example Updates
  * Deprecated → ### 🗑 Deprecated
  * Platform Updates → ### 🛠 Documentation Platform Updates
  * Skip Changelog: Skips PRs with this label.
* **Category Order:**
  * Categories appear in the order defined in `CATEGORY_ORDER`.
  * Group categories together if you have many labels and you want to consolidate.

Modify these in the script to match your repository’s labels.

### Notes
* Ensure your GitHub token has repo scope to access pull request data.
* The script deduplicates PRs under Documentation Changes to avoid repetition when multiple labels apply.
* PRs with the Skip Changelog label are excluded from the output.

### License

MIT License (see `LICENSE` file for details).
