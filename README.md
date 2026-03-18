[![issues](https://img.shields.io/github/issues/luizcsbh/python-trabalho-final)](https://github.com/luizcsbh/python-trabalho-final/issues)
![forks](https://img.shields.io/github/forks/luizcsbh/python-trabalho-final)
![stars](https://img.shields.io/github/stars/luizcsbh/python-trabalho-final)
[![GitHub License](https://img.shields.io/github/license/luizcsbh/python-trabalho-final)]
(https://github.com/luizcsbh/python-trabalho-final/blob/master/LICENSE)
![code-size](https://img.shields.io/github/languages/code-size/luizcsbh/python-trabalho-final)
[![commit activity](https://img.shields.io/github/commit-activity/m/luizcsbh/python-trabalho-final)](https://github.com/luizcsbh/python-trabalho-final/commits)
[![last commit](https://img.shields.io/github/last-commit/luizcsbh/python-trabalho-final)](https://github.com/luizcsbh/python-trabalho-final/commits)



# Fluxo Financeiro

Este projeto é um sistema de **Fluxo Financeiro** desenvolvido em Django para controle e gestão de despesas e receitas. O objetivo do projeto é permitir o registro de transações vitais para o controle financeiro pessoal.

## 🚀 Como Rodar o Projeto

Siga os passos abaixo para configurar e executar o projeto na sua máquina:

### Pré-requisitos
- Python 3.13+
- Git

### 1. Clonar o repositório
```bash
git clone https://github.com/luizcsbh/python-trabalho-final.git
cd python-trabalho-final
```

### 2. Criar e ativar o ambiente virtual
```bash
python3 -m venv .venv

# No macOS/Linux:
source .venv/bin/activate

# No Windows:
.venv\Scripts\activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Executar as migrações (Banco de Dados)
O projeto utiliza SQLite localmente. Execute as migrações para inicializar as tabelas bancárias:
```bash
python manage.py migrate
```

### 5. Iniciar o servidor
```bash
python manage.py runserver
```

Após o servidor iniciar, o sistema estará disponível no seu navegador em: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

## 📄 Licença

Este projeto está licenciado sob a licença **MIT** - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

- [Luiz Santos](https://about.me/luizcsbh)
