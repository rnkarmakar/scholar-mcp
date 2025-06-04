import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/100.0.4896.127 Safari/537.36"
)

mcp = FastMCP("Scholar Server")


@mcp.tool()
def getScholarData(url="https://www.google.com/scholar?q=Quantum+Physics&hl=en"):
    """
    Scrapes the organic results from a Google Scholar search for the given query.
    Args:
        url (str): The URL of the Google Scholar search page.
    Returns:
        list: A list of dictionaries containing the title, link, and other details of each result.
    """

    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT})
        soup = BeautifulSoup(response.text, "html.parser")
        scholar_results = []

        # Note: The CSS selectors (e.g. '.gs_r', '.gs_rt') are based on the original page structure.
        for el in soup.select(".gs_r"):
            try:
                scholar_results.append(
                    {
                        "title": el.select(".gs_rt")[0].text,
                        "title_link": el.select(".gs_rt a")[0]["href"],
                        "id": el.select(".gs_rt a")[0].get("id", ""),
                        "displayed_link": el.select(".gs_a")[0].text,
                        "snippet": el.select(".gs_rs")[0].text.replace("\n", ""),
                        "cited_by_count": el.select(".gs_nph+ a")[0].text,
                        "cited_link": "https://scholar.google.com"
                        + el.select(".gs_nph+ a")[0]["href"],
                        "versions_count": el.select("a~ a+ .gs_nph")[0].text,
                        "versions_link": (
                            "https://scholar.google.com"
                            + el.select("a~ a+ .gs_nph")[0]["href"]
                            if el.select("a~ a+ .gs_nph")[0].text
                            else ""
                        ),
                    }
                )
            except Exception as sub_err:
                print("Error processing one result:", sub_err)

        # Remove keys with empty values in each result dictionary
        for i in range(len(scholar_results)):
            scholar_results[i] = {k: v for k, v in scholar_results[i].items() if v}

        return scholar_results

    except Exception as err:
        print("Error in getScholarData():", err)


@mcp.tool()
def getArxivData(
    url="https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=allintitle%3A+Quantum+Physics+source%3Aarxiv&btnG=",
):
    """
    Searches for papers on arXiv using Google Scholar's search page.
    Args:
        url (str): The URL for the Google Scholar search query : "allintitle: <title from getScholarData result> source:arxiv".
    Returns:
        list: A list of dictionaries containing the title, link, and other details.
    """

    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT})
        soup = BeautifulSoup(response.text, "html.parser")
        scholar_results = []

        # Note: The CSS selectors (e.g. '.gs_r', '.gs_rt') are based on the original page structure.
        for el in soup.select(".gs_r"):
            try:
                result = {}

                # Only add elements if they exist
                title_elements = el.select(".gs_rt")
                if title_elements:
                    result["title"] = title_elements[0].text

                title_links = el.select(".gs_rt a")
                if title_links:
                    result["title_link"] = title_links[0]["href"]
                    result["id"] = title_links[0].get("id", "")

                displayed_links = el.select(".gs_a")
                if displayed_links:
                    result["displayed_link"] = displayed_links[0].text

                snippets = el.select(".gs_rs")
                if snippets:
                    result["snippet"] = snippets[0].text.replace("\n", "")

                cited_elements = el.select(".gs_nph+ a")
                if cited_elements:
                    result["cited_by_count"] = cited_elements[0].text
                    result["cited_link"] = (
                        "https://scholar.google.com" + cited_elements[0]["href"]
                    )

                version_elements = el.select("a~ a+ .gs_nph")
                if version_elements:
                    result["versions_count"] = version_elements[0].text
                    if version_elements[0].text:
                        result["versions_link"] = (
                            "https://scholar.google.com" + version_elements[0]["href"]
                        )

                scholar_results.append(result)

            except Exception as sub_err:
                print("Error processing one result:", sub_err)

        # Remove keys with empty values in each result dictionary
        for i in range(len(scholar_results)):
            scholar_results[i] = {k: v for k, v in scholar_results[i].items() if v}

        return scholar_results

    except Exception as err:
        print("Error in getArxivData():", err)


