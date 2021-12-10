from unittest import TestCase
from models import db, User, Group, UserGroup
from app import app

app.config.from_object('config.TestingConfig')


class TestGroupRoutes(TestCase):
    """Testing signup and login routes."""

    def setUp(self):
        self.client = app.test_client()
        db.drop_all()
        db.create_all()

        # create three test users
        self.test_user = User(full_name='Test User', username='testuser', password='password')
        db.session.add(self.test_user)
        db.session.commit()

        self.test_user2 = User(full_name='Test User Jr.', username='testuserjr', password='passwordjr')
        db.session.add(self.test_user2)
        db.session.commit()

        self.test_user3 = User(full_name='Test User III', username='testuseriii', password='passwordiii')
        db.session.add(self.test_user3)
        db.session.commit()

        # create test group (user 1 admin)
        self.test_group = Group(name='Test Group', description='A group for testing', admin_id=1)
        db.session.add(self.test_group)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        return super().tearDown()


    def test_browse_groups(self):
        """Test browse-groups page displays correctly."""

        with app.test_client() as client:
            resp = client.get('/user/2/browse-groups')
            html = resp.get_data(as_text=True)

            self.assertIn("Test Group", html)

            resp2 = client.get("/user/1/browse-groups")
            html2 = resp2.get_data(as_text=True)

            self.assertNotIn("Test Group", html2)


    def test_group_page(self):
        """Test group page displays correctly."""

        with app.test_client() as client:
            resp = client.get('/user/1/group/1')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test Group</h1>", html)


    def test_join_group(self):
        """Test joining a group works."""

        with app.test_client() as client:
            # follow_redirects=false
            resp = client.post('/user/2/group/1/join')

            self.assertEqual(resp.status_code, 302)

            # follow_redirects=true
            redirect_resp = client.post('/user/3/group/1/join', follow_redirects=True)
            html = redirect_resp.get_data(as_text=True)

            self.assertEqual(redirect_resp.status_code, 200)
            self.assertIn('Leave group', html)

            # check db
            user3_in_group = UserGroup.query.filter_by(user_id=3).all()
            user_group_len = UserGroup.query.filter_by(group_id=1).all()

            self.assertEqual(len(user3_in_group), 1)
            self.assertEqual(len(user_group_len), 2)


    def test_leave_group(self):
        """Test leaving a group works."""

        with app.test_client() as client:
            # follow_redirects=false
            client.post('/user/2/group/1/join')
            resp = client.delete('/user/2/group/1/leave')

            self.assertEqual(resp.status_code, 302)

            # follow_redirects=true
            client.post('/user/3/group/1/join')
            redirect_resp = client.delete('/user/3/group/1/leave', follow_redirects=True)
            html = redirect_resp.get_data(as_text=True)

            self.assertEqual(redirect_resp.status_code, 200)
            self.assertIn('Join group', html)

            # check db
            client.post('/user/3/group/1/join')
            user3_in_group = UserGroup.query.filter_by(user_id=3).all()

            self.assertEqual(len(user3_in_group), 1)

            client.delete('/user/3/group/1/leave')
            user3_not_in_group = UserGroup.query.filter_by(user_id=3).all()

            self.assertEqual(len(user3_not_in_group), 0)