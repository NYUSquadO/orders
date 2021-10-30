# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import OrderItem, Order

class OrderItemFactory(factory.Factory):
    """Creates fake orderitems that you don't have to feed"""

    class Meta:
        """Meta data model for OrderItem"""
        model = OrderItem

    id = factory.Sequence(lambda n: n)
    # order_id = FuzzyChoice(choices = [1,2,3,4,5,6,7,8,9,10])
    item_id = FuzzyChoice(choices = [11,22, 33, 44, 55])
    item_name = FuzzyChoice(choices=["iphone13", "ipad", "Macbook", "ipods"])
    item_qty = FuzzyChoice(choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    item_price = FuzzyChoice(choices=[9999.0, 888.0, 66.0, 5.0])


class OrderFactory(factory.Factory):
    """Creates fake orders that you don't have to feed"""

    class Meta:
        """Meta data model for Order"""
        model = Order

    id = factory.Sequence(lambda n: n)
    cust_id = FuzzyChoice(choices = [101, 102, 103, 104])
    order_items = [OrderItemFactory()]
    status = FuzzyChoice(choices = ["Cancelled", "Placed"])