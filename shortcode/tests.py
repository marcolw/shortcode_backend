from django.test import TestCase, SimpleTestCase

from .utils import getRenderedText


class RenderTestCase(SimpleTestCase):
    def test_render_text_normal(self):
        product = {
            "Part_Number": "PN001",
            "sku": "SKU001",
            "name": "Name PN001, SKU001",
            "description": "Description PN001, SKU001",
            "name_SC": "Name #Part_Number;#, #sku;#",
            "description_SC": "Description #Part_Number#, #sku#",
        }
        self.assertEqual(product['name'], getRenderedText(
            product['name_SC'], product, None))
        self.assertEqual(product['description'], getRenderedText(
            product['description_SC'], product, None))

    def test_render_text_unit_measure(self):
        product = {
            "Part_Number": "PN001",
            "sku": "SKU001",
            "name": "Name 30kHz",
            "description": "Description 130 mm",
            "ULT_Frequency_xkHzx": "30",
            "Length_xmmx": "130",
            "name_SC": "Name #ULT_Frequency_xkHzx;UM#",
            "description_SC": "Description #Length_xmmx; UM#",
        }
        self.assertEqual(product['name'], getRenderedText(
            product['name_SC'], product, None))
        self.assertEqual(product['description'], getRenderedText(
            product['description_SC'], product, None))

    def test_render_text_unit_measure_label(self):
        product = {
            "Part_Number": "PN001",
            "sku": "SKU001",
            "name": "Name ULT Frequency (kHz): 30kHz",
            "description": "Description Length (mm): 130 mm",
            "ULT_Frequency_xkHzx": "30",
            "Length_xmmx": "130",
            "name_SC": "Name #ULT_Frequency_xkHzx;UM;!#",
            "description_SC": "Description #Length_xmmx; UM;!#",
        }
        self.assertEqual(product['name'], getRenderedText(
            product['name_SC'], product, None))
        self.assertEqual(product['description'], getRenderedText(
            product['description_SC'], product, None))

    def test_render_text_label(self):
        product = {
            "Part_Number": "PN001",
            "sku": "SKU001",
            "name": "Name Part Number: PN001",
            "description": "Description sku: SKU001",
            "name_SC": "Name #Part_Number;!;#",
            "description_SC": "Description #sku;!;#",
        }
        self.assertEqual(product['name'], getRenderedText(
            product['name_SC'], product, None))
        self.assertEqual(product['description'], getRenderedText(
            product['description_SC'], product, None))

    def test_render_text_with_commas(self):
        product = {
            "Part_Number": "PN001",
            "sku": "SKU001",
            "ex_data": "1,2, 3, data, with commas, 4",
            "name": "Name 1,2, 3, data, with commas, 4",
            "name_SC": "Name #ex_data;#",
        }
        self.assertEqual(product['name'], getRenderedText(
            product['name_SC'], product, None))

    def test_render_text_label_with_commas(self):
        product = {
            "Part_Number": "PN001",
            "sku": "SKU001",
            "ex_data_field": "1,2, 3, data, with commas, 4",
            "name": "Name ex data field: 1,2, 3, data, with commas, 4",
            "name_SC": "Name #ex_data_field;!;#",
        }
        self.assertEqual(product['name'], getRenderedText(
            product['name_SC'], product, None))

    def test_render_text_array(self):
        product = {
            "Part_Number": "PN001",
            "sku": "SKU001",
            "ex_data_field": "1,2, 3, data, with commas, 4",
            "name": "Name a, bb, c c c",
            "changed": ['a', 'bb', 'c c c'],
            "name_SC": "Name #changed;#",
        }
        self.assertEqual(product['name'], getRenderedText(
            product['name_SC'], product, None))

    def test_render_array_with_None(self):
        product = {
            "Part_Number": "PN001",
            "sku": "SKU001",
            "ex_data_field": "1,2, 3, data, with commas, 4",
            "name": "Name a, None, c c c",
            "changed": ['a', None, 'c c c'],
            "name_SC": "Name #changed;#",
        }
        #with self.assertRaises(TypeError):
        #    getRenderedText(product['name_SC'], product, None)
        self.assertEqual(product['name'], getRenderedText(
            product['name_SC'], product, None))