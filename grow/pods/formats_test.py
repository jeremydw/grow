from . import formats
from grow.pods import pods
from grow.testing import testing
import textwrap
import unittest


class FormatsTestCase(unittest.TestCase):

    def setUp(self):
        dir_path = testing.create_test_pod_dir()
        self.pod = pods.Pod(dir_path)

    def test_markdown(self):
        doc = self.pod.get_doc('/content/pages/intro.md')
        self.assertEqual('<p>About page.</p>', doc.html)
        self.assertEqual('About page.', doc.body)

    def test_locales(self):
        path = '/content/localized/multiple-locales.yaml'
        doc = self.pod.get_doc(path)
        self.assertEqual('base', doc.foo)
        de_doc = self.pod.get_doc(path, locale='de')
        self.assertEqual('de', de_doc.foo)
        it_doc = self.pod.get_doc(path, locale='it')
        self.assertEqual('it_fr', it_doc.foo)
        fr_doc = self.pod.get_doc(path, locale='fr')
        self.assertEqual('it_fr', fr_doc.foo)

    def test_yaml(self):
        doc = self.pod.get_doc('/content/pages/home.yaml')
        self.assertEqual('bar', doc.fields['foo'])

        doc = self.pod.get_doc('/content/pages/about.yaml')
        self.assertEqual('bar', doc.foo)
        doc = self.pod.get_doc('/content/pages/about.yaml', locale='de')
        body = (
            '$locale: de\n'
            '$title@: AboutDE\n'
            'foo: baz'
        )
        self.assertEqual(body, doc.body)
        self.assertEqual('baz', doc.foo)

    def test_html(self):
        doc = self.pod.get_doc('/content/pages/html.html')
        self.assertEqual('HTML Page', doc.title)
        self.assertEqual('<div>HTML Content.</div>', doc.body)
        content = (
            '---\n'
            '$title@: HTML Page\n'
            '$hidden: true\n'
            '---\n'
            '<div>HTML Content.</div>\n'
        )
        self.assertEqual(content, doc.content)

    def test_update(self):
        content = (
            '---\n'
            'foo: bar\n'
            '---\n'
            'Body\n'
        )
        new_content = formats.Format.update(content)
        self.assertEqual(content, new_content)

        fields = {'qaz': 'qux'}
        expected = (
            '---\n'
            'qaz: qux\n'
            '---\n'
            'Body\n'
        )
        new_content = formats.Format.update(content, fields=fields)
        self.assertEqual(expected, new_content)

        body = 'Updated body\n'
        expected = (
            '---\n'
            'foo: bar\n'
            '---\n'
            'Updated body\n'
        )
        new_content = formats.Format.update(content, body=body)
        self.assertEqual(expected, new_content)

    def test_parse_localized_path(self):
        path = '/content/pages/file@locale.ext'
        expected = ('/content/pages/file.ext', 'locale')
        self.assertEqual(expected, formats.Format.parse_localized_path(path))
        path = '/content/pages/file.ext'
        expected = ('/content/pages/file.ext', None)
        self.assertEqual(expected, formats.Format.parse_localized_path(path))

    def test_localize_path(self):
        path = '/content/pages/file.ext'
        locale = 'locale'
        expected = '/content/pages/file@locale.ext'
        self.assertEqual(
            expected, formats.Format.localize_path(path, locale=locale))

    def test_encoding(self):
        pod = testing.create_pod()
        pod.write_yaml('/podspec.yaml', {})
        pod.write_yaml('/content/pages/_blueprint.yaml', {
            '$path': '/{base}/',
            '$view': '/views/base.html',
        })
        pod.write_file('/content/pages/test.yaml', textwrap.dedent(
            """\
            foo: \u201Cbar\u201D
            """
        ))
        pod.write_file('/views/base.html', '{{doc.foo}}')
        controller, params = pod.match('/test/')
        content = controller.render(params)
        self.assertEqual('bar', content)


if __name__ == '__main__':
    unittest.main()
