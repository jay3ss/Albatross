import os
import tempfile

from pelican import Pelican, read_settings
import yaml


settings = read_settings()
content = """
Hello and welcome to my blog! This is my first article, and I'm excited to share my
thoughts and experiences with all of you. I hope you enjoy reading my blog as
much as I enjoy writing it.

Thank you for stopping by!
"""


with tempfile.TemporaryDirectory(prefix="content", dir=".") as td:
    for i in range(1, 11):
        metadata = {
            "title": f"My Article #{i}",
            "author": "John Doe",
            "date": "2022-01-01",
            "tags": [f"tag{i}", f"tag{i+1}"],
        }
        text = yaml.safe_dump(metadata, sort_keys=False) + content
        temp_fd, temp_path = tempfile.mkstemp(
            suffix=".md",
            prefix="albatross",
            dir=td,
        )
        with os.fdopen(temp_fd, "w+") as tf:
            tf.write(text)
    settings["PATH"] = td
    pel = Pelican(settings=settings)
    pel.run()
