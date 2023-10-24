# npm-download-tree
Download npm packages and deps and output as a tree 

## Install

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Use

### Simple download

```bash
./main.py react react-router-dom
```

### Custom recurse level
```bash
./main.py -r 1 react react-router-dom
```

### Packages from local package.json
```bash
./main.py react react-router-dom /home/foo/data/myproject/package.json
```

### Packages from remote package.json
```bash
./main.py react react-router-dom https://raw.githubusercontent.com/ant-design/ant-design/master/package.json
```

## Output

At the root of the project it will create an `output` directory structured like this

- a directory `packages`
- zip file per execution

```text
output
├─ packages
│  ├─ react
│  │  ├─ 1.0.0
│  │  │  ├─ react-1.0.0.tgz
│  ├─ @types
│  │  ├─ node
│  │  │  ├─ 1.0.0
│  │  │  │  ├─ node-1.0.0.tgz
├─ npm_tree_20230101_121415.zip
├─ npm_tree_20230102_121415.zip
```