import requests
import json
import random
import pytest
import allure
from faker import Faker

fake = Faker()
base_url = "http://localhost:5050"

@pytest.fixture
def clear_data():
    yield
    # Cleanup after each test
    requests.delete(f"{base_url}/posts")
    requests.delete(f"{base_url}/comments")
    requests.delete(f"{base_url}/profile")

@allure.feature("Posts")
@allure.story("Create Post")
@allure.title("Test Creating a Post")
def test_create_post(clear_data):
    fake_title = fake.word()
    fake_author = fake.user_name()
    post_data = {
        "title": fake_title,
        "author": fake_author
    }
    response = requests.post(f"{base_url}/posts", json=post_data)

    assert response.status_code == 200
    created_post = response.json()

    assert created_post["title"] == fake_title
    assert created_post["author"] == fake_author

@allure.feature("Posts")
@allure.story("Get Posts")
@allure.title("Test Getting Posts")
def test_get_posts(clear_data):
    response = requests.get(f"{base_url}/posts")

    assert response.status_code == 200
    posts = response.json()

    assert isinstance(posts, list)

@allure.feature("Posts")
@allure.story("Update Post")
@allure.title("Test Updating a Post")
def test_update_post(clear_data):
    fake_title = fake.word()
    fake_author = fake.user_name()
    post_data = {
        "title": fake_title,
        "author": fake_author
    }
    create_response = requests.post(f"{base_url}/posts", json=post_data)

    assert create_response.status_code == 200
    created_post = create_response.json()

    updated_title = fake.word()
    updated_author = fake.user_name()
    updated_data = {
        "title": updated_title,
        "author": updated_author
    }
    update_response = requests.put(f"{base_url}/posts/{created_post['id']}", json=updated_data)

    assert update_response.status_code == 200
    updated_post = update_response.json()

    assert updated_post["title"] == updated_title
    assert updated_post["author"] == updated_author

@allure.feature("Posts")
@allure.story("Delete Post")
@allure.title("Test Deleting a Post")
def test_delete_post(clear_data):
    fake_title = fake.word()
    fake_author = fake.user_name()
    post_data = {
        "title": fake_title,
        "author": fake_author
    }
    create_response = requests.post(f"{base_url}/posts", json=post_data)

    assert create_response.status_code == 200
    created_post = create_response.json()

    delete_response = requests.delete(f"{base_url}/posts/{created_post['id']}")

    assert delete_response.status_code == 200
    deleted_posts = delete_response.json()

    assert isinstance(deleted_posts, list)

@allure.feature("Comment")
@allure.story("Create Comment")
@allure.title("Test creating a Comment")
def test_create_comment(clear_data):
    fake_body = fake.text()
    fake_post_id = random.randint(1, 100)
    comment_data = {
        "body": fake_body,
        "postID": fake_post_id
    }
    response = requests.post(f"{base_url}/comments", json=comment_data)

    assert response.status_code == 200
    created_comment = response.json()

    assert created_comment["body"] == fake_body
    assert created_comment["postID"] == fake_post_id

@allure.feature("Comment")
@allure.story("Get Comment")
@allure.title("Test getting a Comment")
def test_get_comments(clear_data):
    response = requests.get(f"{base_url}/comments")

    assert response.status_code == 200
    comments = response.json()

    assert isinstance(comments, list)

@allure.feature("Comment")
@allure.story("Update Comment")
@allure.title("Test Updating a Comment")
def test_update_comment(clear_data):
    fake_body = fake.text()
    fake_post_id = random.randint(1, 100)
    comment_data = {
        "body": fake_body,
        "postID": fake_post_id
    }
    create_response = requests.post(f"{base_url}/comments", json=comment_data)

    assert create_response.status_code == 200
    created_comment = create_response.json()

    updated_body = fake.text()

    updated_data = {
        "body": updated_body,
        "postID": fake_post_id
    }
    update_response = requests.put(f"{base_url}/comments/{created_comment['id']}", json=updated_data)

    assert update_response.status_code == 200
    updated_comment = update_response.json()

    assert updated_comment["body"] == updated_body
    assert updated_comment["postID"] == fake_post_id

@allure.feature("Comment")
@allure.story("Delete Comment")
@allure.title("Test Deleting a Comment")
def test_delete_comment(clear_data):
    fake_body = fake.text()
    fake_post_id = random.randint(1, 100)
    comment_data = {
        "body": fake_body,
        "postID": fake_post_id
    }
    create_response = requests.post(f"{base_url}/comments", json=comment_data)

    assert create_response.status_code == 200
    created_comment = create_response.json()

    # Delete the comment
    delete_response = requests.delete(f"{base_url}/comments/{created_comment['id']}")

    assert delete_response.status_code == 200
    deleted_comments = delete_response.json()

    assert isinstance(deleted_comments, list)

@allure.feature("Author posts")
@allure.story("Get Author posts")
@allure.title("Test Getting a Author posts")
def test_get_author_posts(clear_data):
    fake_author = fake.user_name()
    response = requests.get(f"{base_url}/posts/author/{fake_author}")

    assert response.status_code == 200
    author_posts = response.json()

    assert isinstance(author_posts, list)

