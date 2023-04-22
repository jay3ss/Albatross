# import urllib.parse

# from flask import url_for


# def test_user_homepage(client):
#     # Test case 1: User with a valid username
#     response = client.get(url_for("user.homepage", username="testuser"))
#     assert response.status_code == 200
#     # Assert that the response contains the username
#     assert "testuser" in response.text

#     # Test case 2: User with a valid username containing special characters
#     response = client.get(url_for("user.homepage", username="test.user"))
#     assert response.status_code == 200
#     # Assert that the response contains the username
#     assert "test.user" in response.text

#     # Test case 3: User with an invalid username containing URL-encoded @ character
#     encoded_username = urllib.parse.quote("@invalid_user")
#     response = client.get(url_for("user.homepage", username=encoded_username))
#     # Assert that the response returns a 404 status code
#     assert response.status_code == 404

#     # Test case 4: User with an invalid username containing unencoded @ character
#     response = client.get(url_for("user.homepage", username="@invalid_user"))
#     # Assert that the response returns a 404 status code
#     assert response.status_code == 404

#     # Test case 5: User with a valid username with trailing slash
#     response = client.get(url_for("user.homepage", username="testuser/"))
#     # Assert that the response returns a 404 status code
#     assert response.status_code == 404

#     # Test case 6: User with a valid username with URL-encoded @ character and trailing slash
#     encoded_username = urllib.parse.quote("@testuser/")
#     response = client.get(url_for("user.homepage", username=encoded_username))
#     # Assert that the response returns a 404 status code
#     assert response.status_code == 404

#     # Test case 7: User with an invalid username with URL-encoded @ character and trailing slash
#     encoded_username = urllib.parse.quote("@invalid_user/")
#     response = client.get(url_for("user.homepage", username=encoded_username))
#     # Assert that the response returns a 404 status code
#     assert response.status_code == 404

#     # Test case 8: User with an invalid username with unencoded @ character and trailing slash
#     response = client.get(url_for("user.homepage", username="@invalid_user/"))
#     # Assert that the response returns a 404 status code
#     assert response.status_code == 404

#     # Test case 9: User with an empty username
#     response = client.get(url_for("user.homepage", username=""))
#     # Assert that the response returns a 404 status code
#     assert response.status_code == 404

#     # Test case 10: User with a valid username with trailing slashes
#     response = client.get(url_for("user.homepage", username="testuser//"))
#     # Assert that the response returns a 404 status code
#     assert response.status_code == 404

#     # Test case 11: User with a valid username with multiple URL-encoded @ characters
#     encoded_username = urllib.parse.quote("@testuser@")
#     response = client.get(url_for("user.homepage", username=encoded_username))
#     # Assert that the response returns a 404 status code
#     assert response.status_code == 404
