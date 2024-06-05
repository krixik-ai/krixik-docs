## Initialize and Authenticate To Get Started

Once you've [installed the Python Client](install_client.md), import Krixik and initialize your session (performing the necessary authentication) to get started.

You'll need two secrets for this:

- Your API key
- Your API URL

If you're participating in our beta test and don't have your secrets, please reach out to Krixik admin.

Instead of handling your secrets directly, we strongly recommend storing them in an `.env` file and loading them via [python-dotenv](https://pypi.org/project/python-dotenv/). This is best practice for storing/loading secrets, as it keeps them compartmentalized and reduces the odds of you accidentally pushing them to a repo.

To do this, define your secrets in your `.env` file as:

```ssh-config
DEMO_API_KEY=EXAMPLE_API_KEY_45678
DEMO_API_URL=EXAMPLE_API_URL_09123
```

Then load them with [python-dotenv](https://pypi.org/project/python-dotenv/) as follows:


```python
# load your secrets from aN .env file using python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()
MY_API_KEY = os.getenv("MY_API_KEY")
MY_API_URL = os.getenv("MY_API_URL")
```

Your secrets loaded, you can now import Krixik and initialize/authenticate to begin your session.

These are two separate actions, so we'll do them separately. First import Krixik:


```python
# import krixik
from krixik import krixik
```

Now initialize your session with your secrets:


```python
# initialize your session with your secrets
krixik.init(api_key=MY_API_KEY, api_url=MY_API_URL)
```

    SUCCESS: You are now authenticated.


Alright, you're good to go! It's time to [assemble some pipelines](../pipeline_creation/create_pipeline.md).
