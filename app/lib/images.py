"""
Image URL utilities for Kuryana.

Centralizes image URL transformations for consistent handling
across all handlers.
"""

from urllib.parse import urljoin

from app import MYDRAMALIST_WEBSITE


def to_absolute_url(path: str | None) -> str:
    """
    Convert a relative path to an absolute MyDramaList URL.

    Args:
        path: Relative path (e.g., "/people/123-name") or absolute URL

    Returns:
        Absolute URL string. Returns empty string if path is None/empty.

    Examples:
        >>> to_absolute_url("/people/123-name")
        "https://mydramalist.com/people/123-name"
        >>> to_absolute_url("https://example.com/image.jpg")
        "https://example.com/image.jpg"
        >>> to_absolute_url(None)
        ""
    """
    if not path:
        return ""

    if path.startswith("http"):
        return path

    return urljoin(MYDRAMALIST_WEBSITE, path.lstrip("/"))


def optimize_poster_url(url: str | None) -> str:
    """
    Optimize poster URL by removing size restrictions.

    MyDramaList poster URLs often include "/1280/" which limits resolution.
    Removing this gets the original full-resolution image.

    Args:
        url: Poster URL potentially containing size restriction

    Returns:
        Optimized URL string. Returns empty string if url is None/empty.

    Examples:
        >>> optimize_poster_url("https://example.com/1280/poster.jpg")
        "https://example.com/poster.jpg"
    """
    if not url:
        return ""

    return url.replace("/1280/", "/")


def optimize_profile_url(url: str | None, size: str = "m") -> str:
    """
    Optimize profile image URL to requested size.

    MyDramaList profile images use size suffixes:
    - s.jpg = small (thumbnail)
    - m.jpg = medium (default)
    - l.jpg = large

    Args:
        url: Profile image URL
        size: Desired size ('s', 'm', or 'l'). Defaults to 'm'.

    Returns:
        Optimized URL string. Returns empty string if url is None/empty.

    Examples:
        >>> optimize_profile_url("https://example.com/profile_s.jpg", "m")
        "https://example.com/profile_m.jpg"
    """
    if not url:
        return ""

    if size not in ("s", "m", "l"):
        size = "m"

    # Replace any size suffix with the requested size
    for s in ("s", "m", "l"):
        url = url.replace(f"{s}.jpg", f"{size}.jpg")

    return url


def optimize_thumbnail_url(url: str | None) -> str:
    """
    Optimize thumbnail URL to card size.

    MyDramaList uses:
    - t.jpg = tiny thumbnail
    - c.jpg = card size (larger)

    Args:
        url: Thumbnail URL

    Returns:
        Optimized URL string. Returns empty string if url is None/empty.

    Examples:
        >>> optimize_thumbnail_url("https://example.com/image_t.jpg")
        "https://example.com/image_c.jpg"
    """
    if not url:
        return ""

    return url.replace("t.jpg", "c.jpg")


def extract_image_url(
    url: str | None,
    optimize: bool = True,
    size: str | None = None,
) -> str:
    """
    Extract and optionally optimize an image URL.

    This is a convenience function that combines URL normalization
    and optimization based on the URL pattern.

    Args:
        url: Raw image URL from HTML
        optimize: Whether to apply optimizations (default: True)
        size: For profile images, the desired size ('s', 'm', 'l')

    Returns:
        Processed URL string. Returns empty string if url is None/empty.
    """
    if not url:
        return ""

    # Ensure absolute URL
    result = to_absolute_url(url)

    if not optimize:
        return result

    # Apply appropriate optimization based on URL pattern
    if "/1280/" in result:
        result = optimize_poster_url(result)
    elif size and any(f"{s}.jpg" in result for s in ("s", "m", "l")):
        result = optimize_profile_url(result, size)
    elif "t.jpg" in result:
        result = optimize_thumbnail_url(result)

    return result
