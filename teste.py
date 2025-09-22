from flask import Flask, render_template, Response
import matplotlib.pyplot as plt
import numpy as np
import io

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/hist.png")
def hist_png():
    # Dados
    n = np.random.randn(1000)

    # Plot
    fig, ax = plt.subplots()
    ax.hist(n, bins=20, color="skyblue", edgecolor="black")
    ax.set_title("Teste Histograma")
    ax.set_xlim((min(n), max(n)))

    output = io.BytesIO()
    plt.savefig(output, format="png")
    plt.close(fig)
    output.seek(0)

    return Response(output.getvalue(), mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
