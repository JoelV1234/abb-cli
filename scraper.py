import requests
from urllib.parse import quote
from lxml import html
from constants import BASE_URL, HEADERS


def _build_url(query, search_type="title", page=1):
    """Build the search URL based on query, type, and page."""
    query_encoded = requests.utils.quote(query)

    if search_type == "author":
        params = f"?s={query_encoded}&tt=1"
    else:
        params = f"?s={query_encoded}&cat=undefined%2Cundefined"

    if page > 1:
        return f"{BASE_URL}/page/{page}/{params}"
    return f"{BASE_URL}/{params}"


def _parse_book(post_el):
    """Parse a single div.post element into a book dict."""
    book = {
        "title": "",
        "author": "",
        "category": "",
        "language": "",
        "keywords": "",
        "format": "",
        "bitrate": "",
        "size": "",
        "posted": "",
        "detail_url": "",
    }

    # Title & Author from div.postTitle h2 a
    title_el = post_el.cssselect("div.postTitle h2 a")
    if title_el:
        full_text = title_el[0].text_content().strip()
        book["detail_url"] = BASE_URL + title_el[0].get("href", "")

        # Split "Title - Author" format
        if " - " in full_text:
            parts = full_text.rsplit(" - ", 1)
            book["title"] = parts[0].strip()
            book["author"] = parts[1].strip()
        else:
            book["title"] = full_text

    # Category, Language, Keywords from div.postInfo
    # The text flows as: "Category: X  Y  Z  Language: EnglishKeywords: A  B"
    # We split on the known markers since <br> doesn't produce newlines.
    info_el = post_el.cssselect("div.postInfo")
    if info_el:
        info_text = info_el[0].text_content().strip()

        if "Category:" in info_text:
            cat_part = info_text.split("Category:", 1)[1]
            if "Language:" in cat_part:
                cat_part = cat_part.split("Language:", 1)[0]
            book["category"] = " ".join(cat_part.split()).strip()

        if "Language:" in info_text:
            lang_part = info_text.split("Language:", 1)[1]
            if "Keywords:" in lang_part:
                lang_part = lang_part.split("Keywords:", 1)[0]
            book["language"] = lang_part.strip()

        if "Keywords:" in info_text:
            kw_part = info_text.split("Keywords:", 1)[1]
            book["keywords"] = " ".join(kw_part.split()).strip()

    # Posted date, Format, Bitrate, Size from div.postContent
    # Like postInfo, <br> doesn't produce newlines so we split on markers.
    content_el = post_el.cssselect("div.postContent")
    if content_el:
        # Use span elements directly for reliable extraction
        spans = content_el[0].cssselect("span")

        # Format & Bitrate from red spans
        colored_spans = [s for s in spans if "color:#a00" in (s.get("style") or "")]
        if len(colored_spans) >= 1:
            book["format"] = colored_spans[0].text_content().strip()
        if len(colored_spans) >= 2:
            book["bitrate"] = colored_spans[1].text_content().strip()

        # File size from blue span
        size_spans = [s for s in spans if "color:#00f" in (s.get("style") or "")]
        if size_spans:
            book["size"] = size_spans[0].text_content().strip() + " MBs"

        # Posted date from text
        full_text = content_el[0].text_content()
        if "Posted:" in full_text:
            posted_part = full_text.split("Posted:", 1)[1]
            # Cut off at Format: or end of text
            if "Format:" in posted_part:
                posted_part = posted_part.split("Format:", 1)[0]
            book["posted"] = posted_part.strip()

    return book


def _parse_pagination(tree):
    """Parse pagination info from the page."""
    current_page = 1
    total_pages = 1

    nav = tree.cssselect("div.wp-pagenavi")
    if nav:
        # Current page
        current = nav[0].cssselect("span.current")
        if current:
            try:
                current_page = int(current[0].text_content().strip())
            except ValueError:
                pass

        # Total pages from the "last" link or highest page number
        last_link = nav[0].cssselect("a.last")
        if last_link:
            href = last_link[0].get("href", "")
            parts = href.split("/page/")
            if len(parts) > 1:
                page_part = parts[1].split("/")[0]
                try:
                    total_pages = int(page_part)
                except ValueError:
                    pass
        else:
            # Fall back to the highest numbered page link
            page_links = nav[0].cssselect("a")
            for link in page_links:
                try:
                    num = int(link.text_content().strip())
                    total_pages = max(total_pages, num)
                except ValueError:
                    pass
            total_pages = max(total_pages, current_page)

    return current_page, total_pages


def search_books(query, search_type="title", page=1):
    """
    Search audiobookbay for books.

    Args:
        query: Search query string
        search_type: "title" or "author"
        page: Page number (1-indexed)

    Returns:
        dict with keys: books, current_page, total_pages, query, search_type
    """
    url = _build_url(query, search_type, page)

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        return {
            "books": [],
            "current_page": page,
            "total_pages": 1,
            "query": query,
            "search_type": search_type,
            "error": str(e),
        }

    tree = html.fromstring(response.content)

    posts = tree.cssselect("div.post")
    books = [_parse_book(post) for post in posts]

    current_page, total_pages = _parse_pagination(tree)

    return {
        "books": books,
        "current_page": current_page,
        "total_pages": total_pages,
        "query": query,
        "search_type": search_type,
    }


def get_magnet_link(detail_url):
    """
    Fetch a book's detail page and construct a magnet link
    from the info hash and trackers.
    """
    try:
        response = requests.get(detail_url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        return None, str(e)

    tree = html.fromstring(response.content)

    # Extract info hash
    info_hash = ""
    hash_cells = tree.xpath('//td[contains(text(), "Info Hash:")]/following-sibling::td')
    if hash_cells:
        info_hash = hash_cells[0].text_content().strip()

    if not info_hash:
        return None, "Could not find info hash on detail page."

    # Extract trackers
    trackers = []
    tracker_cells = tree.xpath('//td[contains(text(), "Tracker")]/following-sibling::td')
    for td in tracker_cells:
        tracker = td.text_content().strip()
        if tracker:
            trackers.append(tracker)

    # Get title for display name
    title_el = tree.cssselect("div.postTitle h1")
    title = title_el[0].text_content().strip() if title_el else ""

    # Build magnet link
    magnet = f"magnet:?xt=urn:btih:{info_hash}"
    if title:
        magnet += f"&dn={quote(title)}"
    for tracker in trackers:
        magnet += f"&tr={quote(tracker)}"

    return magnet, None

