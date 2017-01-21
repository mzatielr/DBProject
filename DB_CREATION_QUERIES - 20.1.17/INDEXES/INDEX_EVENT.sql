CREATE INDEX eventIdIndex ON Event(id);
CREATE INDEX eventCategoryIDIndex ON Event(category_id);
CREATE INDEX eventPlaceIDIndex ON Event(place_id);
CREATE INDEX eventOwnerIDIndex ON Event(owner_id);
CREATE FULLTEXT INDEX FullTextSearchIndex (description);