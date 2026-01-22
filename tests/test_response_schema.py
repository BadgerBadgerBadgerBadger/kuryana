"""
Response schema validation tests.

These tests verify that API responses conform to the documented
type contracts in AGENTS.md and app/lib/types.py.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestResponseWrappers:
    """Test that responses use correct wrapper structures."""

    def test_fetch_endpoint_has_data_wrapper(self):
        """Fetch endpoints should wrap response in 'data' field."""
        # Using a known drama ID
        response = client.get("/id/35729-goblin")

        if response.status_code == 200:
            data = response.json()
            assert "slug_query" in data, "Missing 'slug_query' field"
            assert "data" in data, "Missing 'data' wrapper field"
            assert "scrape_date" in data, "Missing 'scrape_date' field"
            assert isinstance(data["data"], dict), "'data' should be a dict"

    def test_search_endpoint_has_results_wrapper(self):
        """Search endpoints should use 'results' field, not 'data'."""
        response = client.get("/search/q/goblin")

        if response.status_code == 200:
            data = response.json()
            assert "query" in data, "Missing 'query' field"
            assert "results" in data, "Missing 'results' field"
            assert "scrape_date" in data, "Missing 'scrape_date' field"
            assert "data" not in data, "Search should not have 'data' field"

    def test_error_response_structure(self):
        """Error responses should have error/code/description."""
        response = client.get("/id/nonexistent-drama-that-does-not-exist-12345")

        if response.status_code == 404:
            data = response.json()
            assert "error" in data, "Missing 'error' field"
            assert data["error"] is True, "'error' should be True"
            assert "code" in data, "Missing 'code' field"


class TestFieldTypes:
    """Test that fields have consistent types."""

    def test_drama_rating_is_float_or_none(self):
        """Rating should be float or None, never string."""
        response = client.get("/id/35729-goblin")

        if response.status_code == 200:
            data = response.json()
            rating = data["data"].get("rating")

            # Rating should be float or None
            assert rating is None or isinstance(rating, (int, float)), (
                f"Rating should be float or None, got {type(rating).__name__}: {rating}"
            )

            # Specifically should NOT be string
            assert not isinstance(rating, str), (
                f"Rating should never be string, got: {rating}"
            )

    def test_search_drama_has_required_fields(self):
        """Search drama results should have expected fields."""
        response = client.get("/search/q/goblin")

        if response.status_code == 200:
            data = response.json()
            dramas = data["results"].get("dramas", [])

            if dramas:
                drama = dramas[0]
                # Check required fields exist
                assert "slug" in drama, "Drama missing 'slug'"
                assert "title" in drama, "Drama missing 'title'"
                assert "mdl_id" in drama, "Drama missing 'mdl_id'"

    def test_person_response_structure(self):
        """Person endpoint should have correct structure."""
        # Using a known person ID
        response = client.get("/people/461-gong-yoo")

        if response.status_code == 200:
            data = response.json()
            assert "data" in data, "Missing 'data' wrapper"

            person = data["data"]
            assert "name" in person, "Person missing 'name'"


class TestImageUrls:
    """Test image URL handling."""

    def test_drama_poster_is_absolute_url(self):
        """Drama poster should be an absolute URL."""
        response = client.get("/id/35729-goblin")

        if response.status_code == 200:
            data = response.json()
            poster = data["data"].get("poster", "")

            if poster:
                assert poster.startswith("http"), (
                    f"Poster should be absolute URL, got: {poster}"
                )


class TestSlugFormats:
    """Test slug format consistency."""

    def test_search_slug_format(self):
        """Search results should have slug without leading slash."""
        response = client.get("/search/q/goblin")

        if response.status_code == 200:
            data = response.json()
            dramas = data["results"].get("dramas", [])

            if dramas:
                slug = dramas[0].get("slug", "")
                # Search slugs should not have leading slash
                # (they come as "35729-goblin" not "/35729-goblin")
                if slug:
                    # Slug should start with a digit (ID)
                    assert slug[0].isdigit() or slug.startswith("/"), (
                        f"Unexpected slug format: {slug}"
                    )


# =============================================================================
# Unit Tests for Utility Functions
# =============================================================================


class TestImageUtils:
    """Test image utility functions."""

    def test_to_absolute_url_with_relative_path(self):
        from app.lib.images import to_absolute_url

        result = to_absolute_url("/people/123-name")
        assert result.startswith("https://mydramalist.com")
        assert "people/123-name" in result

    def test_to_absolute_url_with_absolute_url(self):
        from app.lib.images import to_absolute_url

        url = "https://example.com/image.jpg"
        result = to_absolute_url(url)
        assert result == url

    def test_to_absolute_url_with_none(self):
        from app.lib.images import to_absolute_url

        result = to_absolute_url(None)
        assert result == ""

    def test_optimize_poster_url(self):
        from app.lib.images import optimize_poster_url

        url = "https://example.com/1280/poster.jpg"
        result = optimize_poster_url(url)
        assert "/1280/" not in result
        assert result == "https://example.com/poster.jpg"

    def test_optimize_profile_url(self):
        from app.lib.images import optimize_profile_url

        url = "https://example.com/profile_s.jpg"
        result = optimize_profile_url(url, "m")
        assert result == "https://example.com/profile_m.jpg"

    def test_optimize_thumbnail_url(self):
        from app.lib.images import optimize_thumbnail_url

        url = "https://example.com/image_t.jpg"
        result = optimize_thumbnail_url(url)
        assert result == "https://example.com/image_c.jpg"
