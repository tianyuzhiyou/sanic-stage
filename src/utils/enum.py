# -*- coding: utf-8 -*-
"""

使用说明：
    0.定义说明
        class Platform(Const):
            属性 = (值, 说明)
            属性 = {'value':值, 'label':说明}
            属性 = 说明 # 值 与 属性 相同的情况下(值与属性都定义为字符串)

    1.定义枚举类， 直接继承此文件的 Const 类即可， 如：

        # 属性 = (值, 说明)  的定义模式,且值是整形
        class Platform(Const):
            ios = (1, 'IOS')
            android = (2, 'ANDROID')
            wp = (3, 'WP')

        # 属性 = (值, 说明)  的定义模式,且值是字符串
        class LocationType(Const):
            asia = ('Asia', '亚洲')
            europe = ('Europe', '欧洲')
            america = ('America', '美洲')
            australia = ('Australia', '澳洲')

        # 属性 = {'value':值, 'label':说明}  的定义模式,值是整形或者字符串都允许
        class LocationType2(Const):
            asia = {'value':'Asia', 'label':'亚洲'}
            europe = {'value':'Europe', 'label':'欧洲'}
            america = {'value':'America', 'label':'美洲'}
            australia = {'value':'Australia', 'label':'澳洲'}

        # 属性 = 说明  的定义模式,且值跟属性一样
        class LocationType3(Const):
            asia = '亚洲'
            europe = '欧洲'
            america = '美洲'
            australia = '澳洲'


    2.在 model 中定义字段时， 可直接 new 枚举类， 如：

        from django.db import models
        class TestModel(models.Model):
            platform = models.PositiveSmallIntegerField('平台', choices=Platform(), db_index=True, default=Platform.android)
            location = models.CharField('用户所属地区', choices=LocationType(), max_length=20, blank=True, null=True)


    3.用来判断时， 直接点出枚举类对应的值即可：

        mo = TestModel()
        if mo.platform == Platform.android: print '这是安卓用户'


    4.获取对应的说明时， 用类的“get_FEILD_display”即可：

        mo = TestModel()
        plat_name = mo.get_platform_display()

        页面展示时：
        {{ object.get_platform_display }}


    5.获取对应的说明， 也可以由枚举类直接获取(用 _attrs, _values, _labels, _labels_to_values, _items 五个属性)：

        print( Platform.ios == 1 and Platform.android == 2 ) # 打印: True

        print( Platform._attrs[2] == 'ANDROID' ) # 打印: True
        print( Platform._attrs ) # 打印: {1: 'IOS', 2: 'ANDROID', 3: 'WP'}
        # 枚举类._attrs 返回 {值:说明}

        print( Platform._labels_to_values['ANDROID'] == 2 ) # 打印: True
        print( Platform._labels_to_values ) # 打印: {'ANDROID': 2, 'IOS': 1, 'WP': 3}
        # 枚举类._labels_to_values 返回 {说明:值} 。 与 _attrs 正好相反

        print( Platform._values['ios'] == 1 ) # 打印: True
        print( Platform._values ) # 打印: {'android': 2, 'ios': 1, 'wp': 3}
        # 枚举类._values 返回 {属性:值}

        print( Platform._labels['ios'] == 'IOS' ) # 打印: True
        print( Platform._labels ) # 打印: {'android': 'ANDROID', 'ios': 'IOS', 'wp': 'WP'}
        # 枚举类._labels 返回 {属性:说明}

        print( Platform() ) # 打印: [(1, 'IOS'), (2, 'ANDROID'), (3, 'WP')]
        print( Platform._items ) # 打印: [(1, 'IOS'), (2, 'ANDROID'), (3, 'WP')]
        # 枚举类._items 返回 [(值,说明), (值,说明)]

"""


class ConstType(type):
    def __new__(cls, name, bases, _attrs):
        values = {}  # {属性:值}
        labels = {}  # {属性:说明}
        attrs = {}  # {值:说明}
        labels_to_values = {}  # {说明:值}

        for k, v in list(_attrs.items()):
            if k.startswith('__'):
                continue
            if isinstance(v, (tuple, list)) and len(v) == 2:
                values[k] = v[0]
                labels[k] = v[1]
                attrs[v[0]] = v[1]
                labels_to_values[v[1]] = v[0]
            elif isinstance(v, dict) and 'label' in v and 'value' in v:
                values[k] = v['value']
                labels[k] = v['label']
                attrs[v['value']] = v['label']
                labels_to_values[v['label']] = v['value']
            elif isinstance(v, str):
                values[k] = k
                labels[k] = v
                attrs[k] = v
                labels_to_values[v] = k
            else:
                values[k] = v
                labels[k] = v

        obj = type.__new__(cls, name, bases, values)
        obj.values = values
        obj.labels = labels
        obj.labels_to_values = labels_to_values
        obj.attrs = attrs
        obj.items = sorted(list(attrs.items()), key=lambda k_v: k_v[0])
        return obj

    def __call__(cls, *args, **kw):
        return cls.items


class Const(metaclass=ConstType):
    ...

