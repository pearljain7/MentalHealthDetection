from flask import Flask, flash, redirect, url_for, render_template, request, send_from_directory
import numpy as np
import re
import sys
import os
import tensorflow as tf
from keras.models import load_model
from joblib import load
from depression_detection_tweets import process_message

app=Flask(__name__)

# def auc(y_true, y_pred):
#    auc = tf.metrics.auc(y_true, y_pred)[1]
#    keras.backend.get_session().run(tf.local_variables_initializer())
#    return auc

# load the model, and pass in the custom metric function
#global graph
#model = tf.keras.models.load_model('/Users/pearl/Desktop/hack/Covid.h5', custom_objects={'auc': auc})

# initialize these variables

#import base64
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        testURL= "file:///Users/pearl/Desktop/index.html"
        # check if the post request has the file part
        sc_tf_idf=load("dep_class.joblib")
        # if user does not select file, browser also
        # submit an empty part without filename
        file1=request.form['file']
        file2=request.form['file1']
        file3=request.form['file2']
        name=request.form['fname']
        if (file1 == '' or file2 == ''):
            print('No selected file')
            return redirect(request.url)
        if file1 and file2:
            pm=process_message(file1)
            res1=sc_tf_idf.classify(pm)
            pm1=process_message(file2)
            res2=sc_tf_idf.classify(pm1)
            pm2=process_message(file3)
            res3=sc_tf_idf.classify(pm2)
            if (str(res1) == 'False' and str(res2) == 'False' and str(res3)=='False'):
                result = 'extremely low chances of being depressed'
            elif (str(res1) == 'False' and str(res2) == 'False' and str(res3)=='True'):
                result = 'low chances of being depressed'
            elif (str(res1) == 'False' and str(res2) == 'True' and str(res3)=='False'):
                result = 'low chances of being depressed'
            elif (str(res1) == 'False' and str(res2) == 'True' and str(res3)=='True'):
                result = 'high chances of being depressed'
            elif (str(res1) == 'True' and str(res2) == 'False' and str(res3)=='False'):
                result = 'low chances of being depressed'
            elif (str(res1) == 'True' and str(res2) == 'False' and str(res3)=='True'):
                result = 'high chances of being depressed'
            elif (str(res1) == 'True' and str(res2) == 'True' and str(res3)=='False'):
                result = 'high chances of being depressed'
            elif (str(res1) == 'True' and str(res2) == 'True' and str(res3)=='True'):
                result = 'extremely high chances of being depressed'
        return render_template("page2.html", result=result, name=name,testURL=testURL)

    return render_template("login.html" )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["name"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"


#STARTING OF THE INTEGRATION OF APPOINT


if __name__ == "__main__":
    app.run(port=5000, debug=True)