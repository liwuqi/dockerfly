BASE_PATH=$(cd "$(dirname "$0")"; pwd)
LOG_FILE=$BASE_PATH/web.log
PID_FILE=$BASE_PATH/web.pid

if [ -f "$PID_FILE" ]; then
    cat $PID_FILE | xargs kill -9
fi

ps aux|grep dockerflyd|grep -v grep|awk '{print $2}'|xargs kill
python  $BASE_PATH/dockerfly/bin/dockerflyd.py
echo "dockerflyd Server is running"

nohup python $BASE_PATH/dockerflyui/servers.py 0.0.0.0 80 $1 > $LOG_FILE 2>&1 & echo $! > $PID_FILE
echo "dockerflyui Server is running"
