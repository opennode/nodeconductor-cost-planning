from ddt import ddt, data
from rest_framework import status, test

from nodeconductor.structure.tests import factories as structure_factories

from . import factories, fixtures
from .. import models


@ddt
class DeploymentPlanListTest(test.APITransactionTestCase):
    def setUp(self):
        self.fixture = fixtures.CostPlanningFixture()
        self.deployment_plan = self.fixture.deployment_plan

    @data('staff', 'owner', 'global_support')
    def test_user_with_permissions_can_list_deployment_plans(self, user):
        response = self.get_deployment_plans(getattr(self.fixture, user))
        self.assertEqual(len(response.data), 1)

    @data('user', 'manager', 'admin')
    def test_user_without_permissions_cannot_list_deployment_plans(self, user):
        response = self.get_deployment_plans(getattr(self.fixture, user))
        self.assertEqual(len(response.data), 0)

    def test_deployment_plans_can_be_filtered_by_customer(self):
        self.client.force_authenticate(self.fixture.staff)
        customer = structure_factories.CustomerFactory()
        response = self.client.get(factories.DeploymentPlanFactory.get_list_url(), {
            'customer': customer.uuid.hex
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def get_deployment_plans(self, user):
        self.client.force_authenticate(user=user)
        response = self.client.get(factories.DeploymentPlanFactory.get_list_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response


@ddt
class DeploymentPlanCreateTest(test.APITransactionTestCase):

    def setUp(self):
        self.fixture = fixtures.CostPlanningFixture()

    @data('owner', 'staff')
    def test_user_with_permissions_can_create_deployment_plan(self, user):
        response = self.create_deployment_plan(getattr(self.fixture, user))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        plan = models.DeploymentPlan.objects.get(uuid=response.data['uuid'])
        self.assertEqual(1, plan.items.count())

    @data('global_support', 'admin', 'manager')
    def test_user_without_permissions_cannot_create_deployment_plan(self, user):
        response = self.create_deployment_plan(getattr(self.fixture, user))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)

    def create_deployment_plan(self, user):
        self.client.force_authenticate(user=user)
        return self.client.post(factories.DeploymentPlanFactory.get_list_url(), {
            'customer': structure_factories.CustomerFactory.get_url(self.fixture.customer),
            'name': 'Webapp for Monster Inc.',
            'items': [
                {
                    'preset': factories.PresetFactory.get_url(),
                    'quantity': 1
                }
            ]
        })


@ddt
class DeploymentPlanUpdateTest(test.APITransactionTestCase):

    def setUp(self):
        self.fixture = fixtures.CostPlanningFixture()
        self.plan = self.fixture.deployment_plan

        self.preset1 = factories.PresetFactory()
        self.plan.items.create(preset=self.preset1, quantity=1)
        self.preset2 = factories.PresetFactory()
        self.plan.items.create(preset=self.preset2, quantity=2)

        self.url = factories.DeploymentPlanFactory.get_url(self.plan)

    @data('staff', 'owner')
    def test_user_with_permissions_can_update_item_list(self, user):
        """
        Old item is removed, remaining item is updated.
        """
        self.client.force_authenticate(user=getattr(self.fixture, user))
        item = {
            'preset': factories.PresetFactory.get_url(self.preset1),
            'quantity': 2
        }

        response = self.client.patch(self.url, {'items': [item]})

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.plan.refresh_from_db()
        self.assertEqual(self.plan.items.count(), 1)
        self.assertEqual(self.plan.items.first().quantity, item['quantity'])

    @data('manager', 'admin', 'user')
    def test_user_without_permissions_cannot_update_plan(self, user):
        self.client.force_authenticate(user=getattr(self.fixture, user))
        response = self.client.put(self.url, {'name': 'New name for plan'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @data('staff', 'owner')
    def test_user_with_permissions_can_update_name(self, user):
        self.client.force_authenticate(user=getattr(self.fixture, user))

        response = self.client.put(self.url, {
            'name': 'New name for plan'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.plan.refresh_from_db()
        self.assertEqual(self.plan.name, 'New name for plan')


@ddt
class DeploymentPlanDeleteTest(test.APITransactionTestCase):

    def setUp(self):
        self.fixture = fixtures.CostPlanningFixture()
        self.plan = self.fixture.deployment_plan
        self.url = factories.DeploymentPlanFactory.get_url(self.plan)

    @data('staff', 'owner')
    def test_user_with_permissions_can_delete_plan(self, user):
        self.client.force_authenticate(getattr(self.fixture, user))

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.DeploymentPlan.objects.filter(pk=self.plan.pk).exists())

    @data('global_support')
    def test_user_without_permissions_cannot_delete_plan(self, user):
        self.client.force_authenticate(getattr(self.fixture, user))

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(models.DeploymentPlan.objects.filter(pk=self.plan.pk).exists())
