from flask import Flask, render_template, request, flash, redirect, url_for
import numpy as np
import pandas as pd
import pickle
import json
from werkzeug.utils import secure_filename
import os
from sklearn.linear_model import LinearRegression
import io

# Konfigurasi upload
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

# Buat folder uploads jika belum ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'rahasia123'  # Diperlukan untuk flash messages

# Load model regresi yang sudah disimpan
try:
    with open("model.pkl", "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    # Jika model belum ada, buat model baru dengan data dummy
    X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)
    y = np.array([10, 20, 25, 40, 50, 55, 65, 80, 85, 95])
    model = LinearRegression()
    model.fit(X, y)
    with open("model.pkl", "wb") as file:
        pickle.dump(model, file)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def prepare_plot_data(X, y, model):
    try:
        # Data untuk scatter plot
        scatter_data = [{'x': float(x), 'y': float(y)} for x, y in zip(X.flatten(), y)]
        
        # Data untuk garis regresi
        X_min = float(min(X))
        X_max = float(max(X))
        X_line = np.array([[X_min], [X_max]])
        y_line = model.predict(X_line)
        regression_line = [
            {'x': X_min, 'y': float(y_line[0])},
            {'x': X_max, 'y': float(y_line[1])}
        ]
        
        return scatter_data, regression_line
    except Exception as e:
        print(f"Error in prepare_plot_data: {str(e)}")
        return [], []

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    show_plot = False
    scatter_data = []
    regression_line = []
    
    if request.method == "POST":
        try:
            # Ambil input pengeluaran iklan dari form
            advertising_budget = float(request.form["budget"])
            # Lakukan prediksi
            prediction = float(model.predict([[advertising_budget]])[0])
            
            # Persiapkan data untuk plot
            X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)
            y = np.array([10, 20, 25, 40, 50, 55, 65, 80, 85, 95])
            scatter_data, regression_line = prepare_plot_data(X, y, model)
            show_plot = True
            
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
            prediction = None

    return render_template("index.html", 
                         prediction=prediction,
                         show_plot=show_plot,
                         scatter_data=json.dumps(scatter_data),
                         regression_line=json.dumps(regression_line))

@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    prediction = None
    show_plot = False
    scatter_data = []
    regression_line = []
    
    if 'file' not in request.files:
        flash('Tidak ada file yang dipilih', 'danger')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('Tidak ada file yang dipilih', 'danger')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        try:
            # Baca file CSV langsung dari memory
            df = pd.read_csv(file)
            
            # Pastikan kolom yang diperlukan ada
            if len(df.columns) < 2:
                flash('File CSV harus memiliki minimal 2 kolom', 'danger')
                return redirect(url_for('index'))
            
            # Ambil dua kolom pertama
            df = df.iloc[:, :2]
            
            try:
                # Konversi kolom ke float
                X = df.iloc[:, 0].astype(float).values.reshape(-1, 1)
                y = df.iloc[:, 1].astype(float).values
            except ValueError:
                flash('Data tidak valid. Pastikan kedua kolom berisi angka desimal yang valid (contoh: 1.5, 2.3)', 'danger')
                return redirect(url_for('index'))
            
            # Buat dan latih model baru
            global model
            model = LinearRegression()
            model.fit(X, y)
            
            # Simpan model baru
            with open("model.pkl", "wb") as f:
                pickle.dump(model, f)
            
            # Persiapkan data untuk plot
            scatter_data, regression_line = prepare_plot_data(X, y, model)
            show_plot = True
            
            # Buat prediksi contoh
            prediction = float(model.predict([[X[0][0]]])[0])
            
            flash('Model berhasil diperbarui dengan data baru!', 'success')
            return render_template("index.html",
                                prediction=prediction,
                                show_plot=show_plot,
                                scatter_data=json.dumps(scatter_data),
                                regression_line=json.dumps(regression_line))
            
        except pd.errors.EmptyDataError:
            flash('File CSV kosong', 'danger')
        except pd.errors.ParserError:
            flash('Format CSV tidak valid', 'danger')
        except Exception as e:
            flash(f'Error dalam memproses file: {str(e)}', 'danger')
        
        return redirect(url_for('index'))
    
    flash('Format file tidak diizinkan', 'danger')
    return redirect(url_for('index'))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

