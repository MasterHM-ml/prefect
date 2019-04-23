import os

import prefect
from prefect.environments.execution.base import Environment
from prefect.environments.storage import Storage


class LocalEnvironment(Environment):
    """
    A LocalEnvironment class for executing a flow contained in Storage in the local process.
    Execution will first attempt to call `get_flow` on the storage object, and if that fails it will
    fall back to `get_env_runner`.  If `get_env_runner` is used, the environment variables from this
    process will be passed.
    """

    def __init__(self) -> None:
        pass

    def execute(self, storage: "Storage", flow_location: str) -> None:
        """
        Executes the flow for this environment from the storage parameter,
        by calling `get_flow` on the storage; if that fails, `get_env_runner` will
        be used with the OS environment variables inherited from this process.

        Args:
            - storage (Storage): the Storage object that contains the flow
            - flow_location (str): the location of the Flow to execute
        """
        try:
            runner = storage.get_flow(flow_location)
            runner.run()
        except NotImplementedError:
            runner = storage.get_env_runner(flow_location)
            current_env = os.environ.copy()
            runner(env=current_env)
