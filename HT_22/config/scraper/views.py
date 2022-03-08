from datetime import datetime

from django.shortcuts import render

from . import forms
from . import utils
from . import tasks


def index(request):
    if request.method == "POST":
        selecta_form = forms.SelectRubricForm(request.POST)

        if selecta_form.is_valid():
            rubric_id = int(selecta_form.cleaned_data['rubric'])
            rubric_name = utils.CHOICES[rubric_id][1]

            context = {
                "message": f"Начало cбора данных по рубрике: {rubric_name}",
                "form": selecta_form,
                "date": datetime.now(),
            }

            tasks.start_scraping.delay(rubric_name)

            return render(request, "./scraper/index.html", context)
        else:
            context = {
                "form": selecta_form,
                "date": datetime.now(),
            }
            return render(request, "./scraper/index.html", context)

    else:
        selecta_form = forms.SelectRubricForm()
        context = {
            "form": selecta_form,
            "date": datetime.now(),
        }
        return render(request, "./scraper/index.html", context)
