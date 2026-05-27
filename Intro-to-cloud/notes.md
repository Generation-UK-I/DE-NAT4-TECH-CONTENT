
Lambda is an **event-driven** service, it allows you to write code in a range of popular languages natively or via API call, you simply provide your code, and decide what **event** triggers it to run. You are billed for the length of time it takes to execute your function, to the second.

There are some limitations to running your functions with Lambda, your function should not:

- Exceed 15 mins (900 secs) runtime
- Consume more than 10GB of RAM, or 10GB of persistent storage
- Be more than 50MB (code and resource files) when zipped
  - If your function needs access to a lot of data, simply store it elsewhere, such as in S3

There are more, but these are the key ones to be aware of initially.