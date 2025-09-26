from flask import Flask, render_template, request
import pandas as pd
from histograma import read_file, parse_text, gen_hist

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", error=None)

@app.route("/generate_histogram", methods=["POST"])
def generate_histogram_route():
    try:
        #mapCollum = {col.lower(): col for col in df.columns}
        data_input = request.form.get('data_input')
        csv_file = request.files.get('csv_file')
        data_series = None

        if csv_file and csv_file.filename != '':
            df = read_file(csv_file.stream)
            column_name = request.form.get('collum')

            if not column_name:
                raise ValueError("Por favor, especifique o nome da coluna a ser analisada.")

            if column_name not in df.columns:
                raise ValueError(f"A coluna '{column_name}' não foi encontrada. Colunas disponíveis: {list(df.columns)}")

            if pd.api.types.is_numeric_dtype(df[column_name]):
                data_series = df[column_name].dropna()
            else:
                raise ValueError(f"A coluna '{column_name}' não contém dados numéricos.")

        elif data_input:
            data_series = parse_text(data_input)
            
        else:
            raise ValueError("Nenhum dado foi fornecido (nem texto, nem arquivo CSV).")

        bins_input = request.form.get('bins', 'auto').strip().lower()
        allowed_rules = ['auto', 'sturges', 'sqrt']
        bins = None

        if bins_input in allowed_rules:
            bins = bins_input
        else:
            try:
                bins = int(bins_input)
                if bins <= 0:
                    raise ValueError("O número de colunas (bins) deve ser um inteiro positivo.")
            except ValueError:
                raise ValueError(f"Regra para bins inválida. Use um número ou uma das regras: {allowed_rules}")

        title = request.form.get('title', 'Histograma')
        color = request.form.get('color', 'blue')
        x_label = request.form.get('x_label', 'Valores')
        y_label = request.form.get('y_label', 'Frequência')

        img_data, stats = gen_hist(
            data_series, title, bins, color, x_label, y_label
        )
        
        return render_template('result.html', title=title, img_data=img_data, stats=stats)

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == "__main__":
    app.run(debug=True)