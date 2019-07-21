from app import app

@app.route('/')
@app.route('/index')
def index():
    return '''
<!DOCTYPE html>
<html lang="en-US">
    <head>
        <meta charset="utf-8">
        <title>BurnerLog</title>
    </head>
    <body>
        <h1>BurnerLog</h1>
        <h2>by Stevie Slotterback</h2>
        <h2>Copyright 2019</h2>
        <p>This application, when completed, will enable technicians to track 
           parts changed during maintenance visits.</p>
    </body>
</html> 
'''
