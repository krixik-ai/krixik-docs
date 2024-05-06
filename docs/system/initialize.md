## Initialize and authenticate a session

Initialize your krixik session with your api key and url as shown below. 


```python
# import krixik and initialize it with your personal secrets
from krixik import krixik

krixik.init(api_key=MY_API_KEY, api_url=MY_API_URL)
```

We strongly recommend loading these required secrets in via [python-dotenv](https://pypi.org/project/python-dotenv/), and storing those secrets in a `.env` file.  This is always good practice for storing / loading secrets (e.g., doing so will reduce the chance you accidentally push secrets to a repo).

With your secrets defined in a `.env` file as

```ssh-config
MY_API_KEY=<MY_API_KEY>
MY_API_URL=<MY_API_URL>
```

use [python-dotenv](https://pypi.org/project/python-dotenv/) to load them in for use in your session as shown below.


```python
# load secrets from a .env file using python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()
MY_API_KEY = os.getenv("MY_API_KEY")
MY_API_URL = os.getenv("MY_API_URL")
```
