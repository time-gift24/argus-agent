## ADDED Requirements

### Requirement: High-Density Agent Grid
The system SHALL display all registered agents in a high-density, searchable grid with status indicators, agent names, and last-activity timestamps.

#### Scenario: Filter Agents by Status
- **WHEN** user selects the "Error" filter in the agent list toolbar
- **THEN** the system SHALL update the grid to only display agents currently in an error state

### Requirement: Bulk Actions Toolbar
The system SHALL provide a toolbar for common actions like starting, stopping, or updating multiple agents simultaneously.

#### Scenario: Select Multiple Agents
- **WHEN** user checks the select boxes for multiple agents in the grid
- **THEN** the system SHALL enable the bulk action buttons (Start, Stop, Restart) in the toolbar
