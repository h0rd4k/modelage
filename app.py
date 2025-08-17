import streamlit as st
from state.session import init_session_state
from components.sidebar import render_sidebar
from components.create_table import render_create_table_form
from components.table_card import render_table_card

st.set_page_config(
	page_title="ModelAge",
	layout="wide"
)

init_session_state()

if st.session_state.get("pending_table_delete"):
	table_id = st.session_state.pending_table_delete
	selected_type = st.session_state.selected_type
	st.session_state.tables[selected_type] = [
		t for t in st.session_state.tables[selected_type]
		if t.table_id != table_id
	]
	st.session_state.pending_table_delete = None
	st.rerun()

if st.session_state.get("pending_column_delete"):
	table_id, column_id = st.session_state.pending_column_delete
	for t_type in ["Fakta", "Dimension", "Lookup"]:
		for table in st.session_state.tables[t_type]:
			if table.table_id == table_id:
				table.columns = [col for col in table.columns if col.column_id != column_id]
				break
	st.session_state.pending_column_delete = None
	st.rerun()

render_sidebar()

selected_type = st.session_state.selected_type
tables = st.session_state.tables[selected_type]

st.markdown(f"## {selected_type}")

render_create_table_form(selected_type)

for table in tables:
	render_table_card(table, selected_type)
