from django import forms


class ResearchFood(forms.Form):
    research_food = forms.CharField(label="Produits", max_length=100)
