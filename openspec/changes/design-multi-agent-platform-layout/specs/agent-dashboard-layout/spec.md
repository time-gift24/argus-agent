## ADDED Requirements

### Requirement: Unified Sidebar Navigation
The system SHALL provide a sidebar containing links to all core agent management functions, including Agents, Global Settings, and System Logs.

#### Scenario: Navigate to Agent List
- **WHEN** user clicks on the "Agents" link in the sidebar
- **THEN** the system SHALL display the agent list view in the main content area

### Requirement: Global Header with Status Summary
The system SHALL display a fixed header containing the platform logo, current user profile, and a summary of global agent health (Total, Active, Error).

#### Scenario: View Global Status
- **WHEN** the dashboard is loaded or refreshed
- **THEN** the system SHALL display the current count of agents and their aggregate health status in the header indicators
