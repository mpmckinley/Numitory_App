def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "%s/%s.%s" % (instance.item_name, instance.item_name, extension)
    # ItemModel = instance.__class__
    # new_id = ItemModel.objects.order_by("instance.item_name").last().id
    #
    # return "%s" % filename
