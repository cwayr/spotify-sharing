from unittest import TestCase
from models import db, User, Group, UserGroup, Post, Likes
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


    def test_group_view(self):
        """Test group page displays correctly."""

        with app.test_client() as client:
            resp = client.get('/user/1/group/1')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test Group</h1>", html)


    def test_admin_group_view(self):
        """Test group page displays correctly to admin."""

        with app.test_client() as client:
            resp = client.get('/user/1/group/1')
            html = resp.get_data(as_text=True)

            self.assertIn("Edit group", html)

    # test_create_group located in 'test_user_routes' because it is a functionality used from the user home page.


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
            user3_in_group = UserGroup.query.filter_by(user_id=3).count()
            user_group_len = UserGroup.query.filter_by(group_id=1).count()

            self.assertEqual(user3_in_group, 1)
            self.assertEqual(user_group_len, 2)


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
            user3_in_group = UserGroup.query.filter_by(user_id=3).count()

            self.assertEqual(user3_in_group, 1)

            client.delete('/user/3/group/1/leave')
            user3_not_in_group = UserGroup.query.filter_by(user_id=3).count()

            self.assertEqual(user3_not_in_group, 0)


    def test_edit_group(self):
        """Test editing a group works."""

        with app.test_client() as client:
            # follow_redirects=false
            resp = client.post('/user/1/group/1/edit', data = {'name': 'Test Group', 'description': 'Is the group really for testing?'})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)

            # follow_redirects=true
            redirect_resp = client.post('/user/1/group/1/edit', data = {'name': 'Test Group Edited', 'description': 'It really is for testing!'}, follow_redirects=True)
            html = redirect_resp.get_data(as_text=True)

            self.assertEqual(redirect_resp.status_code, 200)
            self.assertIn("Edit group", html)

            # check db
            group = Group.query.filter_by(id=1).first()

            self.assertEqual(group.name, 'Test Group Edited')
            self.assertEqual(group.description, "It really is for testing!")


    def test_delete_group(self):
        """Test deleting a group works."""

        with app.test_client() as client:
            # follow_redirects=true
            redirect_resp = client.delete('/user/1/group/1/delete', follow_redirects=True)
            html = redirect_resp.get_data(as_text=True)

            self.assertEqual(redirect_resp.status_code, 200)
            self.assertIn("Browse groups", html)

            # check db
            group = Group.query.filter_by(id=1).first()
            self.assertEqual(group, None)


    def test_post_in_group(self):
        """Test posting in a group works."""

        with app.test_client() as client:

            client.post('/user/2/group/1/join')

        # post without song
            # follow_redirects=false
            resp = client.post('/user/2/group/1/post', data = {'content': 'This is a test post!'})

            self.assertEqual(resp.status_code, 302)

            # follow_redirects=true
            redirect_resp = client.post('/user/2/group/1/post', data = {'content': 'This is a test post!'}, follow_redirects=True)
            html = redirect_resp.get_data(as_text=True)

            self.assertEqual(redirect_resp.status_code, 200)
            self.assertIn('testuserjr', html)
            self.assertIn('This is a test post!', html)

            # check db
            post = Post.query.filter_by(id=1).first()

            self.assertEqual(post.content, 'This is a test post!')
            self.assertEqual(post.user_id, 2)


    def test_post_song_in_group(self):
        """Test posting a song in a group works."""

        with app.test_client() as client:
            with app.test_request_context():
                with client.session_transaction() as sess:
                    sess['track_image'] = 'song_image'
                    sess['track_name'] = 'song_name'
                    sess['track_artist'] = 'song_artist'
                    sess['track_link'] = 'song_link'
                    sess['track_preview'] = 'song_preview'

                # follow_redirects=true
                song_resp = client.post('/user/2/group/1/post', data = {'content': 'Check out this one!'})
                song_html = song_resp.get_data(as_text=True)

                self.assertEqual(song_resp.status_code, 200)
                self.assertIn('testuserjr', song_html)
                self.assertIn('song_image', song_html)

                # check db
                song_post = Post.query.filter_by(content='Check out this one!').first()

                self.assertEqual(song_post.s_image, 'song_image')
                self.assertEqual(song_post.s_name, 'song_name')
                self.assertEqual(song_post.s_artist, 'song_artist')
                self.assertEqual(song_post.s_link, 'song_link')
                self.assertEqual(song_post.s_preview, 'song_preview')

            yield client


    def test_likes(self):
        """Test liking and unliking a post works."""

        with app.test_client() as client:
            # display like button
            client.post('/user/2/group/1/join')
            client.post('/user/2/group/1/post', data = {'content': 'Like this post'})

            post_author_res = client.get('/user/2/group/1')
            post_author_html = post_author_res.get_data(as_text=True)
            post_viewer_res = client.get('/user/1/group/1')
            post_viewer_html = post_viewer_res.get_data(as_text=True)

            self.assertNotIn('fa-heart', post_author_html)
            self.assertIn('far fa-heart', post_viewer_html)

            # like post
            post_id = Post.query.filter_by(content='Like this post').first().id
            like_post_res = client.post(f'/user/1/group/1/{post_id}/like', follow_redirects=True)
            like_post_html = like_post_res.get_data(as_text=True)

            self.assertIn("1 like", like_post_html)
            self.assertIn("fas fa-heart", like_post_html)

            # (check db)
            like = Likes.query.filter_by(id=1).first()
            self.assertEqual(like.user_id, 1)
            self.assertEqual(like.post_id, post_id)

            # unlike post
            unlike_post_res = client.delete(f'/user/1/group/1/{post_id}/unlike', follow_redirects=True)
            unlike_post_html = unlike_post_res.get_data(as_text=True)

            self.assertNotIn("1 like", unlike_post_html)
            self.assertIn("far fa-heart", unlike_post_html)

            # (check db)
            again_like = Likes.query.filter_by(id=1).first()
            self.assertEqual(again_like, None)


class TestSpotifyAPI(TestCase):
    """Testing spotify routes."""

    def setUp(self):
        self.client = app.test_client()
        db.drop_all()
        db.create_all()

        # create test user
        self.test_user = User(full_name='Test User', username='testuser', password='password')
        db.session.add(self.test_user)
        db.session.commit()

        # create test group (user 1 admin)
        self.test_group = Group(name='Test Group', description='A group for testing', admin_id=1)
        db.session.add(self.test_group)
        db.session.commit()


    def tearDown(self):
        db.session.rollback()
        return super().tearDown()


    def test_search_spotify_route(self):
        """Test search-spotify modal works."""

        with app.test_client() as client:
            resp = client.get('/user/1/group/1/search_spotify')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Search for songs", html)


    def test_spotify_api(self):
        """Test search of the spotify api."""

        with app.test_client() as client:
            resp = client.post('/user/1/group/1/search_spotify', data={'query': 'time'})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("time", html)
            self.assertIn('<div class="spotify-search-res">', html)