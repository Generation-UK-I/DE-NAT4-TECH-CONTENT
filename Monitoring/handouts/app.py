#! /usr/local/bin/python
# -*- coding: utf-8 -*-
from calendar import timegm
from datetime import datetime
from flask import Flask

app = Flask(__name__)
app.debug = True


@app.route("/")
def health_check():
    return "This datasource is healthy."


@app.route("/sales_stats", methods=["GET"])
def sales_stats():
    return {
        "stats": [
            {
                "recorded_date": "2024-01-01T09:00:00Z",
                "coffee_sales": "42.00",
                "food_sales": "16.0",
            },
            {
                "recorded_date": "2024-02-01T09:00:00Z",
                "coffee_sales": "55.00",
                "food_sales": "9.0",
            },
            {
                "recorded_date": "2024-03-01T09:00:00Z",
                "coffee_sales": "33.00",
                "food_sales": "22.0",
            },
            {
                "recorded_date": "2024-04-01T09:00:00Z",
                "coffee_sales": "38.00",
                "food_sales": "13.0",
            },
            {
                "recorded_date": "2024-05-01T09:00:00Z",
                "coffee_sales": "39.00",
                "food_sales": "8.0",
            },
            {
                "recorded_date": "2024-06-01T09:00:00Z",
                "coffee_sales": "44.00",
                "food_sales": "13.0",
            },
            {
                "recorded_date": "2024-07-01T09:00:00Z",
                "coffee_sales": "51.00",
                "food_sales": "14.0",
            },
            {
                "recorded_date": "2024-08-01T09:00:00Z",
                "coffee_sales": "45.00",
                "food_sales": "11.0",
            },
            {
                "recorded_date": "2024-09-01T09:00:00Z",
                "coffee_sales": "42.00",
                "food_sales": "7.0",
            },
            {
                "recorded_date": "2024-10-01T09:00:00Z",
                "coffee_sales": "36.00",
                "food_sales": "17.0",
            },
            {
                "recorded_date": "2024-11-01T09:00:00Z",
                "coffee_sales": "45.00",
                "food_sales": "11.0",
            },
            {
                "recorded_date": "2024-12-01T09:00:00Z",
                "coffee_sales": "34.00",
                "food_sales": "23.0",
            }
        ]
    }


if __name__ == "__main__":
    app.run(debug=True)
