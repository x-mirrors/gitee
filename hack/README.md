## Usage

- change dir

```
cd hack
```

- create env

```
virtualenv .venv
```

- use env

```
source ./.venv/bin/activate
```

- install dep

```
pip3 install -r requirements.txt
```

- help

```
$ python render.py
usage: render.py [-h] [--readme | --no-readme | -r] [--workflows | --no-workflows | -w]

Render README.md/github workflows

optional arguments:
  -h, --help            show this help message and exit
  --readme, --no-readme, -r
                        render readme (default: False)
  --workflows, --no-workflows, -w
                        render workflows (default: False)
$ python3 render.py --readme
$ python3 render.py --workflows
```
