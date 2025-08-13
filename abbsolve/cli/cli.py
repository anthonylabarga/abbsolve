from typing import Optional

import typer

from abbsolve.infer.regex import RegexInitialismInverter

app = typer.Typer()


@app.command()
def main(
    initialism: str,
    directory: str = typer.Option(
        ".", "-d", "--directory", help="The root directory to search"
    ),
    workers: Optional[int] = typer.Option(
        None, "-w", "--workers", help="Max worker threads"
    ),
    with_sources: bool = typer.Option(
        False,
        "-s",
        "--with-sources",
        help="Show the files where the matches were found",
    ),
):
    """Resolve initialisms to their full forms."""
    if len(initialism) < 2:
        typer.echo("Error: Initialism must be at least 2 characters long.", err=True)
        raise typer.Exit(1)
    try:
        inverter = RegexInitialismInverter(initialism, directory)

        if with_sources:
            results = inverter.find_candidates_with_sources()
            if results:
                for candidate, sources in results.items():
                    typer.echo(f"{candidate}:")
                    for source in sources:
                        typer.echo(f"  - {source}")
            else:
                typer.echo(f"No candidates found for '{initialism}'")
        else:
            results = inverter.find_candidates(max_workers=workers)
            if results:
                for candidate in results:
                    typer.echo(candidate)
            else:
                typer.echo(f"No candidates found for '{initialism}'")

    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
