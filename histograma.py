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
    counts, bin_edges, patches = ax.hist(data, bins=bins, color=color, edgecolor='black')

    # Intervalo de classe
    bin_labels = [f"{bin_edges[i]:.2f} - {bin_edges[i + 1]:.2f}" for i in range(len(bin_edges) - 1)]
    tick_positions = (bin_edges[:-1] + bin_edges[1:]) / 2
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(bin_labels, rotation=45, ha='right')

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')

    class_count = len(bin_edges) - 1
    class_interval = bin_edges[1] - bin_edges[0] if class_count > 0 else 0

    stats = {
        'count': int(data.count()),
        'mean': float(data.mean()),
        'std': float(data.std()),
        'min': float(data.min()),
        'max': float(data.max()),
        'classes': class_count,
        'interval': float(class_interval)
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