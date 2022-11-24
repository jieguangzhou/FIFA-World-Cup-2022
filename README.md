# FIFA-World-Cup-2022
DolphinScheduler machine learning "FIFA World Cup 2022" betting workflow

In this project, we will use machine learning to **predict which country will win the FIFA World Cup 2022** and **get a betting strategy every day**.



## Step-1 start DolphinScheduler



we can start a [Dolphinscheduler](https://dolphinscheduler.apache.org) standalone server using Docker

```shell
docker run --name dolphinscheduler-standalone-server -p 12345:12345 -p 25333:25333 -d jalonzjg/dolphinscheduler-fifa
```

And then, you can log in to the DolphinScheduler at http://localhost:12345/dolphinscheduler/ui

user: admin
password: dolphinscheduler123

![image-20221124232236471](img/image-20221124232236471.png)

## Step-2 submit workflow



```shell
python3 -m pip install apache-dolphinscheduler==3.1.1
```

```shell
export PYDS_HOME=./
python3 pyds.py
```



You can click the `Project` -> `FIFA`

![image-20221124231716302](img/image-20221124231716302.png)



Then, we can see 3 workflow

- training: Use FLAML to train model
- predict: Use the model to predict which country will win the World Cup
- betting-strategy: Get betting strategy every day

![image-20221124231751744](img/image-20221124231751744.png)



## Step-3 run workflow



### start training workflow

![image-20221124231816267](img/image-20221124231816267.png)



We can view log after the workflow had finished

![image-20221124231849652](img/image-20221124231849652.png)



### Start predict workflow

We can view log after the workflow had finished

![image-20221124232014546](img/image-20221124232014546.png)



## Start betting strategy

![image-20221124232037988](img/image-20221124232037988.png)



`$[yyyy-MM-dd]`mean dolphinscheduler will use  the current year, month and day as a parameter, we can also set it to `2022-11-26` other date.



![image-20221124232109784](img/image-20221124232109784.png)
