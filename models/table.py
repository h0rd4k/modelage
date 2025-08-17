import uuid
from models.column import Column
from config.static_columns import STATIC_TABLE_COLUMNS

class Table:
	def __init__(self, schema_name="", table_name="", table_type="Fakta", table_id=None):
		self.schema_name = schema_name
		self.table_name = table_name
		self.table_type = table_type
		self.table_id = table_id or str(uuid.uuid4())
		self.columns = []

	def add_static_table_columns(self):
		column_defs = STATIC_TABLE_COLUMNS.get(self.table_type, [])
		for col_def in column_defs:
			template_name = col_def["name"]
			name = template_name.replace("{table_name}", self.table_name)

			self.columns.append(Column(
				name=name,
				template_name=template_name,
				data_type=col_def.get("data_type", "INT"),
				length=col_def.get("length", ""),
				default_value=col_def.get("default_value", ""),
				nullable=col_def.get("nullable", "NULL"),
				is_primary_key=col_def.get("is_primary_key", False),
				is_foreign_key=col_def.get("is_foreign_key", False),
				is_identity=col_def.get("is_identity", False),
				column_type=col_def.get("column_type", "Information")
			))

	def update_static_column_names(self):
		for col in self.columns:
			if col.column_type == "Statisk" and hasattr(col, "template_name"):
				col.name = col.template_name.replace("{table_name}", self.table_name)

	def add_empty_column(self, column_type):
		return Column(
			name="",
			data_type="INT",
			length="",
			default_value="",
			nullable="NULL",
			is_primary_key=False,
			is_foreign_key=False,
			is_identity=False,
			references_table=None,
			references_column=None,
			references_schema=None,
			column_type=column_type
		)

	def remove_column(self, index):
		if 0 <= index < len(self.columns):
			del self.columns[index]

	def get_sorted_columns(self):
		static_columns = {
			col.name for col in self.columns
			if col.column_type == "Statisk"
				and hasattr(col, "template_name")
				and "{table_name}" not in col.template_name
		}
		def sort_key(col):
			name = col.name.lower()
			if col.column_type == "Statisk" and hasattr(col, "template_name") and "{table_name}" in col.template_name:
					return (0, name)
			
			if col.column_type in ["Dimension", "Information"]:
					return (1, name)
			
			if col.column_type == "Statisk":
				if not hasattr(col, "template_name") or name not in static_columns:
					return (2, name)
				else:
					return (3, name)
			
			return (4, name)
		return sorted(self.columns, key=sort_key)

	def to_dict(self):
		return {
			"schema_name": self.schema_name,
			"table_name": self.table_name,
			"table_type": self.table_type,
			"table_id": self.table_id,
			"columns": [col.to_dict() for col in self.columns]
		}

	@staticmethod
	def from_dict(data):
		table = Table(
			schema_name=data.get("schema_name", ""),
			table_name=data.get("table_name", ""),
			table_type=data.get("table_type", "Fakta"),
			table_id=data.get("table_id")
		)
		for col_data in data.get("columns", []):
			table.columns.append(Column.from_dict(col_data))
		table.update_static_column_names()
		return table
