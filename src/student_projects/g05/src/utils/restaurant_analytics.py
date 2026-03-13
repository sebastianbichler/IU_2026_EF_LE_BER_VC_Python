class RestaurantAnalytics:

    def __init__(self, restaurant):
        self.restaurant = restaurant

    def total_revenue(self):

        revenue = 0

        for order in self.restaurant.orders:
            revenue += order.bill.total

        return revenue

    def inventory_status(self):

        result = {}

        for item in self.restaurant.inventory:

            name = item.fish.name

            if name not in result:
                result[name] = 0

            result[name] += item.amount_kg

        return result

    def order_statistics(self):

        stats = {}

        for order in self.restaurant.orders:

            for item in order.items:

                name = item.menu_item.name

                if name not in stats:
                    stats[name] = 0

                stats[name] += item.quantity

        return stats