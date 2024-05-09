# Welcome to krixik!

Easily assemble and serverlessly consume modular AI pipelines through secure Python APIs.

## Quickstart guide

Get started in three easy steps.

1.  [install the krixik cli](#install-the-krixik-cli)
2.  [initialize a session](#initialize-a-session)
3.  [start building](#start-building)

### Install the krixik cli using pip

Install the [krixik Python CLI](https://github.com/krixik-ai/krixik-cli) using `pip` by executing the following at a terminal.

```python
# install the krixik cli
pip install krixik
```

Note: Python version 3.8 or higher is required to use the cli.

### Initialize a session

Initialize a session by executing the following in a notebook or ide.

```python
from krixik import krixik
krixik.init(api_key=MY_API_KEY, 
            api_url=MY_API_URL)
```

Here  `MY_API_KEY` and `MY_API_URL` are your account secrets.

Note: [krixik](https://github.com/krixik-ai/krixik-cli) is currently in closed beta.  Please reach out to us directly if you have any issues initializing a session.

### Start building

Start building modular pipelines!

- Dive in headfirst into building [multi-module examples](https://krixik-docs.readthedocs.io/en/latest/examples/overview/)
- Learn how to build with [individual modules](https://krixik-docs.readthedocs.io/en/latest/modules/overview/)
- Learn about [krixik system methods](https://krixik-docs.readthedocs.io/en/latest/system/overview/)
