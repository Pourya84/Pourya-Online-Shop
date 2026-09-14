# tests/store/test_store_forms.py
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from store.forms import ProductForm, CommentForm


@pytest.mark.unit
class TestProductForm:
    def test_valid_product_form(self, create_user, create_category):
        user, profile = create_user(role="seller")
        category = create_category("Tech")

        image_file = io.BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(image_file, format='JPEG')
        image_file.seek(0)

        uploaded_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_file.read(),
            content_type='image/jpeg'
        )

        data = {
            "name": "Test Product",
            "price": 100.00,
            "digital": False,
            "description": "A valid product",
            "is_available": True
        }
        files = {"image": uploaded_file}
        form = ProductForm(data, files)
        assert form.is_valid(), form.errors

    def test_valid_digital_product_form(self, create_user):
        user, profile = create_user(role="seller")
        data = {
            "name": "Digital Product",
            "price": 50.00,
            "digital": True,
            "description": "A digital product",
            "is_available": True
        }
        form = ProductForm(data)
        assert form.is_valid(), form.errors

    def test_physical_product_requires_image(self, create_user):
        user, profile = create_user(role="seller")
        data = {
            "name": "Physical Product",
            "price": 100.00,
            "digital": False,
            "description": "A physical product",
            "is_available": True
        }
        form = ProductForm(data)
        assert not form.is_valid()
        assert "Physical products need an image." in str(form.errors["__all__"])

    def test_missing_name_validation(self):
        data = {"price": 100, "is_available": True}
        form = ProductForm(data)
        assert not form.is_valid()
        assert "name" in form.errors

    def test_clean_name_short(self):
        form_data = {"name": "ab", "price": 10}
        form = ProductForm(form_data)
        assert not form.is_valid()
        assert "Product name is too short" in str(form.errors["name"])

    def test_clean_name_too_long(self):
        # use 201 characters to trigger model validation first, but clean_name also raises
        # we expect the model validation error because it runs before clean_name
        long_name = "A" * 201
        form_data = {"name": long_name, "price": 10}
        form = ProductForm(form_data)
        assert not form.is_valid()
        # Django's default max_length validation error
        assert "Ensure this value has at most 200 characters" in str(form.errors["name"])


@pytest.mark.unit
class TestCommentForm:
    def test_valid_comment(self):
        data = {"text": "This is a valid comment."}
        form = CommentForm(data)
        assert form.is_valid()

    def test_comment_too_short(self):
        data = {"text": "hi"}
        form = CommentForm(data)
        assert not form.is_valid()
        assert "Comment is too short" in str(form.errors["text"])