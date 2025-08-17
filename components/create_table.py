import streamlit as st
from models.table import Table
from utils.helpers import get_prefix, apply_prefix_and_capitalize

def render_create_table_form(selected_type):
	prefix = get_prefix(selected_type)
	with st.expander("Skapa ny tabell", expanded=False):
		with st.form("create_table_form"):
			col1, col2 = st.columns([1, 2])
			with col1:
				schema = st.text_input("Schema")
			with col2:
				name = st.text_input("Tabellnamn")
			submitted = st.form_submit_button("Skapa tabell")

		if submitted and schema and name:
			name = apply_prefix_and_capitalize(name, prefix)
			new_table = Table(schema_name=schema, table_name=name, table_type=selected_type)

			if selected_type in ["Fakta", "Dimension"]:
				new_table.add_static_table_columns()

			st.session_state.tables[selected_type].append(new_table)
			st.success("Tabell skapad!")