@mcp.tool()
def getCitedByData(
    cites_id: str = "6493488604127984456",
    hl: str = "en",
    as_sdt: str = "0,5",
    start: int = 0,
    max_pages: int = 1,
):
    """
    Returns the papers that cite a target work, using Google Scholar's
    ?cites=<cluster_id> endpoint.

    Args:
        cites_id  (str):  Scholar cluster-ID obtained from the “Cited by N” link.
        hl        (str):  Interface language (default 'en').
        as_sdt    (str):  Scholar's 'as_sdt' param (default '0,5' = all + patents).
        start     (int):  Result offset (use multiples of 10 to page).
        max_pages (int):  How many 10-result pages to fetch consecutively.

    Returns:
        list[dict]: Each dict has 'title', 'title_link', 'displayed_link',
                    'snippet', and (if present) 'cited_by_count', 'cited_link',
                    'versions_count', 'versions_link'.
    """

    base = "https://scholar.google.com/scholar"
    results = []
    page = 0
    while page < max_pages:
        params = {
            "cites": cites_id,
            "hl": hl,
            "as_sdt": as_sdt,
            "start": start + page * 10,
        }
        try:
            resp = requests.get(
                base, params=params, headers={"User-Agent": USER_AGENT}, timeout=15
            )
            resp.raise_for_status()
        except Exception as e:
            print(f"Request failed on page {page}: {e}")
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select(".gs_r")
        if not cards:
            # No more results / structure changed.
            break

        for el in cards:
            try:
                entry = {
                    "title": el.select_one(".gs_rt").text,
                    "title_link": el.select_one(".gs_rt a")["href"],
                    "displayed_link": el.select_one(".gs_a").text,
                    "snippet": el.select_one(".gs_rs").get_text(" ", strip=True),
                }

                # Optional “Cited by” and “Versions” sub-links (if they exist)
                cite_link = el.select_one(".gs_nph+ a")
                if cite_link:
                    entry["cited_by_count"] = cite_link.text
                    entry["cited_link"] = (
                        "https://scholar.google.com" + cite_link["href"]
                    )

                vers_link = el.select_one("a~ a+ .gs_nph")
                if vers_link and vers_link.text.strip():
                    entry["versions_count"] = vers_link.text
                    entry["versions_link"] = (
                        "https://scholar.google.com" + vers_link["href"]
                    )

                # Drop empty keys
                results.append({k: v for k, v in entry.items() if v})

            except Exception as sub_err:
                # Skip malformed card but continue scraping
                print("Error processing one citing result:", sub_err)

        # Stop early if Scholar shows “no more pages” marker
        next_button = soup.select_one("#gs_n a[aria-label='Next']")
        if not next_button:
            break

        page += 1

    return results


@mcp.tool()
def getScholarProfiles(
    url="https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=Quantum+Physics",
):
    """
    Scrapes scholar (author) profiles from a Google Scholar search page.
    Args:
        url (str): The URL of the Google Scholar search page.
    Returns:
        list: A list of dictionaries containing the name, link, position, email, departments,
              and cited by count of each profile.
    """

    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT})
        soup = BeautifulSoup(response.content, "html.parser")
        scholar_profiles = []

        for el in soup.select(".gsc_1usr"):
            profile = {
                "name": (
                    el.select_one(".gs_ai_name").get_text()
                    if el.select_one(".gs_ai_name")
                    else ""
                ),
                "name_link": (
                    "https://scholar.google.com"
                    + el.select_one(".gs_ai_name a")["href"]
                    if el.select_one(".gs_ai_name a")
                    else ""
                ),
                "position": (
                    el.select_one(".gs_ai_aff").get_text()
                    if el.select_one(".gs_ai_aff")
                    else ""
                ),
                "email": (
                    el.select_one(".gs_ai_eml").get_text()
                    if el.select_one(".gs_ai_eml")
                    else ""
                ),
                "departments": (
                    el.select_one(".gs_ai_int").get_text()
                    if el.select_one(".gs_ai_int")
                    else ""
                ),
                "cited_by_count": (
                    el.select_one(".gs_ai_cby").get_text().split()[-1]
                    if el.select_one(".gs_ai_cby")
                    else ""
                ),
            }

            # Remove empty fields
            profile = {k: v for k, v in profile.items() if v}
            scholar_profiles.append(profile)

        return scholar_profiles

    except Exception as err:
        print("Error in getScholarProfiles():", err)


