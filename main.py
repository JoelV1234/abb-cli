import sys
import subprocess
from scraper import search_books, get_magnet_link
from display import (
    display_results,
    display_book_detail,
    display_magnet,
    display_error,
    display_searching,
    console,
)


def prompt_search():
    """Prompt user for a new search query."""
    console.print("[bold cyan]Enter search:[/bold cyan]")
    console.print("[dim]  /t <title>  — search by title[/dim]")
    console.print("[dim]  /a <author> — search by author[/dim]")
    console.print("[dim]  <query>     — search by title (default)[/dim]")
    console.print("[dim]  q           — quit[/dim]")

    try:
        user_input = console.input("\n[bold]> [/bold]").strip()
    except (EOFError, KeyboardInterrupt):
        return None, None

    if not user_input or user_input.lower() == "q":
        return None, None

    return parse_search_input(user_input)


def parse_search_input(text):
    """Parse a search input string into (query, search_type)."""
    text = text.strip()

    if text.lower().startswith("/t "):
        return text[3:].strip(), "title"
    elif text.lower().startswith("/a "):
        return text[3:].strip(), "author"
    else:
        return text, "title"


def interactive_loop(query, search_type, page=1):
    """Main interactive loop: display results and handle user input."""
    while True:
        display_searching(query, search_type)
        data = search_books(query, search_type, page)

        if "error" in data:
            display_error(data["error"])
            return

        if not data["books"]:
            display_error(f"No results found for '{query}'.")
            query, search_type = prompt_search()
            if query is None:
                return
            page = 1
            continue

        display_results(data)
        last_selected = None
        last_magnet = None

        # Input loop for current page
        while True:
            try:
                user_input = console.input("[bold]> [/bold]").strip()
            except (EOFError, KeyboardInterrupt):
                console.print("\n[dim]Goodbye![/dim]")
                return

            if not user_input:
                continue

            low = user_input.lower()

            # Quit
            if low == "q":
                console.print("[dim]Goodbye![/dim]")
                return

            # Next page
            if low == "n":
                if data["current_page"] < data["total_pages"]:
                    page = data["current_page"] + 1
                    break
                else:
                    display_error("Already on the last page.")
                    continue

            # Previous page
            if low == "p":
                if data["current_page"] > 1:
                    page = data["current_page"] - 1
                    break
                else:
                    display_error("Already on the first page.")
                    continue

            # Redisplay table
            if low == "tr":
                display_results(data)
                continue

            # Jump to page
            if low.startswith("page "):
                try:
                    target = int(low.split("page ", 1)[1].strip())
                    if 1 <= target <= data["total_pages"]:
                        page = target
                        break
                    else:
                        display_error(
                            f"Page must be between 1 and {data['total_pages']}."
                        )
                except ValueError:
                    display_error("Usage: page <number>")
                continue

            # New search commands
            if low == "r":
                new_query, new_type = prompt_search()
                if new_query is None:
                    return
                query, search_type = new_query, new_type
                page = 1
                break

            if low.startswith("/t ") or low.startswith("/a "):
                new_query, new_type = parse_search_input(user_input)
                if new_query:
                    query, search_type = new_query, new_type
                    page = 1
                    break
                continue

            # Magnet link for last selected book
            if low == "m":
                if last_selected is None:
                    display_error("Select a book first (enter its number).")
                else:
                    book = data["books"][last_selected - 1]
                    if book["detail_url"]:
                        console.print("[dim]Fetching magnet link...[/dim]")
                        magnet, err = get_magnet_link(book["detail_url"])
                        if err:
                            display_error(err)
                        else:
                            last_magnet = magnet
                            display_magnet(magnet)
                    else:
                        display_error("No detail URL for this book.")
                continue

            # Copy magnet link to clipboard (fetch first if needed)
            if low == "c":
                if last_selected is None:
                    display_error("Select a book first (enter its number).")
                else:
                    if last_magnet is None:
                        book = data["books"][last_selected - 1]
                        if book["detail_url"]:
                            console.print("[dim]Fetching magnet link...[/dim]")
                            magnet, err = get_magnet_link(book["detail_url"])
                            if err:
                                display_error(err)
                                continue
                            last_magnet = magnet
                        else:
                            display_error("No detail URL for this book.")
                            continue
                    try:
                        subprocess.run(
                            ["xclip", "-selection", "clipboard"],
                            input=last_magnet.encode(),
                            check=True,
                        )
                        console.print("[bold green]Magnet link copied to clipboard![/bold green]")
                    except FileNotFoundError:
                        try:
                            subprocess.run(
                                ["xsel", "--clipboard", "--input"],
                                input=last_magnet.encode(),
                                check=True,
                            )
                            console.print("[bold green]Magnet link copied to clipboard![/bold green]")
                        except FileNotFoundError:
                            display_error("Install xclip or xsel to copy to clipboard.")
                continue

            # Select book by number
            try:
                choice = int(user_input)
                if 1 <= choice <= len(data["books"]):
                    last_selected = choice
                    display_book_detail(data["books"][choice - 1], choice)
                    continue
                else:
                    display_error(
                        f"Enter a number between 1 and {len(data['books'])}."
                    )
            except ValueError:
                display_error(
                    "Unknown command. Use n/p/page <#>/r//t//a/<number>/q"
                )


def main():
    """Entry point — parse CLI arguments and start the loop."""
    args = sys.argv[1:]

    if not args:
        # No args — prompt for search
        query, search_type = prompt_search()
        if query is None:
            return
    else:
        query, search_type = parse_search_input(" ".join(args))

    if not query:
        display_error("No search query provided.")
        return

    interactive_loop(query, search_type)


if __name__ == "__main__":
    main()
