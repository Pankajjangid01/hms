from odoo import models

class ProductExcelUploadWizard(models.Model):
    _description = 'Product Excel Upload Wizard'
    _inherit = "product.template"

    def action_upload_excel(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Upload Data from Excel sheet',
            'res_model': 'product.template.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
