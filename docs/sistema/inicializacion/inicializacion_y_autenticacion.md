## Inicializa y Autentica para Empezar
[🇺🇸 English version of this document](https://krixik-docs.readthedocs.io/latest/system/initialization/initialize_and_authenticate/)

Tras [instalar el cliente Krixik](instalacion_del_cliente.md), importa Krixik e inicializa tu sesión (completando la autenticación necesaria) para empezar a usar Krixik.

Para esto necesitas dos secretos:

- Tu "API key"
- Tu "API URL"

Si estás participando en nuestras pruebas beta y no tienes tus secretos, escríbele a los administradores de Krixik.

En vez de manejar tus secretos directamente, enfáticamente recomendamos guardarlos en un archivo `.env` y cargarlos a través de [python-dotenv](https://pypi.org/project/python-dotenv/). Esta es una mejor práctica para guardar/cargar secretos, dado que los mantiene separados de tu código y de otros archivos y reduce la posibilidad de que accidentalmente los subas a un repositorio.

Para hacer esto, define tus secretos en un archivo `.env` de la siguiente manera:

```ssh-config
DEMO_API_KEY=EJEMPLO_API_KEY_45678
DEMO_API_URL=EJEMPLO_API_URL_09123
```

Luego cárgalos con [python-dotenv](https://pypi.org/project/python-dotenv/):


```python
# carga tus secretos de un archivo .env con python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()
MI_API_KEY = os.getenv("DEMO_API_KEY")
MI_API_URL = os.getenv("DEMO_API_URL")
```

Tras cargar tus secretos puedes importar Krixik e inicializar/autenticar para empezar tu sesión.

Estas son dos acciones separadas, así que hazlas por separado. Primero importa Krixik:


```python
# importa Krixik
from krixik import krixik
```

Ahora inicializa tu sesión con tus secretos:


```python
# inicializa tu sesión con tus secretos
krixik.init(api_key=MI_API_KEY, api_url=MI_API_URL)
```

    SUCCESS: You are now authenticated.


Listo, ¡ya puedes arrancar! Es hora de [ensamblar *pipelines*](../creacion_de_pipelines/creacion_de_pipelines.md).
