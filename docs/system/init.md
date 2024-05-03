## Initialize your `krixik` cli

Initialize your `krixik` cli using your unique secrets `api_key` and `api_url` as shown below.


```python
from krixik import krixik
krixik.init(api_key=MY_API_KEY, 
            api_url=MY_API_URL)
```

Here  `MY_API_KEY` and `MY_API_URL` are unique to your account.  

To keep your account secure, never store your secrets in code `.py` or notebook `.ipynb` files.  Store secrets in a `.env` file that is explicitly ignored by `.gitignore`. 

You can load these secrets into your code using the `python-dotenv` package as shown below

```python
import os
from dotenv import load_dotenv
load_dotenv()
MY_API_KEY=os.getenv('MY_API_KEY')
MY_API_URL=os.getenv('MY_API_URL')
```

You can check your init credentials using the `krixik.check_init_data` method as shown below

```python
krixik.check_init_data()
```
