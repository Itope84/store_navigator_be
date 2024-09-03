import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import func, desc
import re

from .models import Product

# We should be using nltk for this, but for some reason, nltk won't initialize. Here's a basic poc workaround
STOP_WORDS = set(
    [
        "0" "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "for",
        "from",
        "has",
        "he",
        "in",
        "is",
        "it",
        "its",
        "of",
        "on",
        "that",
        "the",
        "to",
        "was",
        "were",
        "will",
        "with",
    ]
)


def tokenize(text):
    # Convert to lowercase and split on non-word characters
    return re.findall(r"\w+", text.lower())


def preprocess_query(query):
    # tokenize
    tokens = tokenize(query)

    tokens = [
        word for word in tokens if word.lower() not in STOP_WORDS and len(word) > 1
    ]

    # remove special characters
    tokens = [re.sub(r"[^a-zA-Z0-9]", "", word) for word in tokens]

    # remove empty strings
    tokens = [word for word in tokens if word]

    return tokens


def search_products(query):
    # Preprocess the query
    tokens = preprocess_query(query)

    if (not tokens) or (not len(tokens)):
        return None

    search_query = " & ".join(tokens)

    results = (
        Product.query.filter(
            func.to_tsvector("english", Product.name).match(search_query)
        )
        .order_by(
            desc(
                func.ts_rank(
                    func.to_tsvector("english", Product.name),
                    func.to_tsquery(search_query),
                )
            )
        )
        .limit(10)
        .all()
    )

    return results


# Searching with multiple query strings
def bulk_search_products(queries):
    results = {}

    # return a dict of query: results
    for query in queries:
        result = search_products(query)
        if result is not None:
            results[query] = search_products(query)

    return results
