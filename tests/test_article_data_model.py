from app.models import Article, ArticleData, User


def test_article_data_string_representation():
    ad = ArticleData(key="foo", value="bar")
    assert "key" in str(ad)
    assert "value" in str(ad)
    assert "foo" in str(ad)
    assert "bar" in str(ad)


def test_add_article_data_to_article(session):
    user = session.get(User, 1)
    # Create a new Article object
    article = Article(title="Test Article", content="Content", user=user)
    session.add(article)
    session.commit()

    # Create a new ArticleData object
    article_data = ArticleData(key="test_key", value="test_value")

    # Add the ArticleData object to the Article
    article.data.append(article_data)
    session.commit()

    # Retrieve the ArticleData object from the Article
    retrieved_article_data = article.filter_data_by_key(key="test_key")[0]

    # Check that the ArticleData object was added to the Article
    assert retrieved_article_data is not None
    assert retrieved_article_data.key == "test_key"
    assert retrieved_article_data.value == "test_value"


def test_remove_article_data_from_article(session):
    user = session.get(User, 1)
    # Create a new Article object
    article = Article(title="Test Article", content="Content", user=user)
    session.add(article)
    session.commit()

    # Create a new ArticleData object
    article_data = ArticleData(key="test_key", value="test_value")

    # Add the ArticleData object to the Article
    article.data.append(article_data)
    session.commit()

    # Remove the ArticleData object from the Article
    article.data.remove(article_data)
    session.commit()

    # Retrieve the ArticleData object from the Article
    retrieved_article_data = article.filter_data_by_key(key="test_key")


    # Check that the ArticleData object was removed from the Article
    assert len(retrieved_article_data) == 0


def test_update_article_data_in_article(session):
    user = session.get(User, 1)
    # Create a new Article object
    article = Article(title="Test Article", content="Content", user=user)
    session.add(article)
    session.commit()

    # Create a new ArticleData object
    article_data = ArticleData(key="test_key", value="test_value")

    # Add the ArticleData object to the Article
    article.data.append(article_data)
    session.commit()

    # Update the ArticleData object
    article_data.key = "new_key"
    article_data.value = "new_value"
    session.commit()

    # Retrieve the updated ArticleData object from the Article
    updated_article_data = article.filter_data_by_key(key="new_key")[0]

    # Check that the ArticleData object was updated in the Article
    assert updated_article_data is not None
    assert updated_article_data.key == "new_key"
    assert updated_article_data.value == "new_value"


def test_delete_article_data_from_article(session):
    user = session.get(User, 1)
    # Create a new Article object
    article = Article(title="Test Article", content="Content", user=user)
    session.add(article)
    session.commit()

    # Create a new ArticleData object
    article_data = ArticleData(key="test_key", value="test_value")

    # Add the ArticleData object to the Article
    article.data.append(article_data)
    session.commit()

    # Delete the ArticleData object from the Article
    article.data.remove(article_data)
    session.commit()

    # Try to retrieve the deleted ArticleData object from the Article
    retrieved_article_data = article.filter_data_by_key(key="test_key")

    # Check that the ArticleData object was deleted from the Article
    assert len(retrieved_article_data) == 0


def test_clear_article_data_from_article(session):
    user = session.get(User, 1)
    # Create a new Article object
    article = Article(title="Test Article", content="Content", user=user)
    session.add(article)
    session.commit()

    # Create multiple ArticleData objects
    article_data_1 = ArticleData(key="key_1", value="value_1")
    article_data_2 = ArticleData(key="key_2", value="value_2")
    article_data_3 = ArticleData(key="key_3", value="value_3")

    # Add the ArticleData objects to the Article
    article.data.extend([article_data_1, article_data_2, article_data_3])
    session.commit()

    # Clear all ArticleData objects from the Article
    # ArticleData.query.filter(article_id=article.id).delete()
    for data in [article_data_1, article_data_2, article_data_3]:
        article.data.remove(data)
    session.commit()

    # Try to retrieve the cleared ArticleData objects from the Article
    retrieved_article_data_1 = article.filter_data_by_key(key="key_1")
    retrieved_article_data_2 = article.filter_data_by_key(key="key_2")
    retrieved_article_data_3 = article.filter_data_by_key(key="key_3")

    # Check that all ArticleData objects were cleared from the Article
    assert len(retrieved_article_data_1) == 0
    assert len(retrieved_article_data_2) == 0
    assert len(retrieved_article_data_3) == 0


def test_article_data_to_dict(session):
    user = session.get(User, 1)
    # Create new Article and ArticleData objects
    article_data = ArticleData(key="key", value="value")
    article = Article(title="Test Article", content="Content", user=user)
    article.data.append(article_data)
    another_article = Article(title="Another Article", content="Content", user=user)
    another_article.data.append(article_data)
    session.commit()
    session.add(article)

    article_data = session.get(ArticleData, 1)
    ad_dict = article_data.to_dict()

    assert ad_dict["id"] == 1
    assert ad_dict["key"] == "key"
    assert ad_dict["value"] == "value"
    assert 1 in ad_dict["article_ids"]
    assert 2 in ad_dict["article_ids"]
