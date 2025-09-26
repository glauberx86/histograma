import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

def read_file(file_stream):
    try:
        return pd.read_csv(file_stream)
    except Exception as e:
        raise ValueError(f"Erro ao processar o arquivo CSV: {e}")

def gen_hist(data, title, bins, color, x_label, y_label):
    if data is None or data.empty:
        raise ValueError("Não foi possível gerar o gráfico pois o conjunto de dados está vazio.")

    fig, ax = plt.subplots()
    ax.hist(data, bins=bins, color=color, edgecolor='black')
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')

    stats = {
        'count': int(data.count()),
        'mean': float(data.mean()),
        'std': float(data.std()),
        'min': float(data.min()),
        'max': float(data.max())
    }

    return img_base64, stats

def parse_text(text_data):
    try:
        items = text_data.replace(',', ' ').split()
        numeric_data = pd.to_numeric(pd.Series(items), errors='coerce').dropna()
        if numeric_data.empty:
            raise ValueError("Nenhum dado numérico válido foi encontrado no texto inserido.")
        return numeric_data
    except Exception as e:
        raise ValueError(f"Erro ao processar os dados de texto: {e}")