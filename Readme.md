# Django Altair

A small Django template tag for embedding interactive Altair charts in existing Django pages.

## Installation

From a checkout of this repository:

```sh
python -m pip install . altair
```

The template tag accepts an object with a `to_dict()` method. Altair is needed by your application to create charts; the tag itself only depends on Django.

## Usage

Add `django_altair` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "django_altair",
]
```

Create a chart in your view and pass matching JavaScript runtime versions to the template:

```python
import altair as alt
from django.shortcuts import render


def index(request):
    chart = alt.Chart(alt.Data(values=[
        {"category": "A", "value": 28},
        {"category": "B", "value": 55},
    ])).mark_bar().encode(x="category:N", y="value:Q")
    return render(request, "index.html", {
        "chart": chart,
        "vega_version": alt.VEGA_VERSION,
        "vegalite_version": alt.VEGALITE_VERSION,
        "vegaembed_version": alt.VEGAEMBED_VERSION,
    })
```

Include the matching runtimes once, before rendering charts:

```html
{% load django_altair %}
<script src="https://cdn.jsdelivr.net/npm/vega@{{ vega_version }}"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-lite@{{ vegalite_version }}"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-embed@{{ vegaembed_version }}"></script>

{% render_chart chart %}
```

You can call `render_chart` multiple times on the same page. Each chart receives its own target and JavaScript scope. Chart values are serialized as data, including strings containing HTML or Django template syntax.

For production, pin or self-host the matching JavaScript assets according to your application's deployment policy. The tag emits an inline script; a Content Security Policy must allow it. This is not a sanitizer for arbitrary, untrusted Vega specifications, which can include external data URLs and other renderer features.

See Altair's [HTML embedding documentation](https://altair-viz.github.io/user_guide/saving_charts.html#html-format) for runtime details.

## Local example

```sh
python -m pip install -e . altair
cd example
python manage.py runserver
```

The example uses inline data, so no dataset download is required. The JavaScript assets require an internet connection. Its settings are for local development only.

## Tests

```sh
python -m unittest discover -s tests -v
```
