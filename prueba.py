from flask import Flask, render_template, request, flash, redirect, url_for
import enrcyptAndDecrypt as ead

app = Flask(__name__)




@app.route('/',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      mensaje = request.form['nm']
      if mensaje=="" or mensaje == None:
          return render_template("index.html", output="ERROR! el campo de entrada no puede ser vacío, intente de nuevo ")
      if 'encrypt' == request.form.get('action'):
          respuesta=ead.main("encrypt",mensaje)
          return render_template("index.html", output=respuesta)
      elif 'decrypt' == request.form.get('action'):
          respuesta = ead.main("decrypt", mensaje)
          return render_template("index.html", output=respuesta)

   else:
       return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)