import streamlit as st
from utils.json_utils import import_model, export_model

def render_sidebar():
	with st.sidebar:
		st.markdown("## Tabelltyper")
		for table_type in ["Fakta", "Dimension", "Lookup", "Stage"]:
			if st.button(table_type, width=100):
				st.session_state.selected_type = table_type
				st.session_state.editing_index = None

		st.markdown("---")
		st.markdown("## Modellhantering")

		import_file = st.file_uploader("Öppna modell", type="json")
		if import_file and not st.session_state.get("json_imported", False):
			success, error = import_model(import_file)
			if success:
				st.rerun()
			elif error:
				st.error(error)

		export_file = st.text_input("Exportera modell", value="modell.json")
		export_filename, export_data = export_model(export_file)
		st.download_button(
			label="Exportera modell",
			data=export_data,
			file_name=export_filename,
			mime="application/json"
		)
