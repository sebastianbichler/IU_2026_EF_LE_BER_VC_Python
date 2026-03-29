### Activate virtual environment
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Add dependencies
```bash
pip freeze > requirements.txt
```

### Start project
```bash
flask run
```

### Check types
```bash
mypy .
```