from .resource import Resource


class Products(Resource):
    def list(self, filter_groups=None, sort_orders=None, current_page=1, page_size=1):
        search_criteria = {
            "searchCriteria": {
                "currentPage": current_page,
                "pageSize": page_size,
                #"filterGroups": filter_groups,
                #"sortOrders": sort_orders
            }}
        print(search_criteria)
        return self.client.execute("GET", "/products", search_criteria)

    def get(self, sku):
        return self.client.execute("GET", "/products/%s" % sku)

    def create(self, data):
        return self.client.execute("POST", "/products", data)
