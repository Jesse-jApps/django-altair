import altair as alt
from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        source = alt.Data(values=[
            {"category": "A", "value": 28},
            {"category": "B", "value": 55},
            {"category": "C", "value": 43},
            {"category": "D", "value": 91},
        ])
        chart = alt.Chart(source).mark_bar().encode(
            x="category:N", y="value:Q"
        ).interactive()
        chart2 = alt.Chart(source).mark_circle().encode(
            x="category:N", y="value:Q", color="category:N"
        ).interactive()
        return render(request, self.template_name, {
            "chart": chart,
            "chart2": chart2,
            "vega_version": alt.VEGA_VERSION,
            "vegalite_version": alt.VEGALITE_VERSION,
            "vegaembed_version": alt.VEGAEMBED_VERSION,
        })
