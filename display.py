from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()


def display_results(data):
    """Display search results in a numbered table."""
    books = data["books"]
    current_page = data["current_page"]
    total_pages = data["total_pages"]
    query = data["query"]
    search_type = data["search_type"]

    if not books:
        console.print(
            f"\n[bold red]No results found for '{query}'[/bold red]\n"
        )
        return

    # Header
    search_label = "Author" if search_type == "author" else "Title"
    console.print(
        f"\n[bold cyan]Search results for {search_label}: "
        f"[yellow]{query}[/yellow][/bold cyan]\n"
    )

    # Build table
    table = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
        border_style="bright_blue",
        row_styles=["", "dim"],
        expand=True,
    )

    table.add_column("#", style="bold cyan", width=4, justify="right")
    table.add_column("Title", style="bold white", ratio=3)
    table.add_column("Author", style="green", ratio=2)
    table.add_column("Category", style="yellow", ratio=2)
    table.add_column("Format", style="cyan", width=8, justify="center")
    table.add_column("Size", style="bright_red", width=12, justify="right")

    for i, book in enumerate(books, 1):
        table.add_row(
            str(i),
            book["title"] or "—",
            book["author"] or "—",
            _truncate(book["category"], 30),
            book["format"] or "—",
            book["size"] or "—",
        )

    console.print(table)

    # Footer with page info and controls
    page_info = Text()
    page_info.append(f"  Page {current_page} of {total_pages}", style="bold white")
    page_info.append("  │  ", style="dim")
    page_info.append("n", style="bold cyan")
    page_info.append("ext  ", style="dim")
    page_info.append("p", style="bold cyan")
    page_info.append("rev  ", style="dim")
    page_info.append("page <#>", style="bold cyan")
    page_info.append("  ", style="dim")
    page_info.append("r", style="bold cyan")
    page_info.append("eset  ", style="dim")
    page_info.append("q", style="bold cyan")
    page_info.append("uit", style="dim")

    console.print(page_info)
    console.print()


def display_book_detail(book, index):
    """Display full details for a selected book."""
    detail_text = Text()

    detail_text.append(f"  Title:     ", style="dim")
    detail_text.append(f"{book['title']}\n", style="bold white")

    detail_text.append(f"  Author:    ", style="dim")
    detail_text.append(f"{book['author']}\n", style="bold green")

    if book["category"]:
        detail_text.append(f"  Category:  ", style="dim")
        detail_text.append(f"{book['category']}\n", style="yellow")

    if book["language"]:
        detail_text.append(f"  Language:  ", style="dim")
        detail_text.append(f"{book['language']}\n", style="white")

    if book["format"]:
        detail_text.append(f"  Format:    ", style="dim")
        detail_text.append(f"{book['format']}\n", style="cyan")

    if book["bitrate"]:
        detail_text.append(f"  Bitrate:   ", style="dim")
        detail_text.append(f"{book['bitrate']}\n", style="cyan")

    if book["size"]:
        detail_text.append(f"  Size:      ", style="dim")
        detail_text.append(f"{book['size']}\n", style="bright_red")

    if book["posted"]:
        detail_text.append(f"  Posted:    ", style="dim")
        detail_text.append(f"{book['posted']}\n", style="white")

    if book["detail_url"]:
        detail_text.append(f"  URL:       ", style="dim")
        detail_text.append(f"{book['detail_url']}\n", style="underline blue")

    detail_text.append(f"\n  Type ", style="dim")
    detail_text.append("m", style="bold cyan")
    detail_text.append(" to display magnet link  ", style="dim")
    detail_text.append("c", style="bold cyan")
    detail_text.append(" to copy magnet", style="dim")

    panel = Panel(
        detail_text,
        title=f"[bold cyan]Book #{index}[/bold cyan]",
        border_style="bright_blue",
        expand=False,
        padding=(1, 2),
    )
    console.print()
    console.print(panel)
    console.print()


def display_magnet(magnet):
    """Display a magnet link."""
    if magnet:
        console.print(f"\n[bold green]Magnet link:[/bold green]")
        console.print(f"[white]{magnet}[/white]\n")
    else:
        console.print("\n[bold red]Could not retrieve magnet link.[/bold red]\n")


def display_error(message):
    """Display an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def display_searching(query, search_type):
    """Display a searching indicator."""
    label = "author" if search_type == "author" else "title"
    console.print(
        f"\n[dim]Searching by {label} for [bold]{query}[/bold]...[/dim]"
    )


def _truncate(text, max_len):
    """Truncate text with ellipsis if too long."""
    if not text:
        return "—"
    if len(text) <= max_len:
        return text
    return text[: max_len - 1] + "…"
