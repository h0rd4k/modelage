def get_prefix(table_type):
	return {
		"Fakta": "F_",
		"Dimension": "D_",
		"Lookup": "L_"
	}.get(table_type, "")

def check_table_name_prefix(name: str, prefix: str) -> str:
	if not name.startswith(prefix):
		return f"{prefix}{name}"
	return name
