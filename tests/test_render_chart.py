import json
import re
import unittest
from unittest.mock import Mock

from django.conf import settings
from django.template import Context, Engine

from django_altair.templatetags.django_altair import render_chart


if not settings.configured:
    settings.configure()


class RenderChartTests(unittest.TestCase):
    def render_spec(self, spec):
        return str(render_chart(Mock(to_dict=Mock(return_value=spec))))

    def extract_spec(self, html):
        encoded = re.search(r'JSON.parse\((".*")\)', html).group(1)
        return json.loads(json.loads(encoded))

    def test_script_breakout_and_template_syntax_remain_data(self):
        value = '</script><script>alert("x")</script>{% invalid_tag %}{{ secret }}'
        html = self.render_spec({"title": value})
        self.assertEqual(html.count("<script "), 1)
        self.assertEqual(html.count("</script>"), 1)
        self.assertNotIn('<script>alert', html)
        self.assertEqual(self.extract_spec(html), {"title": value})

    def test_unicode_quotes_and_backslashes_round_trip(self):
        spec = {"title": "Waray • 日本語 \u2028 \u2029 ' \" \\ & < >"}
        self.assertEqual(self.extract_spec(self.render_spec(spec)), spec)

    def test_multiple_charts_have_independent_targets(self):
        first = self.render_spec({"title": "First"})
        second = self.render_spec({"title": "Second"})
        first_id = re.search(r'<div id="([^"]+)"', first).group(1)
        second_id = re.search(r'<div id="([^"]+)"', second).group(1)
        self.assertNotEqual(first_id, second_id)
        self.assertEqual(first.count(first_id), 2)
        self.assertEqual(second.count(second_id), 2)

    def test_tag_output_renders_as_html_in_a_django_template(self):
        engine = Engine(libraries={
            "django_altair": "django_altair.templatetags.django_altair",
        })
        template = engine.from_string("{% load django_altair %}{% render_chart chart %}")
        html = template.render(Context({"chart": Mock(to_dict=Mock(return_value={"mark": "bar"}))}))
        self.assertIn('<div id="chart_', html)
        self.assertNotIn("&lt;script", html)
        self.assertEqual(self.extract_spec(html), {"mark": "bar"})


if __name__ == "__main__":
    unittest.main()
