from __future__ import unicode_literals

from nodeconductor.core.permissions import FilteredCollaboratorsPermissionLogic, StaffPermissionLogic
from nodeconductor.structure import models as structure_models


PERMISSION_LOGICS = (
    ('nodeconductor_cost_planning.DeploymentPlan', FilteredCollaboratorsPermissionLogic(
        collaborators_query='customer__roles__permission_group__user',
        collaborators_filter={
            'customer__roles__role_type': structure_models.CustomerRole.OWNER,
        },
        any_permission=True,
    )),
    ('nodeconductor_cost_planning.Category', StaffPermissionLogic(any_permission=True)),
    ('nodeconductor_cost_planning.Configuration', StaffPermissionLogic(any_permission=True)),
)
