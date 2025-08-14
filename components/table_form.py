import streamlit as st
from components.column_form import render_column_form
from utils.sql_generator import generate_sql
from models.column import Column

def render_table_metadata_form(table):
	old_name = table.table_name
	col1, col2 = st.columns([1, 2])
	with col1:
		schema = st.text_input("Schema", value=table.schema_name, key=f"schema_{table.table_id}")
	with col2:
		table_name = st.text_input("Tabellnamn", value=table.table_name, key=f"table_name_{table.table_id}")

	if schema != table.schema_name or table_name != table.table_name:
		table.schema_name = schema
		table.table_name = table_name
		table.update_static_column_names()
		st.session_state.metadata_updated = True
		st.rerun()

	if table.table_name != old_name:
		table.update_static_column_names()

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

	indexed_columns = list(enumerate(table.get_sorted_columns()))

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
			table.columns.append(Column(
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
				column_type=col_type
			))
			st.rerun()

def render_sql_preview(table):
	if any(not col.name.strip() for col in table.columns):
		st.error(f"Tabellen '{table.table_name}' innehåller kolumn(er) utan namn.")
		return
	create_sql, alter_sql = generate_sql(table)
	st.code(create_sql, language="sql")
	if alter_sql.strip():
		st.code(alter_sql, language="sql")
