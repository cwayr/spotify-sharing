from unittest import TestCase
from models import db, User
from app import app

app.config.from_object('config.TestingConfig')


class TestLandingRoutes(TestCase):
    """Testing signup and login routes."""

    def setUp(self):
        self.client = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.rollback()
        return super().tearDown()


    def test_landing_page(self):
        """Test landing page."""

        with app.test_client() as client:
            resp = client.get('/')
            self.assertEqual(resp.status_code, 302)

            redirect_resp = client.get('/', follow_redirects=True)
            html = redirect_resp.get_data(as_text=True)

            self.assertEqual(redirect_resp.status_code, 200)
            self.assertIn('<h1>Sign in to Spotify Sharing</h1>', html)


    def test_signup(self):
        """Test user_signup method."""

        new_user = User.user_signup(name='Test User', username='testuser', password='password')
        db.session.add(new_user)
        db.session.commit()

        new_user_test = User.query.get(1)

        self.assertEqual(new_user_test.username, 'testuser')


    def test_signup_route(self):
        """Test signup route."""

        with app.test_client() as client:
            # follow_redirects=false
            resp = client.post('/signup', data={
                'name': 'Test',
                'username': 'atestuser',
                'password': 'mypassword',
                'confirm_password': 'mypassword'
            }, follow_redirects=False)

            self.assertEqual(resp.status_code, 302)

            # follow_redirects=true
            redirect_resp = client.post('/signup', data={
                'name': 'Test User1',
                'username': 'testuser1',
                'password': 'password1',
                'confirm_password': 'password1'
            }, follow_redirects=True)
            html = redirect_resp.get_data(as_text=True)

            self.assertEqual(redirect_resp.status_code, 200)
            self.assertIn('<h1>Test User1</h1>', html)


    def test_login(self):
        """Test user_login method."""

        new_user = User.user_signup(name='Test User', username='testuser', password='password')
        db.session.add(new_user)
        db.session.commit()

        self.assertTrue(User.user_login(username='testuser', password='password'))
        self.assertFalse(User.user_login(username='testuser', password='wrong_password'))


    def test_login_route(self):
        """Test login route."""

        new_user = User.user_signup(name='Test User', username='testuser', password='password')
        db.session.add(new_user)
        db.session.commit()

        with app.test_client() as client:
            # follow_redirects=false
            resp = client.post('/login', data={
                'username': 'testuser',
                'password': 'password'
            })

            self.assertEqual(resp.status_code, 302)

            # follow_redirects=true
            redirect_resp = client.post('/login', data={
                'username': 'testuser',
                'password': 'password'
            }, follow_redirects=True)
            html = redirect_resp.get_data(as_text=True)

            self.assertEqual(redirect_resp.status_code, 200)
            self.assertIn('<h1>Test User</h1>', html)


    def test_logout_route(self):
        """Test logout route."""

        new_user = User.user_signup(name='Test User', username='testuser', password='password')
        db.session.add(new_user)
        db.session.commit()

        with app.test_client() as client:

            # follow_redirects=false
            resp = client.get('/logout', follow_redirects=False)

            self.assertEqual(resp.status_code, 302)

            # follow_redirects=true
            redirect_resp = client.get('/logout', follow_redirects=True)
            html = redirect_resp.get_data(as_text=True)

            self.assertEqual(redirect_resp.status_code, 200)
            self.assertIn('<h1>Sign in to Spotify Sharing</h1>', html)