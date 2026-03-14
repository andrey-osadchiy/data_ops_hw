import os
from typing import Any
import dockerspawner
from traitlets.config.application import get_config

c: Any = get_config()

# Hub internal config
c.JupyterHub.hub_ip = "0.0.0.0"
c.JupyterHub.hub_port = 8010
c.JupyterHub.hub_connect_ip = "jph"

# Persist hub state in /data
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"
c.ConfigurableHTTPProxy.pid_file = "/data/jupyterhub-proxy.pid"

# Auth (для ДЗ — простой dummy)
c.JupyterHub.admin_users = {os.environ.get("JPH_ADMIN_USER", "admin")}
c.JupyterHub.authenticator_class = "dummy"
c.DummyAuthenticator.password = os.environ["JPH_DUMMY_PASSWORD"]

# Spawner: each user gets own container
c.JupyterHub.spawner_class = dockerspawner.DockerSpawner

c.DockerSpawner.image = os.getenv("DOCKER_NOTEBOOK_IMAGE", "jupyterhub/singleuser")
c.DockerSpawner.cmd = os.getenv("DOCKER_SPAWN_CMD", "start-singleuser.sh")
notebook_dir = os.getenv("DOCKER_NOTEBOOK_DIR", "/home/jovyan")
c.DockerSpawner.notebook_dir = notebook_dir

# per-user persistent volume (docker named volume)
c.DockerSpawner.volumes = {"jupyter-user-{username}": notebook_dir}

# network where hub and singleuser containers can see each other
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = os.environ["DOCKER_NETWORK_NAME"]

# cleanup user containers after stop
c.DockerSpawner.remove = True
c.DockerSpawner.debug = True
