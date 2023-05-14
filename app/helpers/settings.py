import json
from pathlib import Path


def _write_dict_to_file(fname: Path | str | None, contents: dict) -> Path:
    """
    Writes the contents to a file with the given name

    Args:
        Args:
        fname (Path | str | None, optional): Path or filename to write the
            settings to. Defaults to None. If None, the file will be in the
            working directory in with the filename 'user_settings.json'.
            Defaults to None.
        contents (dict): the dict to write to the file

    Returns:
        Path: Path to the file
    """
    if not isinstance(fname, Path):
        fname = Path(fname)

    with open(fname, "w") as f:
        json.dump(contents, f)

    return fname
