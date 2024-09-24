#!/usr/bin/env python3

import logging
import json
from time import sleep
from typing import List, Dict, Optional

from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import RatelimitException
from has_rse.r1 import r1_universities
from has_rse.blacklist import blacklisted
from has_rse.known_rse_groups import known_rse_groups
from has_rse.html import generate_html

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Increased sleep time to 0.5 seconds
SLEEP_TIME = 0.5
RETRY_DELAY = 60  # Delay in seconds before retrying after rate limiting
MAX_ATTEMPTS = 3


def search_for_rse_info(university: str) -> List[Dict]:
    """Searches for RSE information using DuckDuckGo and filters for .edu domains.

    Args:
        university: The name of the university to search for.

    Returns:
        A list of dictionaries, where each dictionary represents a search result
        from a .edu domain, excluding blacklisted URLs.
    """
    query = f"{university} research software engineering"
    logger.info(f"Searching for RSE info with query: {query}")

    attempts = 1
    while attempts <= MAX_ATTEMPTS:  # Retry loop for rate limiting
        try:
            results = DDGS().text(query, region="us-en", max_results=10)
            break  # Exit loop if search is successful
        except RatelimitException:
            logger.warning(f"Rate limit exceeded. Retrying in {RETRY_DELAY} seconds...")
            sleep(RETRY_DELAY)
            attempts = attempts + 1

    filtered_results = [
        result
        for result in results
        if ".edu" in result["href"] and result["href"] not in blacklisted
    ]
    logger.info(f"Found {len(filtered_results)} potential matches for {university}")
    return filtered_results


def extract_rse_info(search_results: List[Dict]) -> Optional[Dict]:
    """Extracts relevant RSE information from DuckDuckGo search results.

    Args:
        search_results: A list of search result dictionaries.

    Returns:
        A dictionary containing the title, body (snippet), and href (link) of the
        first search result that matches RSE keywords, or None if no match is found.
    """
    rse_keywords = {
        "research software engineer",
        "rse group",
        "rse team",
        "rse department",
    }
    exclude_keywords = {"personal",
                        "research software engineering workshop",
                        "full time"}

    for result in search_results:
        lowercase_body = result["body"].lower()
        if any(keyword in lowercase_body for keyword in rse_keywords) and not any(
            keyword in lowercase_body for keyword in exclude_keywords
        ):
            logger.info(f"Found potential RSE info in: {result['title']}")
            return result

    return None


def get_rse_info(university: str) -> Optional[Dict]:
    """Checks if a university has a known RSE group or searches for one.

    Args:
        university: The name of the university.

    Returns:
        A dictionary with RSE information if found, otherwise None.
    """
    if university in known_rse_groups:
        logger.info(f"Found {university} in known_rse_groups")
        return {"name": university, **known_rse_groups[university]}

    search_results = search_for_rse_info(university)
    return extract_rse_info(search_results)


def generate_json(outpath: str) -> None:
    """Generates a JSON file with RSE information for R1 universities.

    Args:
        outpath: Path to save the generated JSON file.
    """
    university_data = []

    for university in r1_universities:
        logger.info(f"Scanning university: {university}")
        info = get_rse_info(university)
        has_rse = bool(info)
        logger.info(f"{university}: {has_rse}")
        link = info.get("href", "") if info else ""
        university_data.append({"name": university, "has_rse": has_rse, "link": link})
        sleep(0.1)  # Add a small delay to be polite to the search engine

    with open(outpath, "w") as f:
        json.dump(university_data, f, indent=4)
