from . import BaseTestClass


class BlogClientTestCase(BaseTestClass):

    def test_index_with_no_posts(self):
        res = self.client.get('/')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'No hay posts en el blog', res.data)

    def test_show_post(self):
        res = self.client.get('/p/1/')
        self.assertEqual(404, res.status_code)
        self.assertIn(b'no existe.', res.data)