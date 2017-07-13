from .models import Information

def int_information():
    #延迟加载，需要用list进行强制求值
    infos = list(Information.objects.all())
    infos_type=dict()
    for info in infos:
        print(type(info))
        infotype = info.infotype
        keys = [int(key) for key in infos_type.keys()]
        if infotype not in keys:
            infos_type['%s'%infotype] = list()
            print(info.id)
        infos_type['%s'%infotype].append(info)
    print(infos_type)
    return infos_type