@allure.feature("Post Commets")
@allure.story("Get Post Commets")
@allure.title("Test Getting a Post Commets")
def test_get_post_comments(clear_data):
    fake_post_id = random.randint(1, 100)
    response = requests.get(f"{base_url}/posts/{fake_post_id}/comments")

    assert response.status_code == 200
    post_comments = response.json()

    assert isinstance(post_comments, list)

@allure.feature("Post Commets")
@allure.story("Delete Post Commets")
@allure.title("Test Delete a Post Commets")
def test_delete_post_comments(clear_data):
    fake_post_id = random.randint(1, 100)
    response = requests.delete(f"{base_url}/comments/post/{fake_post_id}")

    assert response.status_code == 200
    deleted_comments = response.json()

    assert isinstance(deleted_comments, list)

@allure.feature("Profile")
@allure.story("Create Profile")
@allure.title("Test Creating a Profile")
def test_create_profile(clear_data):
    fake_name = fake.name()
    profile_data = {
        "name": fake_name
    }
    response = requests.post(f"{base_url}/profile", json=profile_data)

    assert response.status_code == 200
    created_profile = response.json()

    assert created_profile["name"] == fake_name

@allure.feature("Profile")
@allure.story("Get Profile")
@allure.title("Test Getting a Profile")
def test_get_profile(clear_data):
    response = requests.get(f"{base_url}/profile")

    assert response.status_code == 200
    profile = response.json()

    assert isinstance(profile, dict)

@allure.feature("Profile")
@allure.story("Update Profile")
@allure.title("Test Updating a Profile")
def test_update_profile(clear_data):
    fake_name = fake.name()
    profile_data = {
        "name": fake_name
    }
    create_response = requests.post(f"{base_url}/profile", json=profile_data)

    assert create_response.status_code == 200
    created_profile = create_response.json()

    updated_name = fake.name()
    updated_data = {
        "name": updated_name
    }
    update_response = requests.put(f"{base_url}/profile", json=updated_data)

    assert update_response.status_code == 200
    updated_profile = update_response.json()

    assert updated_profile["name"] == updated_name

@allure.feature("Profile")
@allure.story("Delete Profile")
@allure.title("Test Deleting a Profile")
def test_delete_profile(clear_data):
    response = requests.delete(f"{base_url}/profile")

    assert response.status_code == 200
    deleted_profile = response.json()

    assert isinstance(deleted_profile, dict)

@allure.feature("Post multiple times")
@allure.story("Create Post multiple times")
@allure.title("Test Creating a Post multiple times")
def test_create_post_multiple_times(clear_data):
    for _ in range(5):
        test_create_post(clear_data)

@allure.feature("Comment multiple times")
@allure.story("Create Comment multiple times")
@allure.title("Test Creating a Comment multiple times")
def test_create_comment_multiple_times(clear_data):
    for _ in range(5):
        test_create_comment(clear_data)

@allure.feature("Profile multiple times")
@allure.story("Create Profile multiple times")
@allure.title("Test Creating a Profile multiple times")
def test_create_profile_multiple_times(clear_data):
    for _ in range(5):
        test_create_profile(clear_data)

@allure.feature("Post and Comment")
@allure.story("Create Post and Comment")
@allure.title("Test Creating a Post and Comment")
def test_create_post_and_comment(clear_data):
    fake_title = fake.word()
    fake_author = fake.user_name()
    post_data = {
        "title": fake_title,
        "author": fake_author
    }
    response_post = requests.post(f"{base_url}/posts", json=post_data)
    assert response_post.status_code == 200
    created_post = response_post.json()

    fake_body = fake.text()
    comment_data = {
        "body": fake_body,
        "postID": created_post['id']
    }
    response_comment = requests.post(f"{base_url}/comments", json=comment_data)
    assert response_comment.status_code == 200
    created_comment = response_comment.json()

    assert created_comment["postID"] == created_post['id']

@allure.feature("Delete Comment")
@allure.story("Get Delete Comment")
@allure.title("Test Getting a Delete Comment")
def test_get_and_delete_comment(clear_data=None):
    fake_body = fake.text()
    fake_post_id = random.randint(1, 100)
    comment_data = {
        "body": fake_body,
        "postID": fake_post_id
    }
    response_create_comment = requests.post(f"{base_url}/comments", json=comment_data)
    assert response_create_comment.status_code == 200
    created_comment = response_create_comment.json()

    response_get_comment = requests.get(f"{base_url}/comments/{created_comment['id']}")
    assert response_get_comment.status_code == 200
    retrieved_comment = response_get_comment.json()

    assert retrieved_comment == created_comment

    response_delete_comment = requests.delete(f"{base_url}/comments/{created_comment['id']}")
    assert response_delete_comment.status_code == 200

    response_get_deleted_comment = requests.get(f"{base_url}/comments/{created_comment['id']}")
    assert response_get_deleted_comment.status_code == 200
    assert response_get_deleted_comment.json() == {"id": 0, "body": "", "postID": 0}

#Start all tests
#pytest -v test_api.py