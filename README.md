# ABB-CLI — AudioBook Bay CLI Search Tool

A command-line tool to search for audiobooks on AudioBook Bay.  
Browse results in a paginated table, view book details, and grab magnet links.
> **⚠️ Warning:** This software has currently only been tested on **Linux**. The install scripts behave conditionally and may not work exactly as intended on macOS or Windows.

## Dependencies

### System (Linux)
- `libxml2` and `libxslt1.1` (installed automatically by `setup.sh`)

### Python

- **Python 3.8+**
- `requests` — HTTP requests
- `lxml` — HTML parsing
- `cssselect` — CSS selector support for lxml
- `rich` — styled terminal tables and panels

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/JoelV1234/abb-cli.git
   cd abb-cli
   ```

2. Run the setup script:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
   This creates a virtual environment, installs Python dependencies, and makes `run.sh` executable.

## Uninstall

To completely remove ABB-CLI, run from inside the project directory:
```bash
chmod +x uninstall.sh
./uninstall.sh
```
This will uninstall the Python dependencies and delete the project folder.

## Usage

Start the tool:
```bash
./run.sh
```

Or pass a search directly:
```bash
./run.sh /t <title>       # Search by title
./run.sh /a <author>      # Search by author
```

## Commands

| Key | Action |
|---|---|
| `<number>` | Select a book to view its details |
| `n` | Next page |
| `p` | Previous page |
| `page <N>` | Jump to page N |
| `tr` | Redisplay the current results table |
| `m` | Fetch and display the magnet link |
| `c` | ⚠️ **Not working** — Copy magnet link to clipboard (uses OSC52) |
| `r` | Start a new search |
| `/t <query>` | New title search |
| `/a <query>` | New author search |
| `q` | Quit |

## Files

| File | Purpose |
|---|---|
| `main.py` | Entry point and interactive loop |
| `scraper.py` | Fetches and parses search results and magnet links |
| `display.py` | Renders tables and book detail panels |
| `constants.py` | Base URL, headers, config |
| `requirements.txt` | Python dependencies |
| `setup.sh` | One-time setup script |
| `run.sh` | Launch script |
| `uninstall.sh` | Removes dependencies and project folder |

## Known Issues

- **`c` (copy) command does not work** — The copy-to-clipboard feature uses OSC52 escape sequences, which are not supported by all terminal emulators. Use `m` to display the magnet link and copy it manually instead.
