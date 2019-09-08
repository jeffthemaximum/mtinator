# mtinator

Mtinator (pronouced em-tinator) is my _attempt_ to create the following:

A small web service that does the following things:
- Continuously monitors the status of MTA service to see whether a line is delayed or not.
- When a line transitions from not delayed → delayed, you should print the following message to console or to a logfile: “Line <line_name> is experiencing delays”.
- Similarly, when a line transitions from delayed → not delayed, you should print the following message to console or to a logfile: “Line <line_name> is now recovered”.
- Exposes an endpoint called /status, which takes the name of a particular line as an argument and returns whether or not the line is currently delayed.
- Exposes an endpoint called /uptime, which also takes the name of a particular line as an argument and returns the fraction of time that it has not been delayed since inception. More concretely, “uptime” is defined as 1 - (total_time_delayed / total_time)

# requirements
- python 3.7.4
    - This has only been run against 3.7.4. It will likely work with 3.6+, but that's a guess at this point.
- sqlite 3.24.0
    - Similar to above, it has only been tested with 3.24.0, but likely works with other versions
- a valid MTA api key
    - register at https://datamine.mta.info

# To run
- clone the repo
- (optional): create and activate a virtual environment
- In terminal, run
```
pip install -r requirements.txt
export FLASK_APP=application.py
export MTA_API_KEY={your valid MTA api key}
flask db upgrade
flask run
```
- Once the flask app is running, to start the background task of streaming MTA subway data to update the database, do a CURL request:
```
curl -X POST \
  http://127.0.0.1:5000/services \
  -H 'Content-Type: application/json' \
  -d '{
	"name": "status",
	"state": "start"
}'
```

# Endpoint documentation

### GET /status
- `/status?name={mta_subway_line}`
- example request
    - `/status?name=6`
- example response
```
{
    "line": "6",
    "status": "not delayed"
}
```
- `status` value will always be either `delayed` or `not delayed`
- `line` will always be the `mta_subway_line` value requested
- Endpoint will return 200 http status on successful responses
- Endpoint will return 404 http status on expected errors, including
    - missing name query param
    - name query param not a valid subway line, such as a request to `/status?name=drew`
- Endpoint will return 500 http status on unexpected errors.

### GET /uptime
- `/uptime?name={mta_subway_line}`
- example request
    - `/uptime?name=6`
- example response
```
{
    "line": "6",
    "uptime": "0.95828174"
}
```
- `uptime` value will always be a string containing a float value rounded to at most 8 decimal points.
- `line` will always be the `mta_subway_line` value requested
- Endpoint will return 200 http status on successful responses
- Endpoint will return 404 http status on expected errors, including
    - missing name query param
    - name query param not a valid subway line, such as a request to `/status?name=drew`
- Endpoint will return 500 http status on unexpected errors.

### POST /service
- example request
```
POST /services? HTTP/1.1
Content-Type: application/json
{
	"name": "status",
	"state": "start"
}
```
- example response
```
{
    "name": "status",
    "state": "start"
}
```
- `name` value must always be `"status"`
- `"state"` value must always be either `"start"` or `"stop"`
- This above example request will start the background task to stream MTA subway data and update the database.
