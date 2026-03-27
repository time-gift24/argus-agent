## 1. Project Setup

- [ ] 1.1 Install OpenTiny (TinyVue) and Tailwind CSS dependencies
- [ ] 1.2 Configure Fira Code and Fira Sans typography in the global theme
- [ ] 1.3 Initialize Pinia store for centralized agent state management

## 2. Core Layout & Navigation

- [ ] 2.1 Implement the `AgentDashboardLayout` shell using OpenTiny Layout and Sidebar components
- [ ] 2.2 Create the `GlobalHeader` component with agent health status indicators (Total, Active, Error)
- [ ] 2.3 Set up Vue Router for Agent List, Agent Details, and Interaction views

## 3. Agent Management Views

- [ ] 3.1 Build the `AgentListView` using a high-density OpenTiny grid with status filtering
- [ ] 3.2 Implement the `BulkActionsToolbar` to allow starting/stopping multiple agents
- [ ] 3.3 Develop the `AgentDetailsView` with performance charts and a tabbed interface for logs/settings

## 4. Interaction & Refinement

- [ ] 4.1 Create the `AgentInteractionShell` with terminal-style text input and command history support
- [ ] 4.2 Apply Flat Design aesthetics and transition effects (150-200ms) to all interactive elements
- [ ] 4.3 Verify responsive behavior at 375px, 768px, 1024px, and 1440px breakpoints
