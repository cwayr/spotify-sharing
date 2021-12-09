from unittest import TestCase
from models import db, User, Group
from app import app

app.config.from_object('config.TestingConfig')


class TestGroupRoutes(TestCase):
    """Testing signup and login routes."""

    def setUp(self):
        self.client = app.test_client()
        db.drop_all()
        db.create_all()

        self.test_user = User(full_name='Test User', username='testuser', password='password')
        self.test_user2 = User(full_name='Test User Jr.', username='testuserjr', password='passwordjr')
        db.session.add(self.test_user, self.test_user2)
        db.session.commit()

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

