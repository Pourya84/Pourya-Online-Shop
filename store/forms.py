from django import forms
from .models import Product, Comment
import re


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "digital",
            "image",
            "description",
            "categories",
            "is_available",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "نام محصول"}
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "placeholder": "قیمت"}
            ),
            "digital": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "توضیحات محصول",
                }
            ),
            "categories": forms.CheckboxSelectMultiple(),
            "is_available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "name": "نام محصول",
            "price": "قیمت (تومان)",
            "digital": "محصول دیجیتال",
            "image": "تصویر محصول",
            "description": "توضیحات",
            "categories": "دسته‌بندی‌ها",
            "is_available": "محصول موجود است ",
        }

    def clean_store_name(self):
        store_name = self.cleaned_data.get("store_name")
        if store_name:
            if len(store_name) < 3:
                raise forms.ValidationError("Store name is too short.")

            if len(store_name) > 100:
                raise forms.ValidationError("Store name is too long.")

            if not re.match(r"^[\w\s\-]+$", store_name):
                raise forms.ValidationError("Invalid store name.")

        return store_name

    def clean(self):
        cleaned_data = super().clean()
        digital = cleaned_data.get("digital")
        image = cleaned_data.get("image")
        if not digital and not image:
            raise forms.ValidationError("Physical products need an image.")
        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 3:
            raise forms.ValidationError("Product name is too short.")
        if len(name) > 200:
            raise forms.ValidationError("Product name is too long.")
        return name


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "نظر خود را بنویسید...",
                }
            ),
        }
        labels = {
            "text": "متن نظر",
        }

    def clean_text(self):
        text = self.cleaned_data["text"].strip()
        if len(text) < 3:
            raise forms.ValidationError("Comment is too short.")
        if len(text) > 1000:
            raise forms.ValidationError("Comment is too long.")
        return text