from flask import *
from translator import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'

indo_2_sunda = loadDictionary("indonesia.txt", False)
sunda_2_indo = loadDictionary("sunda.txt", True)

@app.route("/")
def root():
    output = ""
    text = ""
    target = ""
    algo = ""
    if ("text" in request.args) and ("target" in request.args) and ("algo" in request.args):
        # Get arguments
        text = request.args["text"]
        target = request.args["target"]
        algo = request.args["algo"]

        # Set up parameters based on target
        dictionary = None
        if (target == "indonesia"):
            dictionary = sunda_2_indo
            remove_particle = True
            add_particle = False
        elif (target == "sunda"):
            dictionary = indo_2_sunda
            remove_particle = False
            add_particle = True

        # Set up parameters based on target
        matcher = None
        if (algo == "bm"):
            matcher = bm_matcher
        elif (algo == "kmp"):
            matcher = kmp_matcher
        elif (algo == "re"):
            matcher = regex_matcher
        
        if (dictionary != None) and (matcher != None):
            output = translate(text, matcher, dictionary, remove_particle, add_particle)

    return render_template("index.html", result=output, text=text, target=target, algo=algo)
