"""Workspace invite links (FEAT-001)."""

import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta

LINK_LIFETIME = timedelta(days=7)

_links = {}


@dataclass(frozen=True)
class Link:
    id: int
    workspace_id: str
    token: str
    expires_at: datetime


def create_link(workspace_id, now):
    """T-001, FR-001, AC-001: create a link that expires 7 days after `now`."""
    link = Link(
        id=len(_links) + 1,
        workspace_id=workspace_id,
        token=secrets.token_urlsafe(16),
        expires_at=now + LINK_LIFETIME,
    )
    _links[link.token] = link
    return link
