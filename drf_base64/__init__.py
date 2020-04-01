from drf_yasg.inspectors import SwaggerAutoSchema

from .inspectors import NamedBase64FieldInspector

if NamedBase64FieldInspector not in SwaggerAutoSchema.field_inspectors:
    SwaggerAutoSchema.field_inspectors = [NamedBase64FieldInspector] + SwaggerAutoSchema.field_inspectors
