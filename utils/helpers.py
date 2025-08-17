def get_prefix(table_type):
	return {
		"Fakta": "F_",
		"Dimension": "D_",
		"Lookup": "L_"
	}.get(table_type, "")

def apply_prefix_and_capitalize(name: str, prefix: str) -> str:
	if not name.startswith(prefix):
		name = f"{prefix}{name}"
	if name.startswith(prefix):
		actual_name = name[len(prefix):]
		name = f"{prefix}{actual_name.capitalize()}"
	return name
