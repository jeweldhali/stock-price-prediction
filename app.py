from flask import Flask, render_template, request
import numpy as np
import tensorflow
from tensorflow.keras.models import load_model
new_model = load_model("stock.h5")

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('original.html')


@app.route("/predict", methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        try:
            x1 = int(request.form['x1'])
            x2 = int(request.form['x2'])
            x3 = int(request.form['x3'])
            x4 = int(request.form['x4'])
            x5= int(request.form['x5'])
            x_input = np.array([x1, x2, x3,x5,x5])
            temp_input=list(x_input)
            n_steps = 5
            n_features = 1
            lst_output=[]
            i=0
            while(i<5):
                if(len(temp_input)>5):
                    x_input=np.array(temp_input[1:])
                    #print("{} day input {}".format(i,x_input))
                    #print(x_input)
                    x_input = x_input.reshape((1, n_steps, n_features))
                    #print(x_input)
                    yhat = new_model.predict(x_input, verbose=0)
                    #print("{} day output {}".format(i,yhat))
                    temp_input.append(yhat[0][0])
                    temp_input=temp_input[1:]
                    #print(temp_input)
                    lst_output.append(yhat[0][0])
                    i=i+1
                else:
                    x_input = x_input.reshape((1, n_steps, n_features))
                    yhat = new_model.predict(x_input, verbose=0)
                    #print(yhat[0])
                    temp_input.append(yhat[0][0])
                    lst_output.append(yhat[0][0])
                    i=i+1

            lst1 = round(lst_output[0],2)
            lst2 = round(lst_output[1],2)
            lst3 = round(lst_output[2],2)
            lst4 = round(lst_output[3],2)
            lst5 = round(lst_output[4],2)

        except valueError:
            return "Please check if the values are entered correctly"
    return render_template('predict.html', prediction = lst1, prediction1 = lst2, prediction2 = lst3,prediction3 = lst4,prediction4 = lst5)

if __name__ == '__main__':
    app.run()
