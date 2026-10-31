import json
from uuid import uuid4

from django import template
from django.utils.html import escapejs, format_html

register = template.Library()


TEMPLATE_CHART = """
<div id="{output_div}"></div>
<script type="text/javascript">
(function () {{
    const output = document.getElementById("{output_div}");
    const spec = JSON.parse("{spec}");
    vegaEmbed(output, spec, {{"mode": "vega-lite", "actions": false}})
        .catch(function (error) {{
            output.textContent = "JavaScript Error: " + error.message;
            console.error(error);
        }});
}})();
</script>
"""

@register.simple_tag(name='render_chart')
def render_chart(chart):
    # Treat chart values as data, never as Django templates or executable HTML.
    return format_html(
        TEMPLATE_CHART,
        output_div="chart_" + uuid4().hex,
        spec=escapejs(json.dumps(chart.to_dict())),
    )
