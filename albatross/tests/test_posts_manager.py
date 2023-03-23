import datetime

import albatross.managers.articles as pm


def test_create_post(tmpdir):
    # Create a dictionary with the metadata for the article
    metadata = {"title": "Test article", "author": "Test Author"}
    # Create a string with the content for the article
    content = "This is a test article"
    # Call the create_post function and store the result in a variable
    post_file = pm.create_post(metadata, content, tmpdir)
    # Use the assert function to check that the returned path exists and is a file
    assert post_file.exists() and post_file.is_file()
    # Use the assert function to check that the metadata and content of the
    # created article file are correct
    post_content = "---\n"
    post_content += "\n".join([f"{key}: {value}" for key, value in metadata.items()])
    post_content += f"\n---\n\n{content}"
    assert post_file.read_text() == post_content


def test_create_post_metadata(tmpdir):
    metadata = {
        "title": "My first article",
        "author": "John Smith",
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now() + datetime.timedelta(days=2),
        "slug": "test-slug",
        "summary": "A summary of my first article",
        "image_url": "https://example.com/image.jpg",
    }
    content = "This is the content of my first article"

    post_path = pm.create_post(metadata, content, tmpdir)

    post_content = "---\n"
    post_content += "\n".join([f"{key}: {value}" for key, value in metadata.items()])
    post_content += f"\n---\n\n{content}"

    assert post_path.name[-3:] == ".md"
    assert post_content == post_path.read_text()
