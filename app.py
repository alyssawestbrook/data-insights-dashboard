from flask import Flask, request, render_template
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    stats = None
    chart_path = None
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            df = pd.read_csv(filepath)

            stats = df.describe().to_html()

            numeric_cols = df.select_dtypes(include='number').columns
            if len(numeric_cols) > 0:
                plt.figure()
                df[numeric_cols[0]].hist()
                chart_path = os.path.join('static', 'chart.png')
                os.makedirs('static', exist_ok=True)
                plt.savefig(chart_path)
                plt.close()

    return render_template('index.html', stats=stats, chart_path=chart_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')