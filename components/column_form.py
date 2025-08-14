import streamlit as st
from models.column import Column

def render_column_form(column: Column, table) -> bool:
	delete_key = f"delete_col_btn_{table.table_id}_{column.column_id}"
	edit_key = f"edit_col_btn_{table.table_id}_{column.column_id}"

	old_column_values = {
		"name" : column.name,
		"data_type" : column.data_type,
		"length" : column.length,
		"default_value" : column.default_value,
		"nullable" : column.nullable
	}

	col1, col2, col3, col4, col5, col6 = st.columns([5, 4, 3, 2, 2, 2])
	with col1:
		input_name = st.text_input("Kolumnnamn", value=column.name, key=f"name_{edit_key}")

		if st.session_state.get("editing_index") == edit_key:
			if st.button("Spara kolumn", key=f"save_col_{edit_key}"):
				if not input_name.strip():
					st.error("Kolumnnamn får inte vara tomt.")
					return False
				st.session_state.editing_index = None
				st.rerun()

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
			st.session_state.editing_index = None
			st.rerun()	
	
		if (
			input_name != old_column_values["name"] or
			input_data_type != old_column_values["data_type"] or
			input_length != old_column_values["length"] or
			input_default_value != old_column_values["default_value"] or
			input_nullable != old_column_values["nullable"]
		):
			st.session_state.editing_index = edit_key

		if old_column_values["name"].strip() == "" and input_name.strip() != "":
			st.session_state.editing_index = edit_key

		column.name = input_name
		column.length = input_length
		column.default_value = input_default_value
		column.nullable = input_nullable
		column.data_type = input_data_type

		if column.column_type == "Dimension" and input_name.strip():
			if not input_name.startswith("D_"):
				column.name = f"D_{input_name}"
			base_name = column.name.replace("D_", "").replace("_ID", "")
			column.references_schema = st.session_state.get("schema", "")
			column.references_table = "D_Datum" if column.name.startswith("D_Datum") else base_name
			column.references_column = "D_Datum_ID" if column.name.startswith("D_Datum") else f"{base_name}_ID"
			column.is_foreign_key = True

		return False
