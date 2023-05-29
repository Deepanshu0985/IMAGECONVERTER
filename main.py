import os
    
from flask import Flask,render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import cv2

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER='uploads'
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.secret_key="secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def home():
    return render_template( "index.html")

@app.route('/about')
def about():
    return render_template( "index.html")

def processimage(filename,operation):
    print(f"the operation is {operation} and thre filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "gsc":
            nfilename=f"static/{filename}"
            imgprocessed = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            cv2.imwrite(nfilename,imgprocessed)
            return nfilename
        case "png":
            nfilename=f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(nfilename,img)
            return nfilename
        case "jpg":
            nfilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(nfilename,img)
            return nfilename
        case "webp":
            nfilename=f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(nfilename,img)
            return nfilename

    
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    operation = request.form.get("operation")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return "redirect(request.url)"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processimage(filename,operation)
            flash(f"your image has been processed and available <a href='/{new}' target='blank'>here</a>")
            return render_template("index.html")
    return render_template("index.html")


app.run(debug=True)