import numpy as np
import pickle
from sklearn.linear_model import LinearRegression

# Data Dummy: Pengeluaran Iklan (juta rupiah) dan Penjualan (ribu unit)
X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)  # Pengeluaran iklan
Y = np.array([10, 20, 25, 40, 50, 55, 65, 80, 85, 95])  # Penjualan

# Membuat model regresi linear
model = LinearRegression()
model.fit(X, Y)

# Simpan model ke file
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)
