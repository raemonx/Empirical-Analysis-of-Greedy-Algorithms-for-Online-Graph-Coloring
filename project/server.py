from flask import Flask, render_template, request, url_for

from project.cbip import execute_cbip
from project.first_fit import execute_first_fit
from project.graph_generator import generate_graphs

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        k = int(request.form['k'])
        n = int(request.form['n'])
        N = int(request.form['N'])
        algorithm = request.form['algorithm']

        graphs = generate_graphs(k, N, n)

        impossible = url_for('static', filename='img.png')
        draw = None
        solutions = dict()
        chosen_graph_id = None
        for graph in graphs:
            sol = None
            if algorithm == 'FirstFit':
                sol = execute_first_fit(graph)
            elif algorithm == 'CBIP':
                sol = execute_cbip(graph)
            if impossible and sol.vertex_to_color:
                impossible = None
                draw = sol.draw()
                chosen_graph_id = graph.graph_id
            solutions[graph.graph_id] = [sol.get_color_count(), sol.get_competitive_ratio()]

        avg_color_count = round(sum(sol[0] for sol in solutions.values()) / len(solutions), 3)
        avg_comp_ratio = round(sum(sol[1] for sol in solutions.values()) / len(solutions), 3)

        return render_template('index.html',
                               graph=draw,
                               avg_num_colors=avg_color_count,
                               avg_competitive_ratio=avg_comp_ratio,
                               solutions=solutions,
                               k=k,
                               n=n,
                               N=N,
                               algorithm=algorithm,
                               possible=impossible,
                               chosen_graph_id=chosen_graph_id)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5001)
