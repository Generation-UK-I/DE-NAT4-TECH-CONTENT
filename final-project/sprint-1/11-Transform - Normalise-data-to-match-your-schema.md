# Transform - Normalise data to match your schema

## Description

Once we have a solution in-place to clean the transaction data, we need to change the shape of what we have in memory (from loading and cleaning the file data) to match the desired shape in our database schema.

For example, we may need to separate the data into a separate records for the transaction itself, and one record each per basket/purchased item.

Each row we make should have a foreign key pointing to the it's parent table primary key, e.g. Items -> Transaction or  Transactions -> Branch (as an example).

### Hint

This ticket is very large and could be split into multiple other tickets and/or tasks, e.g.:

- Separate string of multiple purchased items into a list
- Separate item price from item name
- Generate your own GUIDs in memory for each item

## User Story

**As a** data analyst
**I want** to be able to have my data structured in third normal form
**So that** data redundancy is reduced and data integrity is improved

## Acceptance Criteria

- [ ] todo
- [ ] todo
- [ ] todo
