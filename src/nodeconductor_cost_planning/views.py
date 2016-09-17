from rest_framework import viewsets, permissions, exceptions
from rest_framework.filters import DjangoFilterBackend

from nodeconductor.structure import filters as structure_filters

from . import models, serializers, filters


class DeploymentPlanViewSet(viewsets.ModelViewSet):
    queryset = models.DeploymentPlan.objects.all()
    serializer_class = serializers.DeploymentPlanSerializer
    lookup_field = 'uuid'
    filter_backends = (structure_filters.GenericRoleFilter, DjangoFilterBackend)
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoObjectPermissions)
    filter_class = filters.DeploymentPlanFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return serializers.DeploymentPlanCreateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """
        Create new deployment plan
        """
        customer = serializer.validated_data['customer']
        if not customer.has_user(self.request.user) and not self.request.user.is_staff:
            raise exceptions.PermissionDenied()

        super(DeploymentPlanViewSet, self).perform_create(serializer)

    def retrieve(self, request, *args, **kwargs):
        """
        Example rendering of deployment plan and configuration.

        .. code-block:: javascript

            GET /api/deployment-plans/c218cbb2f56c4d52a82638ca9fffd85a/
            Accept: application/json
            Content-Type: application/json
            Authorization: Token c84d653b9ec92c6cbac41c706593e66f567a7fa4
            Host: example.com

            {
                "url": "http://example.com/api/deployment-plans/b12bb98a661749ffb02c8a8439299288/",
                "uuid": "b12bb98a661749ffb02c8a8439299288",
                "name": "Webapp for Monster Inc",
                "customer": "http://example.com/api/customers/790b3c131e894581b3dcf66796d9fa30/",
                "items": [
                    {
                        "preset": {
                            "url": "http://example.com/api/deployment-presets/628cd853ba2a4ce7af5d4fff510b5bd2/",
                            "uuid": "628cd853ba2a4ce7af5d4fff510b5bd2",
                            "name": "MySQL",
                            "category": "Databases",
                            "variant": "Large"
                        },
                        "quantity": 1,
                        "total_price": 182.23
                    }
                ],
                "service": "http://example.com/api/azure/54121cd1cde24b73a1c194d74a305cd2/",
                "total_price": 182.23
            }
        """
        return super(DeploymentPlanViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Example request for creating deployment plan.

        .. code-block:: javascript

            POST /api/deployment-plans/
            Accept: application/json
            Content-Type: application/json
            Authorization: Token c84d653b9ec92c6cbac41c706593e66f567a7fa4
            Host: example.com

            {
                "name": "WebApps",
                "customer": "http://example.com/api/customers/2f8b4e0f101545508d52c7655d6386c8/",
                "service": "http://example.com/api/azure/54121cd1cde24b73a1c194d74a305cd2/",
                "items": [
                    {
                        "preset": "http://example.com/api/deployment-presets/2debb6d109954afaa03910ba1c6791a6/",
                        "quantity": 1
                    }
                ]
            }
        """
        return super(DeploymentPlanViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Run **PUT** request against */api/deployment-plans/<uuid>/* to update deployment plan.
        Only name and list of items can be updated.
        List of items should have the same format as POST request.
        Only customer owner and staff can update deployment plan.
        """
        return super(DeploymentPlanViewSet, self).update(request, *args, **kwargs)


class PresetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Preset.objects.all()
    serializer_class = serializers.PresetSerializer
    lookup_field = 'uuid'
    permission_classes = (permissions.IsAuthenticated,)