@mcp.tool()
def getAuthorProfileData(
    url="https://scholar.google.com/citations?hl=en&user=cOsxSDEAAAAJ",
):
    """
    Scrapes the complete profile of an author including the basic info,
    the list of articles, and citation metrics.
    Args:
        url (str): The URL of the author's Google Scholar profile page.
    Returns:
        dict: A dictionary containing the author's name, position, email, departments,
              list of articles, and citation metrics (cited by count, h-index, i10-index).
    """

    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT})
        soup = BeautifulSoup(response.text, "html.parser")
        author_results = {}

        # Main Author Details
        author_results["name"] = (
            soup.select_one("#gsc_prf_in").text
            if soup.select_one("#gsc_prf_in")
            else ""
        )
        author_results["position"] = (
            soup.select_one("#gsc_prf_inw + .gsc_prf_il").text
            if soup.select_one("#gsc_prf_inw + .gsc_prf_il")
            else ""
        )
        author_results["email"] = (
            soup.select_one("#gsc_prf_ivh").text
            if soup.select_one("#gsc_prf_ivh")
            else ""
        )
        author_results["departments"] = (
            soup.select_one("#gsc_prf_int").text
            if soup.select_one("#gsc_prf_int")
            else ""
        )

        # Published Articles
        articles = []
        for el in soup.select("#gsc_a_b .gsc_a_t"):
            article = {
                "title": el.select_one(".gsc_a_at").text,
                "link": "https://scholar.google.com"
                + el.select_one(".gsc_a_at").get("href", ""),
                "authors": (
                    el.select_one(".gsc_a_at + .gs_gray").text
                    if el.select_one(".gsc_a_at + .gs_gray")
                    else ""
                ),
                "publication": (
                    el.select_one(".gs_gray + .gs_gray").text
                    if el.select_one(".gs_gray + .gs_gray")
                    else ""
                ),
            }
            articles.append({k: v for k, v in article.items() if v})

        # Citation Metrics (Cited By, h-index, i10-index)
        cited_by = {}
        cited_by["table"] = []

        # Row 1: Citations
        row1 = {}
        row1["citations"] = {
            "all": (
                soup.select_one("tr:nth-child(1) .gsc_rsb_sc1 + .gsc_rsb_std").text
                if soup.select_one("tr:nth-child(1) .gsc_rsb_sc1 + .gsc_rsb_std")
                else ""
            ),
            "since_2017": (
                soup.select_one("tr:nth-child(1) .gsc_rsb_std + .gsc_rsb_std").text
                if soup.select_one("tr:nth-child(1) .gsc_rsb_std + .gsc_rsb_std")
                else ""
            ),
        }
        cited_by["table"].append(row1)

        # Row 2: h-index
        row2 = {}
        row2["h_index"] = {
            "all": (
                soup.select_one("tr:nth-child(2) .gsc_rsb_sc1 + .gsc_rsb_std").text
                if soup.select_one("tr:nth-child(2) .gsc_rsb_sc1 + .gsc_rsb_std")
                else ""
            ),
            "since_2017": (
                soup.select_one("tr:nth-child(2) .gsc_rsb_std + .gsc_rsb_std").text
                if soup.select_one("tr:nth-child(2) .gsc_rsb_std + .gsc_rsb_std")
                else ""
            ),
        }
        cited_by["table"].append(row2)

        # Row 3: i10-index
        row3 = {}
        row3["i_index"] = {
            "all": (
                soup.select_one("tr~ tr+ tr .gsc_rsb_sc1 + .gsc_rsb_std").text
                if soup.select_one("tr~ tr+ tr .gsc_rsb_sc1 + .gsc_rsb_std")
                else ""
            ),
            "since_2017": (
                soup.select_one("tr~ tr+ tr .gsc_rsb_std + .gsc_rsb_std").text
                if soup.select_one("tr~ tr+ tr .gsc_rsb_std + .gsc_rsb_std")
                else ""
            ),
        }
        cited_by["table"].append(row3)

        return {
            "author_results": author_results,
            "articles": articles,
            "cited_by": cited_by,
        }

    except Exception as err:
        print("Error in getAuthorProfileData():", err)


if __name__ == "__main__":
    mcp.run(transport="stdio")
