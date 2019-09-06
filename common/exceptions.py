class NotFound(Exception):
    def __init__(self):
        super(NotFound, self).__init__()


class NodeNotFound(NotFound):
    def __init__(self, uid):
        super(NodeNotFound, self).__init__()
        self.message = "Couldn't found a node with uuid={}.".format(uid)


class MLDataNotFound(NotFound):
    def __init__(self, uid):
        super(MLDataNotFound, self).__init__()
        self.message = "Couldn't found a MLData with uuid={}.".format(uid)


class ResourceNotFound(NotFound):
    def __init__(self, uid):
        super(ResourceNotFound, self).__init__()
        self.message = "Couldn't found a resource with uuid={}.".format(uid)
