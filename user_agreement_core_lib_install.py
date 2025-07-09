#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import hydra

from user_agreement_core_lib.user_agreement_core_lib import UserAgreementCoreLib

@hydra.main(config_name='core_lib_config', version_base='1.1')
def main(cfg):
    UserAgreementCoreLib.install(cfg)

if __name__ == '__main__':
    main()
