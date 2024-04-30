# Kaggle Extract and Analysis

# Como instalar as dependencias do projeto
Primeiro, instale o [Poetry](https://python-poetry.org/), ele é usado em todo o projeto para gerenciar as dependencias
```bash
pip install poetry
```

Agora, com o `poetry` instalado precisa instalar os pacotes que estão em `pyproject.toml` e criar um ambiente virtual
```bash
poetry shell
poetry install
```

Com o ambiente criado e os pacotes instalados precisa baixar os dados do kaggle, para isso, vai precisar autenticar com a API do Kaggle.

Agora precisa baixar [suas credenciais](https://www.kaggle.com/settings/account) (create new token) e colocar em `C:\Users\<usuário>\.kaggle\kaggle.json`.

Agora rode o projeto

```bash
cd etl
python extract.py
```

Com os dados baixados e extraídos, pode iniciar a analise.

# IMPORTANTE

Os dados de `brazil_population_2019.csv` tem um problema que impede que ele seja lido

para resolver, precisa abrir o arquivo csv, ir na linha 1282 e apagar as colunas extras "Entorno...". Seleciona até a virgula, aperta Ctrl+h e clica em "replace all" (segunda caixinha)

Os dados ficam disponiveis em `data/`
