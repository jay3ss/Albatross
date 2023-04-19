import re
import unittest

from slugify import slugify

from app.helpers import articles as ah


class SlugGenerationTests(unittest.TestCase):

    def test_generate_slug_from_title(self):
        title = "This is a Sample Title"
        slug = ah.generate_slug(title)
        title_slug = slugify(title)
        self.assertRegex(slug, rf'^{re.escape(title_slug)}-[a-f0-9]{{8}}$')

    def test_generate_unique_slugs(self):
        title = "This is a Sample Title"
        slug1 = ah.generate_slug(title)
        slug2 = ah.generate_slug(title)
        self.assertNotEqual(slug1, slug2)

    def test_generate_slug_strips_non_alphanumeric_chars(self):
        title = "This is a Sample Title!!"
        slug = ah.generate_slug(title)
        title_slug = slugify(title)
        self.assertRegex(slug, rf'^{re.escape(title_slug)}-[a-f0-9]{{8}}$')

    def test_generate_slug_contains_uuid_part(self):
        title = "This is a Sample Title"
        slug = ah.generate_slug(title)
        self.assertRegex(slug, r'^[a-z0-9-]+-[a-f0-9]{8}$')

    def test_generate_slug_from_non_english_title(self):
        title = "これは日本語のタイトルです"
        slug = ah.generate_slug(title)
        title_slug = slugify(title)
        self.assertRegex(slug, rf'^{re.escape(title_slug)}-[a-f0-9]{{8}}$')

    def test_generate_slug_from_non_english_title_with_spaces(self):
        title = "Это тестовый заголовок на русском языке с пробелами"
        slug = ah.generate_slug(title)
        title_slug = slugify(title)
        self.assertRegex(slug, rf'^{re.escape(title_slug)}-[a-f0-9]{{8}}$')


if __name__ == '__main__':
    unittest.main()
