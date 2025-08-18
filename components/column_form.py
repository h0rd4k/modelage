import streamlit as st
from models.column import Column
from utils.helpers import capitalize_first

def render_column_form(column: Column, table) -> bool:
	edit_key = f"edit_col{table.table_id}_{column.column_id}"
	delete_key = f"delete_col_btn_{table.table_id}_{column.column_id}"
	save_key = f"save_col_btn_{edit_key}"

	if save_key not in st.session_state:
		st.session_state[save_key] = False

	old_column_values = {
		"name": column.name,
		"data_type": column.data_type,
		"length": column.length,
		"default_value": column.default_value,
		"nullable": column.nullable,
		"references_schema": column.references_schema,
		"references_table": column.references_table,
		"references_column": column.references_column,
		"role_name": column.role_name
	}

	col1, col2, col3, col4, col5, col6 = st.columns([5, 4, 3, 2, 2, 2])
	with col1:
		if column.column_type == "Dimension":
			dimension_tables = st.session_state.tables.get("Dimension", [])
			dimension_options = [
				f"[{tbl.schema_name}].[{tbl.table_name}]"
				for tbl in dimension_tables
			]

			if not dimension_options:
				st.error("Inga dimensionstabeller har skapats ännu, vilket krävs för att kunna lägga till en dimensionskolumn.")
				return False
			current_ref = f"[{column.references_schema}].[{column.references_table}]" if column.references_schema and column.references_table else dimension_options[0]

			selected_ref = st.selectbox(
				"Välj dimensionstabell",
				options=dimension_options,
				index=dimension_options.index(current_ref) if current_ref in dimension_options else 0,
				key=f"ref_table_{edit_key}"
			)

			selected_schema, selected_table = selected_ref.strip("[]").split("].[")
			column.references_schema = selected_schema
			column.references_table = selected_table
			column.references_column = f"{selected_table}_ID"
			column.is_foreign_key = True

			role_input = st.text_input("Rollspelande namn (valfritt)", value=column.role_name or "", key=f"role_name_{edit_key}")
			column.role_name = role_input.strip() if role_input else None

			base_column_name = f"{selected_table}_ID"
			role_playing = capitalize_first(column.role_name) if column.role_name else ""
			column.name = f"{base_column_name}_{role_playing}" if role_playing else base_column_name
		else:
			input_column_name = st.text_input("Kolumnnamn", value=column.name, key=f"name_{edit_key}")

	with col2:
		input_data_type = st.selectbox("Datatyp", Column.data_types, index=Column.data_types.index(column.data_type) if column.data_type in Column.data_types else 0, key=f"data_type_{edit_key}")
	with col3:
		input_length = st.text_input("Längd/Precision", value=column.length, key=f"length_{edit_key}")
	with col4:
		input_default_value = st.text_input("Standardvärde", value=column.default_value, key=f"default_value_{edit_key}")
	with col5:
		input_nullable = st.selectbox("Tillåt NULL", ["NULL", "NOT NULL"], index=["NULL", "NOT NULL"].index(column.nullable), key=f"nullable_{edit_key}")
	with col6:
		if st.button("Radera", key=delete_key):
			st.session_state.pending_column_delete = (table.table_id, column.column_id)
			st.session_state[save_key] = False
			st.rerun()

	has_changed = (
		input_data_type != old_column_values["data_type"] or
		input_length != old_column_values["length"] or
		input_default_value != old_column_values["default_value"] or
		input_nullable != old_column_values["nullable"]
	)

	if column.column_type == "Dimension":
		has_changed = has_changed or (
			column.references_schema != old_column_values["references_schema"] or
			column.references_table != old_column_values["references_table"] or
			column.references_column != old_column_values["references_column"] or
			column.role_name != old_column_values["role_name"] or
			column.name != old_column_values["name"]
		)
	else:
		has_changed = has_changed or input_column_name != old_column_values["name"]

	st.session_state[save_key] = has_changed

	if st.session_state[save_key]:
		if st.button("Spara", key=f"save_col_{edit_key}"):
			if column.column_type != "Dimension" and not input_column_name.strip():
				st.error("Kolumnnamn får inte vara tomt.")
				return False

			if column.column_type != "Dimension":
				column.name = input_column_name
				column.name = capitalize_first(input_column_name)

			column.data_type = input_data_type
			column.length = input_length
			column.default_value = input_default_value
			column.nullable = input_nullable

			st.session_state[save_key] = False
			st.rerun()

	return False
