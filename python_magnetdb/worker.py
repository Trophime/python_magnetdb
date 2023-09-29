import os

from celery import Celery

import python_magnetdb.database
from python_magnetdb.models.server import Server
from python_magnetdb.models.simulation import Simulation

app = Celery('tasks', broker=os.getenv('REDIS_ADDR') or 'redis://localhost:6379/0')


@app.task
def run_simulation(simulation_id, server_id, cores):
    from .actions.run_simulation import run_simulation
    from .actions.run_ssh_simulation import run_ssh_simulation
    if server_id is not None:
        return run_ssh_simulation(Simulation.find(simulation_id), Server.find(server_id), cores)
    else:
        return run_simulation(Simulation.find(simulation_id))


@app.task
def run_simulation_setup(simulation_id):
    from .actions.run_simulation_setup import run_simulation_setup
    return run_simulation_setup(Simulation.find(simulation_id))
