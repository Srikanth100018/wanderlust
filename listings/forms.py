from django import forms
from .models import Listing, Review


class ListingForm(forms.ModelForm):
    GEOMETRY_TYPE_CHOICES = [
        ("Point", "Point"),
        ("LineString", "LineString"),
        ("Polygon", "Polygon"),
    ]

    geometry_type = forms.ChoiceField(
        choices=GEOMETRY_TYPE_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-control"
        }),
        required=True,
        label="Geometry Type"
    )

    geometry_coordinates = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Enter geometry coordinates (e.g., [12.9716, 77.5946])",
            "rows": 3
        }),
        required=True,
        label="Geometry Coordinates"
    )

    class Meta:
        model = Listing
        # include the new fields too
        fields = [
            "title",
            "description",
            "price",
            "location",
            "country",
            "image_url",
            "image_filename",
            "geometry_type",
            "geometry_coordinates",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Enter title"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter description",
                "rows": 4
            }),
            "price": forms.NumberInput(attrs={
                "type": "number",
                "class": "form-control",
                "placeholder": "Enter price"
            }),
            "location": forms.TextInput(attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Enter location"
            }),
            "country": forms.TextInput(attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Enter country"
            }),
            "image_url": forms.URLInput(attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Paste image URL or leave blank"
            }),
            "image_filename": forms.TextInput(attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Filename (optional, usually auto-filled)"
            }),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]

        widgets = {
            "rating": forms.NumberInput(attrs={
                "type": "number",
                "class": "form-control",
                "min": 1,
                "max": 5,
                "placeholder": "Rating (1–5)"
            }),
            "comment": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Write your review...",
                "rows": 3
            }),
        }
