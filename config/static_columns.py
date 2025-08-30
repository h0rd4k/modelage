STATIC_TABLE_COLUMNS = {
	"Fakta": [
		{
			"name": "{table_name}_ID",
			"data_type": "INT",
			"is_identity": True,
			"nullable": "NOT NULL",
			"is_primary_key": True,
			"column_type": "Statisk",
			"sort_order": 0
		},
		{
			"name": "{table_name}_Nyckel",
			"data_type": "NVARCHAR",
			"length": "50",
			"nullable": "NOT NULL",
			"column_type": "Statisk",
			"sort_order": 1
		},
		{
			"name": "Checksumma",
			"data_type": "VARBINARY",
			"length": "50",
			"nullable": "NULL",
			"column_type": "Statisk",
			"sort_order": 2
		},
		{
			"name": "Audit_ID_Insert",
			"data_type": "INT",
			"nullable": "NULL",
			"column_type": "Statisk",
			"sort_order": 3
		},
		{
			"name": "Audit_ID_Update",
			"data_type": "INT",
			"nullable": "NULL",
			"column_type": "Statisk",
			"sort_order": 4
		},
		{
			"name": "Audit_ID_Delete",
			"data_type": "INT",
			"nullable": "NULL",
			"column_type": "Statisk",
			"sort_order": 5
		}
	],

	"Dimension": [
		{
			"name": "{table_name}_ID",
			"data_type": "INT",
			"is_identity": True,
			"nullable": "NOT NULL",
			"is_primary_key": True,
			"column_type": "Statisk",
			"sort_order": 0
		},
		{
			"name": "{table_name}_Nyckel",
			"data_type": "NVARCHAR",
			"length": "50",
			"nullable": "NOT NULL",
			"column_type": "Statisk",
			"sort_order": 1
		},
		{
			"name": "Checksumma",
			"data_type": "VARBINARY",
			"length": "50",
			"nullable": "NULL",
			"column_type": "Statisk",
			"sort_order": 2
		},
		{
			"name": "Audit_ID_Insert",
			"data_type": "DATETIME",
			"nullable": "NULL",
			"column_type": "Statisk",
			"sort_order": 3
		},
		{
			"name": "Audit_ID_Update",
			"data_type": "DATETIME",
			"nullable": "NULL",
			"column_type": "Statisk",
			"sort_order": 4
		},
		{
			"name": "Audit_ID_Delete",
			"data_type": "DATETIME",
			"nullable": "NULL",
			"column_type": "Statisk",
			"sort_order": 5
		}
	]
}
