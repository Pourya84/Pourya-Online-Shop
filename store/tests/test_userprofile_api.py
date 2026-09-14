# store/tests/test_userprofile_api.py
from rest_framework import status
from .base_api import BaseApiTest

class UserProfileApiTests(BaseApiTest):
    """
    تست کامل UserProfileViewSet
    List, Retrieve, Owner Permissions و دسترسی غیرمجاز
    """

    # ==================================================
    # LIST
    # ==================================================
    def test_userprofile_list_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.buyer_token}")
        response = self.client.get("/api/profiles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_userprofile_list_unauthenticated(self):
        response = self.client.get("/api/profiles/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ==================================================
    # RETRIEVE
    # ==================================================
    def test_userprofile_retrieve_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.buyer_token}")
        profile_id = self.buyer_profile.id
        response = self.client.get(f"/api/profiles/{profile_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], profile_id)

    def test_userprofile_retrieve_other_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.seller_token}")
        profile_id = self.buyer_profile.id
        response = self.client.get(f"/api/profiles/{profile_id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_userprofile_retrieve_anonymous(self):
        profile_id = self.buyer_profile.id
        response = self.client.get(f"/api/profiles/{profile_id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)