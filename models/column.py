import uuid

class Column:
	data_types = [
		"INT", "BIGINT", "SMALLINT", "TINYINT",
		"DECIMAL", "FLOAT", "BIT",
		"NVARCHAR", "VARBINARY",
		"DATE", "DATETIME", "TIME"
	]
	column_types = ["Statisk", "Dimension", "Information"]

	def __init__(self, name="", data_type="INT", length="", default_value="", nullable="NULL",
		is_primary_key=False, is_foreign_key=False, is_identity=False,
		references_table=None, references_column=None, references_schema=None, role_name=None,
		column_type="Information", column_id=None, template_name=None, sort_order=None):
			self.name = name
			self.template_name = template_name or name
			self.data_type = data_type
			self.length = length
			self.default_value = default_value
			self.nullable = nullable
			self.is_primary_key = is_primary_key
			self.is_foreign_key = is_foreign_key
			self.is_identity = is_identity
			self.references_table = references_table
			self.references_column = references_column
			self.references_schema = references_schema
			self.role_name = role_name
			self.column_type = column_type
			self.column_id = column_id or str(uuid.uuid4())
			self.sort_order = sort_order

	def to_dict(self):
		return {
			"name": self.name,
			"template_name": self.template_name,
			"data_type": self.data_type,
			"length": self.length,
			"default_value": self.default_value,
			"nullable": self.nullable,
			"is_primary_key": self.is_primary_key,
			"is_foreign_key": self.is_foreign_key,
			"is_identity": self.is_identity,
			"references_table": self.references_table,
			"references_column": self.references_column,
			"references_schema": self.references_schema,
			"role_name": self.role_name,
			"column_type": self.column_type,
			"column_id": self.column_id,
			"sort_order": self.sort_order
		}

	@staticmethod
	def from_dict(data):
		return Column(
			name=data.get("name", ""),
			template_name=data.get("template_name", data.get("name", "")),
			data_type=data.get("data_type", "INT"),
			length=data.get("length", ""),
			default_value=data.get("default_value", ""),
			nullable=data.get("nullable", "NULL"),
			is_primary_key=data.get("is_primary_key", False),
			is_foreign_key=data.get("is_foreign_key", False),
			is_identity=data.get("is_identity", False),
			references_table=data.get("references_table", None),
			references_column=data.get("references_column", None),
			references_schema=data.get("references_schema", None),
			role_name=data.get("role_name", None),
			column_type=data.get("column_type", "Information"),
			column_id=data.get("column_id", str(uuid.uuid4())),
			sort_order=data.get("sort_order", None)
	)
