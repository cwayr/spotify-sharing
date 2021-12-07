from unittest import TestCase
from models import db, User
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

    def tearDown(self):
        db.session.rollback()
        return super().tearDown()


    def test_profile_content(self):
        """Test that profile page displays correct content."""

        with app.test_client() as client:
            resp = client.get('/user/1')
            html = resp.get_data(as_text=True)

            self.assertIn('Test User', html)
            self.assertIn('@testuser', html)


    def test_create_new_group_route(self):
        """Test that new group is created."""

        with app.test_client() as client:
            # follow_redirects=false
            resp = client.post('/user/1/group', data={
                'name': 'Test Group',
                'description': 'A very descriptive description.'
            })

            self.assertEqual(resp.status_code, 302)

            # follow_redirects=true
            redirect_resp = client.post('/user/1/group', data={'name': 'Test Group 2', 'description': 'Another very descriptive description.'}, follow_redirects=True)
            html = redirect_resp.get_data(as_text=True)

            self.assertEqual(redirect_resp.status_code, 200)
            self.assertIn('Test User', html)