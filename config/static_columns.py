STATIC_TABLE_COLUMNS = {
	"Fakta": [
		{
			"name": "{table_name}_ID",
			"data_type": "INT",
			"is_identity": True,
			"nullable": "NOT NULL",
			"is_primary_key": True,
			"column_type": "Statisk"
		},
		{
			"name": "{table_name}_Nyckel",
			"data_type": "NVARCHAR",
			"length": "50",
			"nullable": "NOT NULL",
			"column_type": "Statisk"
		},
		{
			"name": "Checksumma",
			"data_type": "VARBINARY",
			"length": "50",
			"nullable": "NULL",
			"column_type": "Statisk"
		},
		{
			"name": "Tidstämpel_Insert",
			"data_type": "DATETIME",
			"nullable": "NULL",
			"column_type": "Statisk"
		},
		{
			"name": "Tidstämpel_Update",
			"data_type": "DATETIME",
			"nullable": "NULL",
			"column_type": "Statisk"
		}
	],

	"Dimension": [
		{
			"name": "{table_name}_ID",
			"data_type": "INT",
			"is_identity": True,
			"nullable": "NOT NULL",
			"is_primary_key": True,
			"column_type": "Statisk"
		},
		{
			"name": "{table_name}_Nyckel",
			"data_type": "NVARCHAR",
			"length": "50",
			"nullable": "NOT NULL",
			"column_type": "Statisk"
		},
		{
			"name": "Checksumma",
			"data_type": "VARBINARY",
			"length": "50",
			"nullable": "NULL",
			"column_type": "Statisk"
		},
		{
			"name": "Tidstämpel_Insert",
			"data_type": "DATETIME",
			"nullable": "NULL",
			"column_type": "Statisk"
		},
		{
			"name": "Tidstämpel_Update",
			"data_type": "DATETIME",
			"nullable": "NULL",
			"column_type": "Statisk"
		}
	]
}
