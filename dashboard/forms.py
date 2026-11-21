from django import forms
from django.utils.text import slugify

from catalog.models import Brand, Category, Product


class SimpleCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", "accent", "is_active"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.name)
        if commit:
            instance.save()
        return instance


class SimpleBrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["name", "is_active"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.name)
        if commit:
            instance.save()
        return instance


class SimpleProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "brand", "category", "description", "price", "stock_quantity", "image_url", "is_active", "is_featured"]
        widgets = {"description": forms.Textarea(attrs={"rows": 4}), "image_url": forms.URLInput(attrs={"placeholder": "https://... (optional)"})}

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.name)
        if commit:
            instance.save()
        return instance
