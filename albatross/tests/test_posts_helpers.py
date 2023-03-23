from albatross.helpers.articles import generate_introduction


def test_generate_introduction():
    # Test with minimum number of characters
    content = "This is the content of the post and it is 50 chars"
    intro = generate_introduction(content, 50)
    assert intro == content

    # Test with more than minimum number of characters
    intro = generate_introduction("This is the content of the post", 5)
    assert intro == "This..."

    # Test with content that is shorter than the minimum number of characters
    intro = generate_introduction("This is short", 100)
    assert intro == "This is short"

    # Test that the function correctly generates an introduction
    # from the given content
    content = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
        "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim "
        "veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea "
        "commodo consequat. Duis aute irure dolor in reprehenderit in voluptate "
        "velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat "
        "cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id "
        "est laborum."
    )
    expected_intro = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
        "tempor incididunt ut labore et dolore magna aliqua."
    )
    assert generate_introduction(content) == expected_intro
