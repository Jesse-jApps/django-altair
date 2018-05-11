# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.shortcuts import render
import altair as alt
import pandas as pd
from vega_datasets import data
class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = locals()


        data3 = pd.DataFrame({
            'a': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
            'b': [28, 55, 43, 91, 81, 53, 19, 87, 52]
        })

        context['chart'] = alt.Chart(data3).mark_bar().encode(
            x='a',
            y='b'
        ).interactive()

        source = data.cars()

        context['chart2'] = alt.Chart(source).mark_circle().encode(
            x='Horsepower',
            y='Miles_per_Gallon',
            color='Origin'
        ).interactive()



        return render(request, self.template_name, context)