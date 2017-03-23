""" Defines how to optimize DigitalOcean droplets sizes """
import collections

from rest_framework import serializers as rf_serializers

from nodeconductor_digitalocean import apps as do_apps, models as do_models, serializers as do_serializers

from .. import optimizers, register, serializers


OptimizedPreset = collections.namedtuple('OptimizedPreset', ('preset', 'size', 'quantity', 'price'))

OptimizedDigitalOcean = optimizers.namedtuple_with_defaults(
    'OptimizedDigitalOcean',
    field_names=optimizers.OptimizedService._fields + ('optimized_presets',),
    default_values=optimizers.OptimizedService._defaults,
)


class DigitalOceanOptimizer(optimizers.Optimizer):
    """ Find the cheapest Digital Ocean size for each preset """
    HOURS_IN_DAY = 24

    def optimize(self, deployment_plan, service):
        optimized_presets = []
        price = 0
        for item in deployment_plan.items.all():
            preset = item.preset
            try:
                size = do_models.Size.objects.filter(
                    cores__gte=preset.cores, ram__gte=preset.ram, disk__gte=preset.storage).order_by('price')[0]
            except IndexError:
                preset_as_str = '%s (cores: %s, ram %s MB, storage %s MB)' % (
                    preset.name, preset.cores, preset.ram, preset.storage)
                raise optimizers.OptimizationError(
                    'It is impossible to create a droplet for preset %s. It is too big.' % preset_as_str)
            optimized_presets.append(OptimizedPreset(
                preset=preset,
                size=size,
                quantity=item.quantity,
                price=size.price * item.quantity * self.HOURS_IN_DAY,
            ))
            price += size.price * item.quantity * self.HOURS_IN_DAY
        return OptimizedDigitalOcean(price=price, service=service, optimized_presets=optimized_presets)


register.Register.register_optimizer(do_apps.DigitalOceanConfig.service_name, DigitalOceanOptimizer)


class OptimizedPresetSerializer(rf_serializers.Serializer):
    size = do_serializers.SizeSerializer()
    preset = serializers.PresetSerializer()
    quantity = rf_serializers.IntegerField()
    price = rf_serializers.DecimalField(max_digits=22, decimal_places=10)


class OptimizedDigitalOceanSerializer(serializers.OptimizedServiceSerializer):
    service = rf_serializers.HyperlinkedRelatedField(
        view_name='digitalocean-detail',
        lookup_field='uuid',
        read_only=True,
    )
    optimized_presets = OptimizedPresetSerializer(many=True)


register.Register.register_serializer(do_apps.DigitalOceanConfig.service_name, OptimizedDigitalOceanSerializer)
