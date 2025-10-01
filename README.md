# Sistema de Gerenciamento de Oficina (junior_auto_ar)

Este projeto é um sistema de gerenciamento de uma oficina automotiva de ar condicionado desenvolvido em Flask + SQLAlchemy.

## 🚀 Tecnologias
- Python 3.10+
- Flask 3.x
- SQLAlchemy
- SQLite
- Html
- Css

## 📦 Instalação e Execução

### 1. Criar ambiente virtual
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Inicializar banco de dados (apenas se não existir)
```bash
python init_db.py
```

### 4. Rodar servidor
```bash
flask run
```

O sistema estará disponível em: **http://127.0.0.1:5000**
