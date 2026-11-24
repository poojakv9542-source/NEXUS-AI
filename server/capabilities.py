import json

CAPABILITIES = json.loads(r'''[
    {
        "id": "CAP-001",
        "category": "File management",
        "name": "List files in a selected folder",
        "implementation_status": "implemented",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "verified"
    },
    {
        "id": "CAP-002",
        "category": "File management",
        "name": "Read text files",
        "implementation_status": "implemented",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_individually_tested"
    },
    {
        "id": "CAP-003",
        "category": "File management",
        "name": "Find a file by its name",
        "implementation_status": "implemented",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_individually_tested"
    },
    {
        "id": "CAP-004",
        "category": "File management",
        "name": "Organize files into folders",
        "implementation_status": "implemented",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": true,
        "verification_status": "not_individually_tested"
    },
    {
        "id": "CAP-005",
        "category": "File management",
        "name": "Rename files",
        "implementation_status": "implemented",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": true,
        "verification_status": "not_individually_tested"
    },
    {
        "id": "CAP-006",
        "category": "File management",
        "name": "Identify duplicate files",
        "implementation_status": "implemented",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_individually_tested"
    },
    {
        "id": "CAP-007",
        "category": "File management",
        "name": "Summarize document contents",
        "implementation_status": "implemented",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_individually_tested"
    },
    {
        "id": "CAP-008",
        "category": "File management",
        "name": "Extract information from PDF and text files",
        "implementation_status": "implemented",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_individually_tested"
    },
    {
        "id": "CAP-009",
        "category": "Office and administrative tasks",
        "name": "Prepare daily work reports",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-010",
        "category": "Office and administrative tasks",
        "name": "Generate weekly performance reports",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-011",
        "category": "Office and administrative tasks",
        "name": "Create meeting summaries",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-012",
        "category": "Office and administrative tasks",
        "name": "Prepare meeting agendas",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-013",
        "category": "Office and administrative tasks",
        "name": "Draft professional emails",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-014",
        "category": "Office and administrative tasks",
        "name": "Create task lists for employees",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-015",
        "category": "Office and administrative tasks",
        "name": "Track pending assignments",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": true,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-016",
        "category": "Office and administrative tasks",
        "name": "Prepare project status reports",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-017",
        "category": "Office and administrative tasks",
        "name": "Generate employee attendance summaries from authorized data",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-018",
        "category": "Office and administrative tasks",
        "name": "Create official document drafts",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-019",
        "category": "Data analysis",
        "name": "Analyze Excel spreadsheets",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-020",
        "category": "Data analysis",
        "name": "Calculate total sales and revenue",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-021",
        "category": "Data analysis",
        "name": "Identify trends in business data",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-022",
        "category": "Data analysis",
        "name": "Compare monthly performance",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-023",
        "category": "Data analysis",
        "name": "Generate graphs and charts",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-024",
        "category": "Data analysis",
        "name": "Find missing values in datasets",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-025",
        "category": "Data analysis",
        "name": "Calculate employee productivity",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-026",
        "category": "Data analysis",
        "name": "Generate statistical summaries",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-027",
        "category": "Data analysis",
        "name": "Identify unusual data patterns",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-028",
        "category": "Data analysis",
        "name": "Create data analysis reports",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-029",
        "category": "Employee task management",
        "name": "Assign tasks to employees",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": true,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-030",
        "category": "Employee task management",
        "name": "Track task progress",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-031",
        "category": "Employee task management",
        "name": "Identify overdue tasks",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-032",
        "category": "Employee task management",
        "name": "Send task reminders",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": true,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-033",
        "category": "Employee task management",
        "name": "Generate employee performance summaries",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-034",
        "category": "Employee task management",
        "name": "Categorize tasks by priority",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-035",
        "category": "Employee task management",
        "name": "Track completed and pending work",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-036",
        "category": "Employee task management",
        "name": "Prepare department-wise reports",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-037",
        "category": "Employee task management",
        "name": "Escalate overdue tasks for manager review",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": true,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-038",
        "category": "Employee task management",
        "name": "Generate daily task summaries",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-039",
        "category": "Research and information gathering",
        "name": "Research a given topic",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-040",
        "category": "Research and information gathering",
        "name": "Summarize online articles",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-041",
        "category": "Research and information gathering",
        "name": "Compare products or services",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-042",
        "category": "Research and information gathering",
        "name": "Collect information from approved websites",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-043",
        "category": "Research and information gathering",
        "name": "Prepare competitor analysis",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-044",
        "category": "Research and information gathering",
        "name": "Generate research reports",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-045",
        "category": "Research and information gathering",
        "name": "Extract important information from documents",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-046",
        "category": "Research and information gathering",
        "name": "Prepare presentation outlines",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-047",
        "category": "Browser automation",
        "name": "Open approved websites",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-048",
        "category": "Browser automation",
        "name": "Search for information",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-049",
        "category": "Browser automation",
        "name": "Fill web forms with approval",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": true,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-050",
        "category": "Browser automation",
        "name": "Download authorized documents",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": true,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-051",
        "category": "Browser automation",
        "name": "Upload approved files",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": true,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-052",
        "category": "Browser automation",
        "name": "Extract information from web pages",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-053",
        "category": "Browser automation",
        "name": "Navigate company portals",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-054",
        "category": "Browser automation",
        "name": "Update information in approved systems",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": true,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-055",
        "category": "Communication and integrations",
        "name": "Draft emails",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-056",
        "category": "Communication and integrations",
        "name": "Send emails after approval",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": true,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-057",
        "category": "Communication and integrations",
        "name": "Read assigned work emails",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": true,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-058",
        "category": "Communication and integrations",
        "name": "Create calendar events",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": true,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-059",
        "category": "Communication and integrations",
        "name": "Schedule meetings",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": true,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-060",
        "category": "Communication and integrations",
        "name": "Send task notifications",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": true,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-061",
        "category": "Communication and integrations",
        "name": "Integrate with Jira",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-062",
        "category": "Communication and integrations",
        "name": "Integrate with Microsoft Teams",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-063",
        "category": "Communication and integrations",
        "name": "Integrate with Trello",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-064",
        "category": "Communication and integrations",
        "name": "Generate meeting follow-up messages",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-065",
        "category": "Management and decision support",
        "name": "Generate management dashboards",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-066",
        "category": "Management and decision support",
        "name": "Identify delayed projects",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-067",
        "category": "Management and decision support",
        "name": "Compare department performance",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-068",
        "category": "Management and decision support",
        "name": "Generate monthly reports",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-069",
        "category": "Management and decision support",
        "name": "Identify workload distribution",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-070",
        "category": "Management and decision support",
        "name": "Summarize business operations",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-071",
        "category": "Management and decision support",
        "name": "Highlight tasks requiring attention",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    },
    {
        "id": "CAP-072",
        "category": "Management and decision support",
        "name": "Prepare management summaries",
        "implementation_status": "planned",
        "test_mode": "local_mock_or_sample_data",
        "approval_required": false,
        "verification_status": "not_implemented"
    }
]''')
