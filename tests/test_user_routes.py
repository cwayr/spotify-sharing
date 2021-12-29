from unittest import TestCase
from models import db, User, Group, UserGroup
from app import app

app.config.from_object('config.TestingConfig')


class TestUserRoutes(TestCase):
    """Testing user routes."""

    def setUp(self):
        self.client = app.test_client()
        db.drop_all()
        db.create_all()

        self.test_user = User(full_name='Test User', username='testuser', password='password')
        db.session.add(self.test_user)
        db.session.commit()

        self.test_user2 = User(full_name='Test User Jr', username='testuserjr', password='passwordjr')
        db.session.add(self.test_user2)
        db.session.commit()

        print('user2:', self.test_user2)

    def tearDown(self):
        db.session.rollback()
        return super().tearDown()


    def test_profile_content(self):
        """Test that profile page displays correct content."""

        with app.test_client() as client:
            # create test groups
            self.test_group = Group(name='Test Group', description='A group for testing', admin_id=1)
            db.session.add(self.test_group)
            db.session.commit()

            self.test_group = Group(name='Test Group 2', description='Another group for testing', admin_id=2)
            db.session.add(self.test_group)
            db.session.commit()

            user_group = UserGroup(user_id=2, group_id=1)
            db.session.add(user_group)
            db.session.commit()

            resp = client.get('/user/2')
            html = resp.get_data(as_text=True)

            self.assertIn('<h1>Test User Jr</h1>', html)
            self.assertIn('<h3>@testuserjr</h3>', html)

            self.assertIn('<h3>Test Group 2</h3>', html)
            self.assertIn('<h3>Test Group</h3', html)


    def test_edit_user(self):
        """Test editing user details works."""

        with app.test_client() as client:
            # follow_redirects=false
            resp = client.post('/user/2/edit', data = {'full_name': 'Test User III', 'username': 'testuserIII', 'introduction': 'Imma test user'})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)

            # follow_redirects=true
            redirect_resp = client.post('/user/2/edit', data = {'full_name': 'Test User III', 'username': 'testuserIII', 'introduction': 'Imma test user'}, follow_redirects=True)
            html = redirect_resp.get_data(as_text=True)

            self.assertEqual(redirect_resp.status_code, 200)
            self.assertIn("Test User III", html)
            self.assertIn("testuserIII", html)
            self.assertIn("Imma test user", html)

            # check db
            user = User.query.filter_by(id=2).first()

            self.assertEqual(user.introduction, "Imma test user")


    def test_create_new_group_route(self):
        """Test that new group is created."""

        with app.test_client() as client:
            # follow_redirects=false
            resp = client.post('/user/1/new-group', data={
                'name': 'My Test Group',
                'description': 'A very descriptive description.'
            })

            self.assertEqual(resp.status_code, 302)

            # follow_redirects=true
            redirect_resp = client.post('/user/1/new-group', data={
                'name': 'My Test Group 2',
                'description': 'Another very descriptive description.'
                }, follow_redirects=True)
            html = redirect_resp.get_data(as_text=True)

            self.assertEqual(redirect_resp.status_code, 200)
            self.assertIn('Test User', html)