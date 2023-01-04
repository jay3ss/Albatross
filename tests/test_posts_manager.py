import datetime

from .fixtures import base_dir
import albatross.posts_manager as pm



def test_create_post(base_dir):
    # Create a dictionary with the metadata for the post
    metadata = {'title': 'Test post', 'author': 'Test Author'}
    # Create a string with the content for the post
    content = 'This is a test post'
    # Call the create_post function and store the result in a variable
    post_path = pm.create_post(metadata, content, base_dir)
    # Use the assert function to check that the returned path exists and is a file
    assert post_path.exists() and post_path.is_file()
    # Use the assert function to check that the metadata and content of the created post file are correct
    assert post_path.read_text() == content
    assert post_path.metadata == metadata


def test_create_post(base_dir):
    metadata = {
        "title": "My first post",
        "author": "John Smith",
        "created_at": "2022-01-01",
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now() + datetime.timedelta(days=2),
        "slug": "test-slug",
        "summary": "A summary of my first post",
        "image_url": "https://example.com/image.jpg"
    }
    content = "This is the content of my first post"

    post_path = pm.create_post(metadata, content, base_dir)

    assert post_path.is_file()
    assert post_path.read_text() == content
    assert metadata["slug"] in post_path.name
    assert metadata["created_at"].strftime("%Y-%m-%d") in post_path.name

    with open(post_path, "r") as f:
        file_content = f.read()
        assert file_content == f"---\n{metadata}\n---\n\n{content}"
