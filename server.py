from bottle import route, run, template, static_file


binarycounter = 0

@route('/static/<file_path:path>')
def static(file_path):
    return static_file(file_path, root='./static')

@route('/example/binarycounter')
def index():
    global binarycounter
    binarycounter = binarycounter + 1
    return template(
        '<?xml version="1.0" encoding="utf-8" ?> \
        <pins> \
        <pin name="LED1" value="{{LED1_value}}" /> \
        <pin name="LED2" value="{{LED2_value}}" /> \
        <pin name="LED3" value="{{LED3_value}}" /> \
        </pins>' 
        , LED1_value=(binarycounter // 4) % 2 \
        , LED2_value=(binarycounter // 2) % 2 \
        , LED3_value=(binarycounter // 1) % 2)

run(host='XXX.XXX.XXX.XXX', port=8080)
