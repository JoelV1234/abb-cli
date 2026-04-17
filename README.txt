ABB-CLI — AudioBook Bay Search Tool
====================================

A command-line tool to search for audiobooks on AudioBook Bay.
Browse results in a paginated table, view book details, and grab magnet links.


DEPENDENCIES
------------
- Python 3.8+
- requests  — HTTP requests
- lxml      — HTML parsing
- cssselect — CSS selector support for lxml
- rich      — styled terminal tables and panels
- xclip     — clipboard support (system package, optional)


INSTALLATION
------------
1. Clone or download this project.

2. Run the setup script:

       chmod +x setup.sh
       ./setup.sh

   This creates a virtual environment, installs Python dependencies,
   and makes run.sh executable.

3. (Optional) Install xclip for the copy-to-clipboard feature:

       sudo apt install xclip


USAGE
-----
Start the tool:

    ./run.sh

Or manually:

    source .venv/bin/activate
    python3 main.py

You can also pass a search directly:

    ./run.sh /t <title>       Search by title
    ./run.sh /a <author>      Search by author


COMMANDS (interactive)
----------------------
  <number>     Select a book to view its details
  n            Next page
  p            Previous page
  page <N>     Jump to page N
  tr           Redisplay the current results table
  m            Fetch and display the magnet link for the selected book
  c            Fetch (if needed) and copy the magnet link to clipboard
  r            Start a new search
  /t <query>   New title search
  /a <query>   New author search
  q            Quit


FILES
-----
  main.py        Entry point and interactive loop
  scraper.py     Fetches and parses search results and magnet links
  display.py     Renders tables and book detail panels (rich)
  constants.py   Base URL, headers, config
  requirements.txt   Python dependencies
  setup.sh       One-time setup script
  run.sh         Launch script
