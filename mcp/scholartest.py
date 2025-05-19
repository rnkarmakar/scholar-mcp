import requests
from bs4 import BeautifulSoup

#%%
def getArxivData(url = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=allintitle%3A+Quantum+Physics+source%3Aarxiv&btnG="):
    """
    Searches for papers on arXiv using Google Scholar's search page.
    Args:
        url (str): The URL for the Google Scholar search query : "allintitle: <title from getScholarData result> source:arxiv".
    Returns:
        list: A list of dictionaries containing the title, link, and other details.
    """
    try:
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/100.0.4896.127 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
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
                    result["cited_link"] = "https://scholar.google.com" + cited_elements[0]["href"]
                
                version_elements = el.select("a~ a+ .gs_nph")
                if version_elements:
                    result["versions_count"] = version_elements[0].text
                    if version_elements[0].text:
                        result["versions_link"] = "https://scholar.google.com" + version_elements[0]["href"]
            
                scholar_results.append(result)
                
            except Exception as sub_e:
                print("Error processing one result:", sub_e)
        
        # Remove keys with empty values in each result dictionary
        for i in range(len(scholar_results)):
            scholar_results[i] = {k: v for k, v in scholar_results[i].items() if v}
        
        print("Google Scholar Organic Results:")
        return scholar_results
    except Exception as e:
        print("Error in getArxivData():", e)

print(getArxivData("https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=allintitle%3A+On+layer+normalization+in+the+transformer+architecture+source%3Aarxiv&btnG="))