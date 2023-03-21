"""TODO."""


def version_callback(*, version: bool) -> None:
    """Print version and exit."""
    if version:
        from importlib import metadata

        from typer import Exit

        print(f"Kodinerds IPTV {metadata.version(__package__)}")
        raise Exit
