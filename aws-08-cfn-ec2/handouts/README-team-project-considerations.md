# AWS Team Project considerations

Now that we have finished going through the AWS 01...08 sessions, and we have all that context, we have some hints & tips for your team projects.

## Relational vs non-relational databases

> Some of this will make more sense after the Data Warehouses session.

- Local PostgreSQL is a relational database.
- Redshift is not, it's a data-warehouse.
- How we insert data into each will be different.
- When inserting into Postgres, we very much care about relational integrity.
    - We also care about re-using yesterdays IDs on todays data (so often look those up).
        - This is a row-based system with strong relationships, always in 3rd or more normal form, in a relational layout.
    - We can use the `RETURNING` clause to help with this.
    - Our reports can link the solid referential data together; There is only one "Leeds" branch with one ID, and that one ID links to many days data.
    - We insert one files worth of data at a time, so when the next file arrives we can look up the previous data.
    - We can let the database create IDs as auto-generated numbers for us, or as GUIDs.
- When inserting into RedShift, we care about bulk data;
    - We only mildly care about referential integrity; it's optional.
    - This is a column-based system with loose integrity but fast processing of large amounts of data; it is often not in full 3rd normal form, usually in a star or snowflake schema, or is even denormalised.
    - RedShift does not have the `RETURNING` clause.
    - We often don't look up yesterdays IDs to re-use them.
    - We often make new IDs for todays data; as long as todays data has some integrity (so our reports are accurate), we don't care if we duplicate things. We have have many "Leeds" branches with the same name and different IDs on different days.
    - So, we often don't let the database create IDs as auto-generated numbers for us;
        - And often do generate GUIDs ourselves and use those.
    - Our reports can fix up the stats and numbers by assuming that the "Leeds" branch yesterday has the same name as the "Leeds" branch today, and group on that, and link each days ID to that days data.
    - Our lambdas need to be able to run 25+ branches of data in at the exact same time, overlapping, so can't depend on what another lambda is doing - or what data it sees or is creating.

## Timeouts in Lambdas

- Watch for timeouts in your logs - if so, you need to put the `Lambda | Timeout` value up in your yml files and redeploy.
- This means your lambda will be killed by AWS before it completes inserting your data.
- You can also change it directly in the web console (_Lambda -> Configurations_) for testing.
- Depending on your code, big files could take 5-10 mins to process.
- Lambdas should be fast, so check;
    - are you only making ONE connection per lambda?
    - are you committing?
    - are you using batch inserts?
        - `INSERT into table_name (col_a, col_b, col_c) VALUES (row_1_id, a1, b1), (row_2_id, a2, b3) .... (row_100, a100, b100)`
        - See <https://docs.aws.amazon.com/redshift/latest/dg/c_best-practices-multi-row-inserts.html>

## Throttles in Lambdas

- Watch out for throttles in the lambda metrics (so, _Lambda -> Monitoring tab -> Throttles panel_, or, in _CloudWatch -> Metrics -> Lambda_)
- This means AWS refused to run enough lambdas at once, so some files will be missed.
- See <https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html> - this is a very good and detailed read.
- Either
    - Remove your `Concurrency Limit`.
    - _Web console -> Lambda -> Configuration -> Concurrency_ -> change to "Use unreserved account concurrency".
    - If it exists, remove the line `Lambda | ReservedConcurrentExecutions` in your yml files and redeploy.
- Or
    - increase your `Reserved Concurrency` to > the number of expected files
    - _Web console -> Lambda -> Configuration -> Concurrency_ -> change to "Reserved Concurrency" > the number of files you get sent each day (25?) so e.g. 30.
    - If it exists, you need to put the `Lambda | ReservedConcurrentExecutions` value up in your yml files to e.g. 30 and redeploy,
        - Else, add the line `Lambda | ReservedConcurrentExecutions` with a high value.
