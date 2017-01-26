# pysciencedock

Scientific and statistical methods from Python exposed through Docker.

## Local usage

List methods available with JSON descriptions of inputs and outputs:
```
python -m pysciencedock
```

Print help information for a method:
```
python -m pysciencedock <method> --help
```

Run one of the methods:
```
python -m pysciencedock <method> <arg1> ...
```

## Usage through Docker

Build the Docker image:
```
git clone ...
cd pysciencedock
docker build -t pysciencedock .
```

List the methods available through Docker:
```
docker run pysciencedock
```

Run a method through Docker:
```
docker run <docker_options> pysciencedock <method> <arg1> ...
```

In order to send data files to Docker, mount a volume and use the mounted
volume prefix for the input and output paths. For example, if `myinput.csv`
is in your current directory, the following will produce `myoutput.csv` in
the current directory:
```
docker run -v $PWD:/mnt/data pysciencedock normalize --data=/mnt/data/myinput.csv --output=/mnt/data/myoutput.csv
```

## Usage through Girder

* Install Girder.
* Enable the "Item tasks" plugin.
* Start a `girder_worker` Celery worker and point it and the Worker plugin settings to use the same task queue.
* From any folder you have write access to (you must be admin), select
  "Add tasks" from the actions menu.
* Enter "kitware/pysciencedock" as the image name and click Run.
* When that task completes, navigate to a created task item and select
  "Run task" from the actions menu.
* Fill in the task parameters and click Run.
