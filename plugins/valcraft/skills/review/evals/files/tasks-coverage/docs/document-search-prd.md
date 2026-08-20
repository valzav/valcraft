# PRD: Document search

## Problem

Browsing the folder tree is the only way to reach a document. In a workspace with thousands of documents, members give up and recreate documents that already exist.

## What we want

A member types part of what they remember and finds the document. What they remember may be words from the title, or words from the body — both must work, because members routinely remember a phrase from inside a document and nothing about its title.

Results must never include a document the member is not allowed to read. A search result that reveals a private document's title is a permissions leak even if the document cannot be opened.

## Out of scope

- Ranking tuning beyond simple relevance.
- Search across workspaces.
