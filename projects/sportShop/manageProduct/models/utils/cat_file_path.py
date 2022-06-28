import os


def get_upload_path(instance, filename):

    if instance.parent:

        return os.path.join('stuff_cat',
                            instance.parent.title,
                            instance.title,
                            filename)

    return os.path.join('stuff_cat',
                        instance.title,
                        filename)
