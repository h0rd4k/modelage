import streamlit as st
from components.column_form import render_column_form
from utils.sql_generator import generate_sql
from models.column import Column

def render_table_metadata_form(table):
	edit_key = f"edit_table{table.table_id}"
	save_key = f"save_table_btn_{edit_key}"

	if save_key not in st.session_state:
		st.session_state[save_key] = False

	col1, col2 = st.columns([1, 2])
	with col1:
		input_schema_name = st.text_input("Schema", value=table.schema_name, key=f"schema__name_{edit_key}")
	with col2:
		input_table_name = st.text_input("Tabellnamn", value=table.table_name, key=f"table_name_{edit_key}")

	has_changed = (
		input_schema_name != table.schema_name or
		input_table_name != table.table_name
	)
	st.session_state[save_key] = has_changed

	if st.session_state[save_key]:
		if st.button("Spara", key=f"save_btn_{edit_key}"):
			table.schema_name = input_schema_name
			table.table_name = input_table_name
			table.update_static_column_names()
			st.session_state[save_key] = False
			#st.rerun()

def render_table_columns_editor(table):
	st.markdown("#### Kolumner")
	if st.session_state.get("pending_column_delete"):
		tbl_id, col_id = st.session_state.pending_column_delete
		if tbl_id == table.table_id:
			for i, col in enumerate(table.columns):
				if col.column_id == col_id:
					table.remove_column(i)
					break
			st.session_state.pending_column_delete = None
			st.rerun()

	for col_type in ["Statisk", "Dimension", "Information"]:
		if col_type == "Dimension" and table.table_type != "Fakta":
			continue
		if col_type == "Statisk" and table.table_type == "Lookup":
			continue

		st.markdown(f"### {col_type}")

		sorted_cols = table.get_sorted_columns()
		saved_cols = [col for col in sorted_cols if col.column_type == col_type and col.name.strip()]
		new_cols = [col for col in table.columns if col.column_type == col_type and not col.name.strip()]

		for cols in saved_cols:
			render_column_form(cols, table)

		for cols in new_cols:
			render_column_form(cols, table)

		if st.button(f"Ny kolumn", key=f"add_{col_type}_{table.table_id}"):
			table.columns.append(table.add_empty_column(col_type))
			st.rerun()

def render_sql_preview(table):
	if any(not col.name.strip() for col in table.columns):
		st.error(f"Tabellen '{table.table_name}' innehåller kolumn(er) utan namn.")
		return
	create_sql, alter_sql = generate_sql(table)
	st.code(create_sql, language="sql")
	if alter_sql.strip():
		st.code(alter_sql, language="sql")
