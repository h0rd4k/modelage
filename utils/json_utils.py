import streamlit as st
import json
from models.table import Table

def import_model(file):
	if not file:
		return None, "Ingen fil vald."

	try:
		data = json.load(file)
		for t_type in ["Fakta", "Dimension", "Lookup"]:
			st.session_state.tables[t_type] = [
				Table.from_dict(tbl) for tbl in data.get(t_type, [])
			]
		st.session_state.selected_type = "Fakta"
		st.session_state.editing_index = None
		st.session_state.json_imported = True
		return True, None
	except Exception as e:
		return False, f"Fel vid läsning: {e}"

def export_model(filename):
	if not filename.endswith(".json"):
		filename += ".json"

	all_tables = {
		t_type: [table.to_dict() for table in st.session_state.tables[t_type]]
		for t_type in ["Fakta", "Dimension", "Lookup"]
	}
	json_data = json.dumps(all_tables, indent=2, ensure_ascii=False)
	return filename, json_data
