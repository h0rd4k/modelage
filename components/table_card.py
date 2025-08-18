import streamlit as st
from components.table_form import (
	render_table_metadata_form,
	render_table_columns_editor,
	render_sql_preview
)

def render_table_card(table, selected_type):
	label = f"[{table.schema_name}].[{table.table_name}]"
	with st.expander(label, expanded=False):
		tab1, tab2, tab3 = st.tabs(["Tabell", "Kolumner", "Kod"])

		with tab1:
			st.markdown(f"### Tabell: {label}")
			col1, col2 = st.columns([1, 1])
			with col1:
				if st.button("Radera tabell", key=f"delete_table_{table.table_id}"):
					st.session_state.pending_table_delete = table.table_id
					st.rerun()

			render_table_metadata_form(table)

			st.markdown("#### Översikt")
			st.markdown(f"- **Antal kolumner:** `{len(table.columns)}`")

			if table.columns:
				st.markdown("##### Kolumner")
				data = []
				columns_to_show = table.get_sorted_columns()
				for col in columns_to_show:
					data.append({
						"Kolumnnamn": col.name,
						"Datatyp": col.data_type,
						"Längd/Precision": col.length,
						"Standardvärde": col.default_value,
						"Tillåter NULL": "Ja" if col.nullable == "NULL" else "Nej",
						"Kolumntyp": col.column_type
					})
				st.table(data)

		if table.table_type == "Fakta":
			st.markdown("##### Dimensioner")
			dimension_links = []
			for col in table.columns:
				if col.column_type == "Dimension" and hasattr(col, "is_foreign_key") and col.is_foreign_key:
					dimension_links.append({
						"Nyckelkolumn": col.name,
						"Dimensionstabell": f"[{col.references_schema}].[{col.references_table}]",
						"Referenskolumn": col.references_column,
						"Datatyp": col.data_type
					})

			if dimension_links:
				st.table(dimension_links)
			else:
				st.info("Inga kopplade dimensionstabeller hittades.")

		with tab2:
			render_table_columns_editor(table)

		with tab3:
			st.markdown("### SQL-preview")
			render_sql_preview(table)
