# FIFA-World-Cup-2022
DolphinScheduler machine learning "FIFA World Cup 2022" betting workflow

## step-1 start DolphinScheduler

we can start a Dolphinscheduler standalone server using Docker

```
docker run --name dolphinscheduler-standalone-server -p 12345:12345 -p 25333:25333 -d jalonzjg/dolphinscheduler-fifa
```

And then, you can login the DolphinScheduler in http://localhost:12345/dolphinscheduler/ui

user: admin
password: dolphinscheduler123

## step-2 submit workflow

```
pip install apache-dolphinscheduler==3.1.1

```

```
export PYDS_HOME=./
python pyds.py

```
