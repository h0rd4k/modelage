def get_prefix(table_type):
	return {
		"Fakta": "F_",
		"Dimension": "D_",
		"Lookup": "L_"
	}.get(table_type, "")

def capitalize_first(name: str) -> str:
	return name[0].upper() + name[1:] if name else name

def apply_prefix_and_capitalize(name: str, prefix: str) -> str:
	name = name.strip()
	if not name.startswith(prefix):
		name = f"{prefix}{name}"
	actual_name = name[len(prefix):]
	return f"{prefix}{capitalize_first(actual_name)}"
