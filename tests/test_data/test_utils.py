import hydra

from core_lib.core_lib import CoreLib


def sync_create_core_lib_config(path: str):
    [CoreLib.cache_registry.unregister(key) for key in CoreLib.cache_registry.registered()]
    [CoreLib.observer_registry.unregister(key) for key in CoreLib.observer_registry.registered()]
    config_file = 'user_agreement_core_lib.yaml'
    hydra.core.global_hydra.GlobalHydra.instance().clear()
    hydra.initialize(config_path=path)
    config = hydra.compose(config_file)
    return config
