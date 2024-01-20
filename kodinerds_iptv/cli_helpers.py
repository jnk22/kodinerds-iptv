"""TODO."""


def version_callback(*, version: bool) -> None:
    """Print version and exit."""
    if version:
        from importlib import metadata

        from typer import Exit

        print(f"Kodinerds IPTV CLI {metadata.version(__package__)}")  # noqa: T201
        raise Exit
