# Yelp-Search-Engine

CSE 6242 Course Proj

Our CSE 6242 project aims to build a small search engine like Yelp based on reviews data.


# Tech Stack

Front-end: Next.js, Antd, Axios, React

Back-end: Opensearch(AWS), Kibana(AWS), Sqlite, Flask

Model: Textrank, NER


# Data Source

Data collection: We use the open-source Yelp dataset, which is available at https://www.yelp.com/dataset. This dataset contains reviews data, business information data and otehr data.
We mainly use these two. In food entity recoginition task, we use the USDA FoodData Central Data, which is available at https://fdc.nal.usda.gov/download-datasets.html.
In NER tasks, we also need other text data for revision. We simply choose public dataset from the BBC comprised of 2225 articles, which is availale at https://www.kaggle.com/competitions/learn-ai-bbc/data.


# Installation

To install all Python dependencies used in this project, run

```
pip install -r requirements.txt
```


# Execution

First, you have to set a Opensearch domain on AWS and add credentials info to your environment path.

```python upload_review_data.py```: upload reviews data onto Opensearch

```python upload_business_data.py```: upload reviews data onto Sqlite

If NER task is required, run NER.ipynb to obtain trained model stored in pkl

Finally, ```python app.py```: start Flask application, you can navigate to localhost:5000 in your browser to see the site

