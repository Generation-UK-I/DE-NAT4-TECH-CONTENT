# Improving Data Quality Tutorial

Throughout this lesson we will use a deliberately messy dataset, which we're going to work with using Pandas in your Jupyter Notebook environment. Review the [Data Science in Python](https://github.com/Generation-UK-I/data-science-in-python/blob/main/deploying-jupyter.md) repository if you do not have this set up.

## Create the Dataset

- Open a new Jupyter Notebook, change the first cell to markdown and type:

```text
# Data Cleansing Lab

## Creating the Dataset
```

- Execute the markdown cell, ensure the next one is configured for code, and add the following to create a dataframe.

```python
import pandas as pd
import numpy as np

sales_data = pd.DataFrame({
    'customer_id': [101, 102, 103, 104, 105, 106],
    'name': ['Alice', 'BOB', 'Charlie', 'david', None, 'frankie'],
    'age': [25, -3, 34, 200, 29, 6],
    'country': ['UK', 'uk', 'United Kingdom', 'USA', 'USA ', 'UK'],
    'purchase_amount': [120.50, 85.00, np.nan, 40.00, 75.00, 1055],
    'email': [
        'alice@email.com',
        'bob@email.com',
        'charlie@email',
        'david@email.com',
        'eve@email.com',
        'frankieemail.com'
    ]
})

sales_data
```

If you execute the code Jupyter will display the dataframe without requiring a `print` statement.

>Our dataset is relatively small, but as it scales up, Pandas and similar libraries can continue to provide the required functionality with greater performance and efficiency than other tools.

### Check Validity

Our dataset has the following validity issues:

|Column|Problem|
|---|---|
|age|`-3` is impossible|
|age|`200` is unrealistic|
|email|Missing `.com`|
|email|Missing `@`|

- Below the dataframe add another markdown cell containing:

```text
### Checking for Data Validity

Check for ages below zero
```

- In the next cell add the following code to check for invalid values:

```py
sales_data[sales_data['age'] < 0]
```

- Executing the cell should reveal `BOB`

- Add a new markdown cell containing `Check for unrealistic ages`, then repeat the last two steps, but search for people older than a suitable integer.

- We next need to search for users with invalid email addresses. To do so we'll use the `series.str.contains` method, which allows us to search the strings within a dataframe or series for substrings which we can define with regex.

  To save going further than necessary down that rabbit hole, the code is provided below.

  Add the following markdown: `Checking for Invalid email addresses`, then the below code in the next cell.

```py
sales_data[~sales_data['email'].str.contains('@')]
sales_data[~sales_data['email'].str.contains(r'@.*\.', na=False)]
```

- Since it's better for data to be missing rather than inaccurate, we should remove the invalid `age` entries. To do so we'll use Pandas `series.loc` method, which will return values for the given label or expression. Add the following markdown to a cell:

```text
### Fixing Invalid Data

Replace Invalid Ages with NaN
```

- Then this code:

```py
sales_data.loc[sales_data['age'] < 0, 'age'] = np.nan
sales_data.loc[sales_data['age'] > 120, 'age'] = np.nan

sales_data # call the dataframe to verify the changes
```

>`NaN` means missing data

Sometimes you may be able to correct invalid data, in our case we can infer from the other records that we're missing the `.com` (top-level domain) from one address, and the `@` symbol from another.

>This scenario could be feasible in the real-world if the dataset contains, for example, records about employees in a company were the email address is consistent. Of course it will often not be the case.

- Add another code cell to update the relevant records:

```py
sales_data.loc[2, 'email'] = 'charlie@email.com'  # Add .com TLD
sales_data.loc[5, 'email'] = 'frankie@email.com'  # Add @ symbol

sales_data # Verify
```

### Check Accuracy

Computers can often identify invalid data automatically, but fixing accuracy can be more difficult because:

- The value may look correct
- External knowledge is often needed
- Human verification may be required

Our dataset is small, but has one potential accuracy issue

- Add markdown:

```text
Find Unusually Large Purchases
```

- Add code:

```py
sales_data[sales_data['purchase_amount'] > 1000]
```

A record is returned, and it is a valid value, but is it accurate?

We could gain more insight by using the `series.describe()` method against the column containing the suspicious value:

```py
sales_data['purchase_amount'].describe()
```

This provides a quick statistical summary of the purchase_amount column. We're not aiming to be data analysts so we don't need to go into the maths, but there are a few things we can point out.

1. Often standard deviation is used to identify outliers; Typically data more than three standard deviations from the mean is considered an outlier. In this case our dataset is too small, so standard deviation is dragged up too much.
2. We can see that the suspected outlier is multiple times larger than the mean, which is unusual for such a small dataset.

    We might suspect the issue: for example maybe someone just double-pressed `5`; How you fix this accuracy issue (*or even whether you fix it - it may be down to the data analysts*) will depend upon the scenario and organisational processes.

For our purposes we can assume it was a double-press, so fix it by adapting the code we used earlier to update the email addresses.

>Add your own markdown to explain the next steps

### Check Consistency

Our dataset has consistency issues with the country field; The `series.value_counts()` method can give us some insight:

```py
sales_data['country'].value_counts()
```

We clearly have some issues with how both `UK` and `USA` are represented.

- Standardise existing values:

```py
sales_data['country'] = sales_data['country'].str.strip()
sales_data['country'] = sales_data['country'].str.upper()

sales_data['country'].value_counts()
```

- We still have one inconsistent value, update it using the `series.replace()` method:

```py
sales_data['country'] = sales_data['country'].replace({
    'UNITED KINGDOM': 'UK'
})

sales_data['country'].value_counts()
```

Our `country` values are now consistent, call `sales_data` to see the changes from the original dataset.

### Check Completeness

In our data we're missing:

- A name
- Two ages
- One purchase amount

We could use different approaches to update some of the missing values. We may be able to:

- Drop records containing missing values
- Replace missing values with a realistic calculated alternative, for example the mean of the dataset.
- If the value is not crucial to the record we may replace a null value with a placeholder.
- In some cases we can infer missing values from surrounding data.

We can drop NaN records with `sales_data.dropna()`, but we'll lose half of our data, so let's try some different approaches.

Although occasional unusually large purchases may occur, the majority of valid values should trend towards the mean.

- Execute the following code in the next cell to update the missing value in purchase_amount using the `series.fillna()` method.

```py
sales_data['purchase_amount'] = sales_data['purchase_amount'].fillna(
    sales_data['purchase_amount'].mean()
)

sales_data
```

In our case we can assume that `age` is not an essential value for a record (*of course in the real-world this would likely not be the case*), so we can replace it with the placeholder string "Unknown", which is more informative than `NaN` - which could mean missing, corrupted, deleted, etc.

```py
sales_data['age'] = sales_data['age'].fillna('Unknown')

sales_data
```

Now we just need to deal with the missing `name` value; For our dataset we can infer it from the surrounding data - the email address appears to be simply `[name]@email.com` with no apparent truncation.

- Update the relevant name record by adapting previously used code with the correct name.

- Repeat the earlier command to verify there are no more null values.

### Check Uniformity

Our final task to clean the dataset is to deal with the uniformity issue in the name field.

- Re-use and adapt some earlier code to ensure that all values in the name field are returned in title case.

>A common uniformity challenge is DATE values, because they may be recorded in different formats, and differ across countries, for example: DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD, and so on. There are methods available, and processes to deal with such issues, but digging into them is a bit outside of our scope for now.

---

You should now have fixed all of the quality issues in the dataset.

Continue onto the next exercise, using pandas with a much bigger dataset.

[Exercise 2](./data-cleansing-exercise-bonus.md)
