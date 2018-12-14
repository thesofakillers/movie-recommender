"""
Runs the flask app
"""


from pellicola import app

# to allow server to be run with "python pellicola.py" -- no need for ENV vars
if __name__ == '__main__':
    app.run(debug=False)
