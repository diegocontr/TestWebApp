from flask import Flask, render_template, request, jsonify
import numpy as np
from scipy.integrate import solve_ivp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    initial_angle = float(request.form['initial_angle'])
    damping_coefficient = float(request.form['damping_coefficient'])
    
    result = run_simulation(initial_angle, damping_coefficient)
    return jsonify(result)

def run_simulation(initial_angle, damping_coefficient, duration=100, step_size=0.1):
    def damped_pendulum(t, y):
        theta, omega = y
        return [omega, -damping_coefficient * omega - 9.81 * np.sin(theta)]

    y0 = [np.radians(initial_angle), 0]
    t_eval = np.arange(0, duration, step_size)
    sol = solve_ivp(damped_pendulum, (0, duration), y0, t_eval=t_eval)

    return {'time': sol.t.tolist(), 'angle': sol.y[0].tolist()}

if __name__ == '__main__':
    app.run(debug=True)
