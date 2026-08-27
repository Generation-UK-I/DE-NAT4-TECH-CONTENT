# Design schema to model data

## Description

Before storing our data we must design a schema for it so that we can create it in our database.

### Notes

- Design a db schema with one or more tables.
- Use GUIDs for the ID columns, not auto-generated numbers/sequences, to avoid concurrency issues later in AWS.
- You will insert the GUIDs yourselves into the data in your python code (there is a python function for generating GUIDs).
- Assume a big-data style on your tables & data; don't assume that todays Leeds branch is the same as tomorrows Leeds branch (so, can have a different guid), nor that products always have the same name or price! Adjust your schema and it's constraints accordingly.

## User Story

**As a** product owner
**I want** to agree on the design of the schema
**So that** the data is easy to query

## Acceptance Criteria

- [ ] todo
- [ ] todo
- [ ] todo
