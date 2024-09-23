# R1 Universities with RSE Groups
[![Run and deploy](https://github.com/Sbozzolo/has_rse/actions/workflows/deploy.yml/badge.svg)](https://github.com/Sbozzolo/has_rse/actions/workflows/deploy.yml)
[![Here](https://img.shields.io/badge/list_is_here-click_me!-blue.svg)](https://sbozzolo.github.io/has_rse)

This repository automatically generates a list of R1 universities in the US that appear to have Research Software Engineering (RSE) groups based on web searches. The list is updated weekly and deployed to GitHub Pages. You can access the live list [here](https://gbozzola.github.io/has_rse/).

## How it Works

The process involves the following steps:

1. **Data Collection:**
   - We start with a list of R1 universities from the Carnegie Classification of Institutions of Higher Education.
   - For each university, we perform a web search using DuckDuckGo, focusing on terms related to "research software engineering".
   - We filter the search results to include only those from `.edu` domains.

2. **RSE Group Identification:**
   - We analyze the search results for keywords that suggest the presence of an RSE group (e.g., "research software engineer", "RSE team", "RSE group").
   - If a search result contains relevant keywords, we mark the university as potentially having an RSE group.
   - We also maintain a list of known RSE groups and blacklisted URLs to improve accuracy.

3. **Output Generation:**
   - The results are compiled into a JSON file (`universities.json`) containing university names, whether they appear to have an RSE group, and a link to a relevant webpage (if found).
   - An HTML page (`index.html`) is generated from the JSON data, providing a user-friendly table with the results.

4. **Deployment:**
   - The generated files are automatically deployed to GitHub Pages using GitHub Actions, making the list accessible online.

## Contributing

### Adding Known RSE Groups

If you know of an RSE group at an R1 university that is not currently listed, you can add it to the `has_rse/known_rse_groups.py` file. Follow the existing format:

```python
known_rse_groups = {
    # ... other universities
    "University of Example": {
        "href": "https://example.edu/rse",  # Link to the RSE group's webpage
        "description": "Example RSE Group",  # Optional description
    },
}
```

### Adding Blacklisted URLs

If a URL is incorrectly identified as indicating an RSE group, you can add it to the `has_rse/blacklist.py` file:

```python
blacklisted = [
    # ... other URLs
    "https://example.edu/some-page",
]
```

After making changes, please submit a pull request. Your contributions are greatly appreciated!

## Disclaimer

This list is generated automatically and may contain inaccuracies. The presence or absence of an RSE group on this list should not be considered definitive. We recommend visiting the university's website for the most up-to-date information.

A good fraction of this code was generated by Gemini 1.5 Pro.
