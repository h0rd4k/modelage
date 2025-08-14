def generate_sql(table):
	full_table = f"[{table.schema_name}].[{table.table_name}]"
	create_sql = f"CREATE TABLE {full_table} (\n"
	column_lines = []
	pk_columns = []

	valid_columns = [col for col in table.get_sorted_columns() if col.name.strip()]

	for col in valid_columns:
		length = f"({col.length})" if col.length and col.data_type.upper() in ["NVARCHAR", "VARBINARY", "DECIMAL"] else ""
		datatype = f"{col.data_type}{length}"
		line = f"  [{col.name}] {datatype}"

		if col.default_value:
			df_name = f"DF_{table.schema_name}_{table.table_name}_{col.name.replace(table.table_name + '_', '')}"
			line += f" CONSTRAINT [{df_name}] DEFAULT {col.default_value}"

		line += f" {col.nullable}"

		if col.is_identity:
			line += " IDENTITY(1,1)"

		column_lines.append(line)

		if col.is_primary_key:
			pk_columns.append(f"[{col.name}]")

	create_sql += "\n  ,".join(column_lines)

	if pk_columns:
		pk_name = f"PK_{table.schema_name}_{table.table_name}"
		create_sql += f"\n  ,  CONSTRAINT [{pk_name}] PRIMARY KEY ({', '.join(pk_columns)})"

	create_sql += "\n);"

	alter_sql = ""
	for col in valid_columns:
		if col.is_foreign_key and col.references_table and col.references_column:
			ref_table = f"[{col.references_table}]"
			ref_column = f"[{col.references_column}]"
			if col.references_schema:
				ref_table = f"[{col.references_schema}].{ref_table}"
			fk_name = f"FK_{table.schema_name}_{table.table_name}_{col.name.replace(table.table_name + '_', '')}"
			alter_sql += f"ALTER TABLE {full_table} WITH CHECK ADD CONSTRAINT [{fk_name}] FOREIGN KEY ([{col.name}]) REFERENCES {ref_table} ({ref_column});\n"

	return create_sql, alter_sql
