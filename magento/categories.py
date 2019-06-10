from magento.resource import Resource


class Categories(Resource):

    def get(self, category_id):
        return self.client.execute("GET", "categories/%s" % category_id)

    def list(self, root_category_id=None, depth=None):
        parameter = {}
        if root_category_id:
            parameter["rootCategoryId"] = root_category_id
        if depth:
            parameter["depth"] = depth

        return self.client.execute("GET", "/categories", parameter)

    def create(self, data):
        return self.client.execute("POST", "/categories", data)
