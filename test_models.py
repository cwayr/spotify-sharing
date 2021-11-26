"""Model tests."""

from unittest import TestCase
from models import db, User, Group, UserGroup, Post
from app import app

app.config.from_object('config.TestingConfig')


class UserModelTestCase(TestCase):
    """Test case for the user model."""

    def setUp(self):
        """Create test client and add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        # add 3 users
        user_1 = User(full_name="User 1", username="user1", password="password1")
        user_2 = User(full_name="User 2", username="user2", password="password2")
        user_3 = User(full_name="User 3", username="user3", password="password3")

        db.session.add_all([user_1, user_2, user_3])
        db.session.commit()

        # add 2 groups
        group_1 = Group(name="Group 1", description="Group 1 description", admin_id=1)
        group_2 = Group(name="Group 2", description="Group 2 description" , admin_id=2)

        db.session.add_all([group_1, group_2])
        db.session.commit()

        # add users to groups
        user_group_1 = UserGroup(user_id=1, group_id=1)
        user_group_2 = UserGroup(user_id=2, group_id=1)
        user_group_2a = UserGroup(user_id=2, group_id=2)
        user_group_3 = UserGroup(user_id=3, group_id=2)

        db.session.add_all([user_group_1, user_group_2, user_group_2a, user_group_3])
        db.session.commit()

        # add posts to groups
        post_1 = Post(content="Post 1 content", user_id=1, group_id=1, spotify_id=100)
        post_2 = Post(content="Post 2 content", user_id=2, group_id=1, is_reply=True, reply_to = 1)
        post_3 = Post(content="Post 3 content", user_id=3, group_id=2)

        db.session.add_all([post_1, post_2, post_3])
        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_user_model(self):
        """Test user model."""

        get_all_users = User.query.all()
        self.assertEqual(len(get_all_users), 3)

        get_user_1 = User.query.get_or_404(1)
        self.assertEqual(get_user_1.full_name, "User 1")

        get_user_2_pw = User.query.get_or_404(2).password
        self.assertEqual(get_user_2_pw, "password2")


    def test_group_model(self):
        """Test group model."""

        get_all_groups = Group.query.all()
        self.assertEqual(len(get_all_groups), 2)

        get_group_1 = Group.query.get_or_404(1)
        self.assertEqual(get_group_1.name, "Group 1")

        get_group_2_desc = Group.query.get_or_404(2).description
        self.assertEqual(get_group_2_desc, "Group 2 description")

        get_group_2_admin = Group.query.get_or_404(2).admin_id
        self.assertEqual(get_group_2_admin, 2)


    def test_user_group_model(self):
        """Test user group model."""

        get_all_user_groups = UserGroup.query.all()
        self.assertEqual(len(get_all_user_groups), 4)

        get_user_1_groups = UserGroup.query.filter_by(user_id=1).all()
        self.assertEqual(len(get_user_1_groups), 1)


    def test_post_model(self):
        """Test post model."""

        get_all_posts = Post.query.all()
        self.assertEqual(len(get_all_posts), 3)

        get_user_1_posts = Post.query.filter_by(user_id=1).all()
        self.assertEqual(len(get_user_1_posts), 1)

        get_group_1_posts = Post.query.filter_by(group_id=1).all()
        self.assertEqual(len(get_group_1_posts), 2)

        get_post_2 = Post.query.get_or_404(2)
        self.assertEqual(get_post_2.content, "Post 2 content")

        get_post_2_reply_to = Post.query.get_or_404(2).reply_to
        self.assertEqual(get_post_2_reply_to, 1)

        get_post_2_is_reply = Post.query.get_or_404(2).is_reply
        self.assertEqual(get_post_2_is_reply, True)


