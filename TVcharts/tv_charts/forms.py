from django import forms


class FilterForm(forms.Form):
    """
    Form to filter ad sort data in TvSeriesListDjango
    """
    sort_options = [('title', 'title'), ('votes', 'number of votes'), ('rating', 'rating')]
    order_options = [('', 'ascending'), ('-', 'descending')]

    starts_with = forms.CharField()
    sort_by = forms.ChoiceField(choices=sort_options)
    order = forms.ChoiceField(choices=order_options, label='')
    per_page = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].required = False
            # CSS class for bootstrap
            self.fields[i].widget.attrs['class'] = 'form-control'