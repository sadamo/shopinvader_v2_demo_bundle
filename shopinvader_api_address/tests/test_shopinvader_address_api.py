# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import json

from fastapi import status
from requests import Response

from odoo.tests.common import tagged

from odoo.addons.extendable_fastapi.tests.common import FastAPITransactionCase

from ..routers import address_router


@tagged("post_install", "-at_install")
class TestShopinvaderAddressApi(FastAPITransactionCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.env["res.users"].create(
            {
                "name": "Test User",
                "login": "test_user",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            cls.env.ref(
                                "shopinvader_api_address.shopinvader_address_user_group"
                            ).id
                        ],
                    )
                ],
            }
        )

        cls.test_partner = cls.env["res.partner"].create(
            {
                "name": "FastAPI Shopinvader Address Demo",
                "street": "rue test",
                "zip": "1410",
                "city": "Waterloo",
                "country_id": cls.env.ref("base.be").id,
                "title": cls.env.ref("base.res_partner_title_madam").id,
            }
        )

        cls.default_fastapi_authenticated_partner = cls.test_partner
        cls.default_fastapi_router = address_router

    def test_get_invoicing_address(self):
        """
        Test to get address of authenticated_partner
        """
        with self._create_test_client(router=address_router) as test_client:
            response: Response = test_client.get(
                "/addresses/invoicing",
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"error message: {response.text}",
        )

        response_json = response.json()
        self.assertTrue(response_json)

        address = response_json[0]

        self.assertEqual(address.get("name"), self.test_partner.name)
        self.assertEqual(address.get("street"), self.test_partner.street)
        self.assertEqual(address.get("zip"), self.test_partner.zip)
        self.assertEqual(address.get("city"), self.test_partner.city)
        self.assertEqual(address.get("country_id"), self.test_partner.country_id.id)
        self.assertEqual(address.get("id"), self.test_partner.id)
        self.assertEqual(address.get("title_id"), self.test_partner.title.id)

        with self._create_test_client(router=address_router) as test_client:
            response: Response = test_client.get(
                f"/addresses/invoicing/{self.test_partner.id}",
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"error message: {response.text}",
        )

        response_json = response.json()
        self.assertTrue(response_json)

        address = response_json

        self.assertEqual(address.get("name"), self.test_partner.name)
        self.assertEqual(address.get("street"), self.test_partner.street)
        self.assertEqual(address.get("zip"), self.test_partner.zip)
        self.assertEqual(address.get("city"), self.test_partner.city)
        self.assertEqual(address.get("country_id"), self.test_partner.country_id.id)
        self.assertEqual(address.get("id"), self.test_partner.id)
        self.assertEqual(address.get("title_id"), self.test_partner.title.id)

    def test_get_delivery_address(self):
        """
        Test to get delivery address of authenticated_partner
        """

        with self._create_test_client(router=address_router) as test_client:
            response: Response = test_client.get(
                "/addresses/delivery",
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"error message: {response.text}",
        )

        response_json = response.json()
        self.assertEqual(0, len(response_json))

        # add delivery address
        new_address = self.env["res.partner"].create(
            {
                "name": "test New Addr",
                "street": "test Street",
                "zip": "5000",
                "city": "Namur",
                "country_id": self.env.ref("base.be").id,
                "parent_id": self.test_partner.id,
                "type": "delivery",
            }
        )

        with self._create_test_client(router=address_router) as test_client:
            response: Response = test_client.get(
                "/addresses/delivery",
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"error message: {response.text}",
        )

        response_json = response.json()
        self.assertTrue(response_json)

        address = response_json[0]

        self.assertEqual(address.get("name"), new_address.name)
        self.assertEqual(address.get("street"), new_address.street)
        self.assertEqual(address.get("zip"), new_address.zip)
        self.assertEqual(address.get("city"), new_address.city)
        self.assertEqual(address.get("country_id"), new_address.country_id.id)
        self.assertEqual(address.get("id"), new_address.id)

        with self._create_test_client(router=address_router) as test_client:
            response: Response = test_client.get(
                f"/addresses/delivery/{new_address.id}",
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"error message: {response.text}",
        )

        response_json = response.json()

        address = response_json

        self.assertEqual(address.get("name"), new_address.name)
        self.assertEqual(address.get("street"), new_address.street)
        self.assertEqual(address.get("zip"), new_address.zip)
        self.assertEqual(address.get("city"), new_address.city)
        self.assertEqual(address.get("country_id"), new_address.country_id.id)
        self.assertEqual(address.get("id"), new_address.id)

    def test_update_invoicing_address(self):
        """
        Test to update invoicing address
        """
        data = {
            "name": "FastAPI Shopinvader Address Demo",
            "zip": "1410",
            "city": "Waterloo",
            "country_id": self.env.ref("base.be").id,
            "street": "test Street",
            "title_id": self.env.ref("base.res_partner_title_madam").id,
        }

        with self._create_test_client(router=address_router) as test_client:
            response: Response = test_client.post(
                f"/addresses/invoicing/{self.test_partner.id}", content=json.dumps(data)
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"error message: {response.text}",
        )
        response_json = response.json()
        self.assertTrue(response_json)

        address = response_json

        self.assertEqual(address.get("street"), "test Street")
        self.assertEqual(address.get("street"), self.test_partner.street)

    def test_update_invoicing_address_vat(self):
        """
        Test to update invoicing address vat
        """
        data = {
            "name": "FastAPI Shopinvader Address Demo",
            "zip": "1410",
            "city": "Waterloo",
            "country_id": self.env.ref("base.be").id,
            "street": "rue test",
            "vat": "BE0477472701",
        }

        with self._create_test_client(router=address_router) as test_client:
            response: Response = test_client.post(
                f"/addresses/invoicing/{self.test_partner.id}", content=json.dumps(data)
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"error message: {response.text}",
        )
        response_json = response.json()
        self.assertTrue(response_json)

        address = response_json

        self.assertEqual(address.get("vat"), "BE0477472701")
        self.assertEqual(address.get("vat"), self.test_partner.vat)

    def test_create_delivery_address(self):
        """
        Test to create delivery address
        """
        data = {
            "name": "test Addr",
            "street": "test Street",
            "zip": "5000",
            "city": "Namur",
            "country_id": self.env.ref("base.be").id,
        }

        with self._create_test_client(router=address_router) as test_client:
            response: Response = test_client.post(
                "/addresses/delivery", content=json.dumps(data)
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg=f"error message: {response.text}",
        )
        response_json = response.json()
        self.assertTrue(response_json)

        address = response_json

        self.assertEqual(address.get("street"), "test Street")
        self.assertNotEqual(address.get("street"), self.test_partner.street)

        address_odoo = self.env["res.partner"].browse(address.get("id"))
        self.assertEqual(address_odoo.type, "delivery")

    def test_delete_delivery_address(self):
        """
        Test to delete delivery address
        """

        new_address = self.env["res.partner"].create(
            {
                "name": "test New Addr",
                "street": "test Street",
                "zip": "5000",
                "city": "Namur",
                "country_id": self.env.ref("base.be").id,
                "parent_id": self.test_partner.id,
                "type": "delivery",
            }
        )

        with self._create_test_client(router=address_router) as test_client:
            response: Response = test_client.delete(
                f"/addresses/delivery/{new_address.id}",
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"error message: {response.text}",
        )
        self.assertFalse(new_address.active)

    def test_update_delivery_address(self):
        """
        Test to update delivery address
        """
        new_address = self.env["res.partner"].create(
            {
                "name": "test New Addr",
                "street": "test Street",
                "zip": "5000",
                "city": "Namur",
                "country_id": self.env.ref("base.be").id,
                "parent_id": self.test_partner.id,
                "type": "delivery",
            }
        )

        data = {
            "name": "test Addr2",
            "street": "test Street2",
            "zip": "5000",
            "city": "Namur",
            "country_id": self.env.ref("base.be").id,
        }

        with self._create_test_client(router=address_router) as test_client:
            response: Response = test_client.post(
                f"/addresses/delivery/{new_address.id}", content=json.dumps(data)
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"error message: {response.text}",
        )
        self.assertEqual(new_address.name, data.get("name"))
        self.assertEqual(new_address.street, data.get("street"))
