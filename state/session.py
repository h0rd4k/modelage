import streamlit as st

def init_session_state():
	defaults = {
		"tables": {
			"Fakta": [],
			"Dimension": [],
			"Lookup": []
		},
		"selected_type": "Fakta",
		"editing_index": None,
		"json_imported": False,
		"pending_table_delete": None,
		"pending_column_delete": None,
		"column_added": False
	}
	for key, value in defaults.items():
		if key not in st.session_state:
			st.session_state[key] = value
