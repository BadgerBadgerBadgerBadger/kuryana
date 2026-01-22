"""
Type definitions for Kuryana API responses.

These TypedDict classes document the structure of API responses
and enable type checking for response data.
"""

from datetime import datetime
from typing import TypedDict


# =============================================================================
# Common Types
# =============================================================================


class CastMember(TypedDict, total=False):
    """Cast member in a drama."""

    name: str
    profile_image: str
    slug: str
    link: str


class Recommendation(TypedDict, total=False):
    """Recommended drama."""

    title: str
    slug: str
    link: str
    poster: str


class WhereToWatch(TypedDict, total=False):
    """Streaming platform availability."""

    platform: str
    link: str
    note: str


# =============================================================================
# Drama Response Types
# =============================================================================


class DramaDetails(TypedDict, total=False):
    """Drama metadata details."""

    aired: str
    episodes: str
    status: str
    duration: str
    content_rating: str
    score: str
    ranked: str
    popularity: str
    watchers: str


class DramaOthers(TypedDict, total=False):
    """Drama additional info."""

    country: list[str]
    type: str
    genre: list[str]
    tags: list[str]


class DramaData(TypedDict, total=False):
    """Drama detail response data."""

    link: str
    title: str
    complete_title: str
    sub_title: str
    year: str
    rating: float | None  # Always float or None, never string
    poster: str
    synopsis: str
    casts: list[CastMember]
    details: DramaDetails
    others: DramaOthers
    current_episode: str
    next_episode_airing: dict | None
    recommendations: list[Recommendation]
    where_to_watch: list[WhereToWatch]


class DramaResponse(TypedDict):
    """Full drama fetch response."""

    slug_query: str
    data: DramaData
    scrape_date: datetime


# =============================================================================
# Cast Response Types
# =============================================================================


class CastMemberWithRole(TypedDict, total=False):
    """Cast member with role information."""

    name: str
    profile_image: str
    slug: str
    link: str
    role: dict  # Contains 'name' and 'type'


class CastData(TypedDict, total=False):
    """Cast list response data."""

    link: str
    title: str
    poster: str
    casts: dict[str, list[CastMemberWithRole]]  # Keyed by role category


class CastResponse(TypedDict):
    """Full cast fetch response."""

    slug_query: str
    data: CastData
    scrape_date: datetime


# =============================================================================
# Person Response Types
# =============================================================================


class PersonWork(TypedDict, total=False):
    """Work entry for a person."""

    title: dict  # Contains 'name' and 'link'
    year: int | str | None
    role: dict | None  # Contains 'name' and 'type'
    rating: float | None
    episodes: int | None


class PersonDetails(TypedDict, total=False):
    """Person metadata details."""

    nationality: str
    birthday: str
    gender: str


class PersonData(TypedDict, total=False):
    """Person detail response data."""

    link: str
    name: str
    profile: str
    about: str
    details: PersonDetails
    works: dict[str, list[PersonWork]]  # Keyed by work category (Drama, Movie, etc.)
    news: list[dict]


class PersonResponse(TypedDict):
    """Full person fetch response."""

    slug_query: str
    data: PersonData
    scrape_date: datetime


# =============================================================================
# Search Response Types
# =============================================================================


class SearchDrama(TypedDict, total=False):
    """Drama search result."""

    slug: str
    title: str
    thumb: str
    mdl_id: str
    ranking: str | None
    type: str | None
    year: int | None
    series: str | bool


class SearchPerson(TypedDict, total=False):
    """Person search result."""

    slug: str
    name: str
    thumb: str
    nationality: str


class SearchResults(TypedDict):
    """Search results container."""

    dramas: list[SearchDrama]
    people: list[SearchPerson]


class SearchResponse(TypedDict):
    """Full search response."""

    query: str
    results: SearchResults
    scrape_date: datetime


# =============================================================================
# Episode Response Types
# =============================================================================


class Episode(TypedDict, total=False):
    """Episode information."""

    title: str
    image: str
    link: str
    rating: float | None  # Always float or None
    air_date: str | None


class EpisodesData(TypedDict, total=False):
    """Episodes list response data."""

    link: str
    episodes: list[Episode]


class EpisodesResponse(TypedDict):
    """Full episodes fetch response."""

    slug_query: str
    data: EpisodesData
    scrape_date: datetime


# =============================================================================
# Error Response Type
# =============================================================================


class ErrorDescription(TypedDict, total=False):
    """Error description details."""

    title: str
    info: str


class ErrorResponse(TypedDict, total=False):
    """Error response structure."""

    error: bool
    code: int
    description: str | ErrorDescription
