import base64
import io
import xlsxwriter
import tempfile
from PIL import Image
from odoo import models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def action_export_selected_products_excel(self):
        """method to generate the excel sheet and write data in the excel sheet"""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Product Data")

        worksheet.write('A1','Product Name')
        worksheet.write('B1','Price List')
        worksheet.write('C1','Internal Reference')
        worksheet.write('D1','Image')
        worksheet.set_column('A:A',30)
        worksheet.set_column('B:B',15)
        worksheet.set_column('C:C',20)
        worksheet.set_column('D:D',35)

        row = 1
        for product in self:
            worksheet.write(row,0,product.name or '')
            worksheet.write(row,1,product.list_price or 0.0)
            worksheet.write(row,2,product.default_code or '')

            if product.image_1920:
                try:
                    temp_image = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                    image_data = base64.b64decode(product.image_1920)
                    img = Image.open(io.BytesIO(image_data))
                    img.save(temp_image.name, format='PNG')
                    worksheet.set_row(row, 80)
                    worksheet.insert_image(row, 3, temp_image.name, {
                        'x_offset': 0,
                        'y_offset': 0,
                        'x_scale': 0.2,
                        'y_scale': 0.2,
                    })
                except Exception:
                    pass
            row += 1

        workbook.close()
        output.seek(0)

        attachment = self.env['ir.attachment'].create({
            'name': 'product_export.xlsx',
            'res_id': self.ids[0] if self else False,
            'res_model': 'product.template',
            'datas': base64.b64encode(output.read()),
            'type': 'binary',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
            }