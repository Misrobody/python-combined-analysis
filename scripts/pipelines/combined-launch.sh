#!/bin/bash

# uxsim
#./scripts/pipelines/combined-model.sh data/uxsim/operation-execution-logs data/uxsim/pyparse-core combined-uxsim-core > uxsim.log
#./scripts/pipelines/combined-model.sh data/uxsim/operation-execution-logs data/uxsim/pyparse combined-uxsim-extended > uxsim2.log


# anytree
#./scripts/pipelines/combined-model.sh data/anytree/operation-execution-log data/anytree/pyparse-core combined-anytree-core > anytree.log
#./scripts/pipelines/combined-model.sh data/anytree/operation-execution-log data/anytree/pyparse combined-anytree-extended > anytree2.log

#pillow
#./scripts/pipelines/combined-model.sh data/pillow/dynamic data/pillow/static combined-pillow > pillow.log


./scripts/pipelines/combined-model.sh data/scipy/dynamic data/scipy/static combined-scipy > scipy.log

