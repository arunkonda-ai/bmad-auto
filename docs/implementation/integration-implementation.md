# BMAD Auto Integration Implementation

## Overview

This guide provides PM-centric integration implementation where John (PM) orchestrates all external service coordination through command simulation and database context. All external integrations flow through the PM hub with command logging, preserving `.bmad-core` integrity while enabling autonomous coordination.

## PM-Coordinated External Integration Architecture

### PM Integration Hub
```python
# bmad-auto/coordination/pm_integration_hub.py
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class ExternalService(str, Enum):
    LINEAR = "linear"
    GITHUB = "github"
    AI_SERVICES = "ai_services"
    AG_UI = "ag_ui"

class PMIntegrationHub:
    """
    John (PM) central coordination for external service integration
    All external API calls flow through PM with command logging
    """
    def __init__(self):
        self.pm_agent = john_pm_agent
        self.command_logger = CommandLogger()
        self.database_context = DatabaseContextManager()
        self.service_clients = self._initialize_service_clients()
        self.ag_ui = AGUICoordinator()

    async def coordinate_external_action(self, action_context: Dict[str, Any],
                                       target_service: ExternalService) -> Dict[str, Any]:
        """PM coordinates all external actions with command logging"""
        # PM analyzes action requirements
        pm_analysis = self.pm_agent.analyze_external_action(
            action_context=action_context,
            target_service=target_service
        )

        # Log PM decision for external coordination
        self.command_logger.log_pm_external_decision(
            service=target_service,
            action=action_context["action"],
            pm_rationale=pm_analysis.rationale,
            executing_agent=action_context.get("requesting_agent")
        )

        # Execute through service-specific coordinator
        if target_service == ExternalService.LINEAR:
            return await self._coordinate_linear_action(pm_analysis, action_context)
        elif target_service == ExternalService.GITHUB:
            return await self._coordinate_github_action(pm_analysis, action_context)
        elif target_service == ExternalService.AI_SERVICES:
            return await self._coordinate_ai_service_action(pm_analysis, action_context)
        elif target_service == ExternalService.AG_UI:
            return await self._coordinate_agui_action(pm_analysis, action_context)

    async def _coordinate_linear_action(self, pm_analysis: PMAnalysis,
                                      action_context: Dict[str, Any]) -> Dict[str, Any]:
        """PM coordinates Linear actions through MCP or direct API"""
        # Check MCP availability for Linear
        if self._is_mcp_available("linear"):
            # Use Linear MCP for coordination
            result = await self._execute_linear_mcp_action(pm_analysis, action_context)
        else:
            # Fallback to direct Linear API with PM oversight
            result = await self._execute_linear_api_action(pm_analysis, action_context)

        # PM processes result and updates database context
        await self._update_database_context_from_external(result, ExternalService.LINEAR)
        return result

# bmad-auto/integration/linear_coordinator.py
class PMLinearCoordinator:
    """
    PM coordinates Linear integration through MCP or direct API
    All Linear actions flow through PM with command logging
    """
    def __init__(self, pm_hub: PMIntegrationHub):
        self.pm_hub = pm_hub
        self.mcp_client = LinearMCPClient() if self._is_mcp_available() else None
        self.direct_client = LinearDirectClient() if not self.mcp_client else None

    async def create_task_from_agent_completion(self, agent_completion: Dict[str, Any]) -> Dict[str, Any]:
        """PM coordinates Linear task creation from agent completion"""
        # PM analyzes agent completion for Linear task requirements
        task_requirements = self.pm_hub.pm_agent.analyze_linear_task_requirements(
            agent_completion=agent_completion
        )

        # Execute through available client with PM oversight
        if self.mcp_client:
            result = await self._create_via_mcp(task_requirements)
        else:
            result = await self._create_via_direct_api(task_requirements)

        # PM logs Linear coordination action
        self.pm_hub.command_logger.log_linear_coordination(
            action="task_creation",
            agent=agent_completion["agent"],
            linear_result=result,
            pm_decision=task_requirements
        )

        return result

    async def _create_via_mcp(self, task_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create Linear task via MCP with PM coordination"""
        return await self.mcp_client.create_issue(
            team=task_requirements["team"],
            title=task_requirements["title"],
            description=task_requirements["description"],
            assignee=task_requirements.get("assignee"),
            labels=task_requirements.get("labels", [])
        )

    async def _create_via_direct_api(self, task_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create Linear task via direct API with PM coordination"""
        return await self.direct_client.create_workflow_issue(task_requirements)

class LinearMCPClient:
    """Linear MCP integration for PM-coordinated actions"""
    def __init__(self):
        self.mcp_connection = self._establish_mcp_connection()

    async def create_issue(self, team: str, title: str, description: str,
                          assignee: Optional[str] = None, labels: List[str] = None) -> Dict[str, Any]:
        """Create Linear issue via MCP"""
        mcp_result = await self.mcp_connection.call_tool(
            "mcp__linear__create_issue",
            {
                "team": team,
                "title": title,
                "description": description,
                "assignee": assignee,
                "labels": labels or []
            }
        )
        return mcp_result

class LinearDirectClient:
    """Direct Linear API client for PM-coordinated actions when MCP unavailable"""
    def __init__(self):
        self.api_key = os.getenv("LINEAR_API_KEY")
        self.base_url = "https://api.linear.app/graphql"
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def create_workflow_issue(self, task_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create Linear issue from PM task requirements"""
        mutation = """
        mutation CreateIssue($input: IssueCreateInput!) {
            issueCreate(input: $input) {
                success
                issue {
                    id
                    identifier
                    title
                    description
                    state { name }
                    assignee { name }
                    priority
                    labels { nodes { name } }
                    createdAt
                    updatedAt
                }
            }
        }
        """

        variables = {
            "input": {
                "teamId": await self._get_team_id(task_requirements["team"]),
                "title": task_requirements["title"],
                "description": task_requirements["description"],
                "priority": task_requirements.get("priority", 0),
                "labelIds": await self._get_label_ids(task_requirements.get("labels", [])),
                "assigneeId": await self._get_assignee_id(task_requirements.get("assignee"))
            }
        }

        result = await self._execute_graphql(mutation, variables)

        if result["data"]["issueCreate"]["success"]:
            issue_data = result["data"]["issueCreate"]["issue"]
            return {
                "linear_id": issue_data["id"],
                "identifier": issue_data["identifier"],
                "title": issue_data["title"],
                "status": "created",
                "created_at": issue_data["createdAt"]
            }

        raise Exception(f"Failed to create Linear issue: {result}")

    async def update_workflow_progress(self, issue_id: str, progress_data: Dict[str, Any]) -> bool:
        """Update Linear issue with workflow progress"""
        mutation = """
        mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
            issueUpdate(id: $id, input: $input) {
                success
                issue { id }
            }
        }
        """

        variables = {
            "id": issue_id,
            "input": {
                "description": progress_data.get("description"),
                "stateId": await self._get_state_id(progress_data.get("status")),
                "assigneeId": await self._get_assignee_id(progress_data.get("current_agent"))
            }
        }

        result = await self._execute_graphql(mutation, variables)
        return result["data"]["issueUpdate"]["success"]

    async def add_progress_comment(self, issue_id: str, workflow_state: WorkflowState) -> bool:
        """Add progress comment to Linear issue"""
        mutation = """
        mutation CreateComment($input: CommentCreateInput!) {
            commentCreate(input: $input) {
                success
                comment { id }
            }
        }
        """

        comment_body = self._generate_progress_comment(workflow_state)

        variables = {
            "input": {
                "issueId": issue_id,
                "body": comment_body
            }
        }

        result = await self._execute_graphql(mutation, variables)
        return result["data"]["commentCreate"]["success"]

    def _generate_progress_comment(self, workflow_state: WorkflowState) -> str:
        """Generate structured progress comment"""
        latest_checkpoint = workflow_state.checkpoints[-1] if workflow_state.checkpoints else None

        comment = f"""
## Workflow Progress Update

**Phase**: {workflow_state.phase.value.title()}
**Status**: {workflow_state.status.value.title()}
**Progress**: {workflow_state.progress_percentage:.1f}%
**Current Agent**: {workflow_state.current_agent.value.title() if workflow_state.current_agent else 'Unassigned'}

### Latest Activity
"""

        if latest_checkpoint:
            comment += f"""
**Action**: {latest_checkpoint.action}
**Agent**: {latest_checkpoint.agent.value.title() if latest_checkpoint.agent else 'System'}
**Confidence**: {latest_checkpoint.confidence_score or 'N/A'}
**Timestamp**: {latest_checkpoint.timestamp.isoformat()}
"""

        if workflow_state.human_approvals_required:
            comment += "\n### Pending Approvals\n"
            for approval in workflow_state.human_approvals_required:
                comment += f"- {approval.approval_type} (Required: {approval.required_role})\n"

        return comment

    async def _execute_graphql(self, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Execute GraphQL query against Linear API"""
        payload = {
            "query": query,
            "variables": variables
        }

        async with self.session.post(self.base_url, json=payload) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_text = await response.text()
                raise Exception(f"Linear API error: {response.status} - {error_text}")
```

## PM-Coordinated GitHub Integration

### GitHub Coordination Through PM Hub
```python
# bmad-auto/integration/github_coordinator.py
class PMGitHubCoordinator:
    """
    PM coordinates GitHub actions through command simulation and direct API
    All GitHub operations flow through PM with command logging
    """
    def __init__(self, pm_hub: PMIntegrationHub):
        self.pm_hub = pm_hub
        self.github_client = GitHubDirectClient()

    async def coordinate_development_completion(self, dev_completion: Dict[str, Any]) -> Dict[str, Any]:
        """PM coordinates GitHub actions from development completion"""
        # PM analyzes development completion for GitHub requirements
        github_requirements = self.pm_hub.pm_agent.analyze_github_requirements(
            dev_completion=dev_completion
        )

        # PM determines GitHub actions needed
        github_actions = []
        if github_requirements.needs_branch:
            github_actions.append("create_branch")
        if github_requirements.needs_pr:
            github_actions.append("create_pr")
        if github_requirements.needs_review:
            github_actions.append("request_review")

        # Execute GitHub actions with PM coordination
        results = []
        for action in github_actions:
            result = await self._execute_github_action(action, github_requirements)
            results.append(result)

            # PM logs each GitHub coordination action
            self.pm_hub.command_logger.log_github_coordination(
                action=action,
                agent=dev_completion["agent"],
                github_result=result,
                pm_decision=github_requirements
            )

        return {"github_actions": results, "pm_coordination": github_requirements}

    async def _execute_github_action(self, action: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Execute GitHub action with PM oversight"""
        if action == "create_branch":
            return await self.github_client.create_feature_branch(requirements)
        elif action == "create_pr":
            return await self.github_client.create_pull_request(requirements)
        elif action == "request_review":
            return await self.github_client.request_code_review(requirements)

class GitHubDirectClient:
    """Direct GitHub API client for PM-coordinated actions"""
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.repository = os.getenv("GITHUB_REPOSITORY")
        self.base_url = "https://api.github.com"
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def create_feature_branch(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create feature branch from PM requirements"""
        branch_name = f"feature/bmad-auto-{requirements['task_id']}"
        base_branch = requirements.get('base_branch', 'main')

        # Get base branch SHA
        base_ref = await self._get_ref(base_branch)
        base_sha = base_ref["object"]["sha"]

        # Create new branch
        await self._create_ref(f"refs/heads/{branch_name}", base_sha)

        return {
            "branch_name": branch_name,
            "base_branch": base_branch,
            "status": "created",
            "sha": base_sha
        }

    async def create_pull_request(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create pull request from PM requirements"""
        pr_data = {
            "title": f"[BMAD Auto] {requirements['title']}",
            "body": requirements['description'],
            "head": requirements['branch_name'],
            "base": requirements.get('base_branch', 'main'),
            "draft": requirements.get('is_draft', False)
        }

        url = f"{self.base_url}/repos/{self.repository}/pulls"

        async with self.session.post(url, json=pr_data) as response:
            if response.status == 201:
                pr_info = await response.json()
                return {
                    "pr_number": pr_info["number"],
                    "title": pr_info["title"],
                    "status": "created",
                    "url": pr_info["html_url"],
                    "created_at": pr_info["created_at"]
                }
            else:
                error_text = await response.text()
                raise Exception(f"Failed to create PR: {response.status} - {error_text}")

    async def update_pr_with_validation_results(self, pr_number: int,
                                              validation_results: Dict[str, Any]) -> bool:
        """Update pull request with validation results"""
        comment_body = self._generate_validation_comment(validation_results)

        comment_data = {"body": comment_body}
        url = f"{self.base_url}/repos/{self.repository}/issues/{pr_number}/comments"

        async with self.session.post(url, json=comment_data) as response:
            return response.status == 201

    def _generate_pr_description(self, workflow_state: WorkflowState) -> str:
        """Generate comprehensive PR description"""
        description = f"""
# BMAD Auto Generated Pull Request

## Workflow Summary
- **Workflow ID**: {workflow_state.workflow_id}
- **Phase**: {workflow_state.phase.value.title()}
- **Objective**: {workflow_state.context.objective}
- **Progress**: {workflow_state.progress_percentage:.1f}%

## Implementation Details

### Deliverables
"""

        for deliverable in workflow_state.context.deliverables:
            description += f"- {deliverable}\n"

        description += "\n### Quality Validation\n"

        for checkpoint in workflow_state.checkpoints[-3:]:  # Last 3 checkpoints
            description += f"""
**{checkpoint.agent.value.title() if checkpoint.agent else 'System'}**: {checkpoint.action}
- Confidence: {checkpoint.confidence_score or 'N/A'}
- Timestamp: {checkpoint.timestamp.isoformat()}
"""

        if workflow_state.human_approvals_required:
            description += "\n### Required Approvals\n"
            for approval in workflow_state.human_approvals_required:
                description += f"- [ ] {approval.approval_type} ({approval.required_role})\n"

        description += "\n---\n*Generated by BMAD Auto Orchestration System*"

        return description

    async def _get_ref(self, ref_name: str) -> Dict[str, Any]:
        """Get reference information"""
        url = f"{self.base_url}/repos/{self.repository}/git/refs/heads/{ref_name}"

        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to get ref {ref_name}")

    async def _create_ref(self, ref: str, sha: str) -> Dict[str, Any]:
        """Create new git reference"""
        ref_data = {
            "ref": ref,
            "sha": sha
        }

        url = f"{self.base_url}/repos/{self.repository}/git/refs"

        async with self.session.post(url, json=ref_data) as response:
            if response.status == 201:
                return await response.json()
            else:
                raise Exception(f"Failed to create ref {ref}")
```

## PM-Coordinated AG UI Integration

### AG UI Human-AI Collaboration Through PM Hub
```python
# bmad-auto/integration/agui_coordinator.py
class AGUICoordinator:
    """
    PM coordinates human-AI collaboration through AG UI interface
    Enables real-time monitoring and strategic decision support
    """
    def __init__(self, pm_hub: PMIntegrationHub):
        self.pm_hub = pm_hub
        self.agui_client = AGUIClient()
        self.collaboration_state = CollaborationState()

    async def coordinate_human_approval_request(self, approval_context: Dict[str, Any]) -> Dict[str, Any]:
        """PM coordinates human approval requests through AG UI"""
        # PM analyzes approval requirements
        approval_analysis = self.pm_hub.pm_agent.analyze_approval_requirements(
            context=approval_context
        )

        # Create AG UI approval request
        agui_request = {
            "request_type": "human_approval",
            "context": approval_context,
            "pm_analysis": approval_analysis,
            "timeout": approval_analysis.get("timeout", 300),  # 5 minutes default
            "urgency": approval_analysis.get("urgency", "normal")
        }

        # Send to AG UI for human interaction
        human_response = await self.agui_client.request_human_decision(agui_request)

        # PM processes human decision and updates context
        pm_integration = self.pm_hub.pm_agent.integrate_human_decision(
            approval_context=approval_context,
            human_decision=human_response
        )

        # Log human-AI collaboration
        self.pm_hub.command_logger.log_human_collaboration(
            interaction_type="approval_request",
            pm_analysis=approval_analysis,
            human_response=human_response,
            integration_result=pm_integration
        )

        return pm_integration

    async def coordinate_strategic_discussion(self, strategic_context: Dict[str, Any]) -> Dict[str, Any]:
        """PM coordinates strategic discussions via AG UI"""
        # PM prepares strategic discussion context
        discussion_prep = self.pm_hub.pm_agent.prepare_strategic_discussion(
            context=strategic_context
        )

        # Enable back-and-forth discussion via AG UI
        discussion_session = await self.agui_client.start_discussion_session(
            context=discussion_prep,
            discussion_type="strategic_planning",
            participants=["human", "pm_agent"]
        )

        # PM facilitates discussion and captures decisions
        strategic_decisions = await self._facilitate_strategic_discussion(discussion_session)

        return strategic_decisions

class AGUIClient:
    """
    AG UI client for human-AI collaboration interface
    """
    def __init__(self):
        self.agui_endpoint = os.getenv("AGUI_ENDPOINT")
        self.session_manager = AGUISessionManager()

    async def request_human_decision(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Request human decision through AG UI interface"""
        session = await self.session_manager.create_session(
            session_type="approval_request",
            context=request
        )

        # Display context and options to human via AG UI
        await self._display_approval_interface(session, request)

        # Wait for human response with timeout
        human_response = await self._await_human_response(
            session_id=session.id,
            timeout=request.get("timeout", 300)
        )

        return human_response

# bmad-auto/context_management/mcp_context_manager.py
class MCPContextManager:
    """PM-coordinated context management through MCP integrations"""

    def __init__(self, pm_hub: PMIntegrationHub, mcp_connections: Dict[str, str]):
        self.pm_hub = pm_hub
        self.connections = mcp_connections
        self.context_cache: Dict[str, Any] = {}
        self.cache_ttl = 3600  # 1 hour

    async def get_agent_context_via_pm(self, agent_id: str, context_request: Dict[str, Any]) -> Dict[str, Any]:
        """PM coordinates agent context retrieval through MCP"""
        # PM analyzes context requirements for agent
        context_analysis = self.pm_hub.pm_agent.analyze_agent_context_needs(
            agent_id=agent_id,
            context_request=context_request
        )

        # PM determines which MCP sources to query
        mcp_sources = context_analysis.required_sources

        # Fetch context through PM coordination
        context_data = {}
        for source in mcp_sources:
            source_data = await self._fetch_from_mcp_source(source, context_analysis)
            context_data[source] = source_data

        # PM filters and distributes context to agent
        filtered_context = self.pm_hub.pm_agent.filter_context_for_agent(
            agent_id=agent_id,
            raw_context=context_data,
            context_analysis=context_analysis
        )

        # Log PM context distribution
        self.pm_hub.command_logger.log_context_distribution(
            agent=agent_id,
            sources=mcp_sources,
            filtered_context_size=len(str(filtered_context)),
            pm_analysis=context_analysis
        )

        return filtered_context

    async def get_project_intelligence(self, project_context: Dict[str, Any]) -> Dict[str, Any]:
        """Gather project-specific intelligence from integrated sources"""
        intelligence = {
            "sprint_status": {},
            "team_communication": {},
            "system_health": {},
            "recent_changes": {}
        }

        # Parallel intelligence gathering
        tasks = []

        if "jira_mcp" in self.connections:
            tasks.append(self._fetch_sprint_intelligence(project_context))

        if "slack_mcp" in self.connections:
            tasks.append(self._fetch_communication_intelligence(project_context))

        if "monitoring_mcp" in self.connections:
            tasks.append(self._fetch_system_intelligence(project_context))

        if "github_mcp" in self.connections:
            tasks.append(self._fetch_code_intelligence(project_context))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Combine results
        for i, result in enumerate(results):
            if not isinstance(result, Exception):
                intelligence.update(result)

        return intelligence

    async def enhance_agent_context(self, agent_type: AgentType,
                                  workflow_context: WorkflowContext) -> Dict[str, Any]:
        """Dynamically enhance agent context with MCP data"""
        enhanced_context = {
            "base_context": workflow_context.dict(),
            "dynamic_enhancements": {}
        }

        # Agent-specific context enhancement
        if agent_type == AgentType.MARY:
            # Market intelligence enhancements
            market_data = await self._fetch_market_intelligence(workflow_context)
            enhanced_context["dynamic_enhancements"]["market_intelligence"] = market_data

        elif agent_type == AgentType.JAMES:
            # Technical context enhancements
            tech_context = await self._fetch_technical_context(workflow_context)
            enhanced_context["dynamic_enhancements"]["technical_intelligence"] = tech_context

        elif agent_type == AgentType.QUINN:
            # Quality context enhancements
            quality_data = await self._fetch_quality_intelligence(workflow_context)
            enhanced_context["dynamic_enhancements"]["quality_intelligence"] = quality_data

        return enhanced_context

    async def _fetch_from_docs_mcp(self, technology: str, context_type: str) -> Dict[str, Any]:
        """Fetch documentation from official docs MCP"""
        # Implementation for official documentation MCP
        pass

    async def _fetch_market_intelligence(self, context: WorkflowContext) -> Dict[str, Any]:
        """Fetch market intelligence for business analyst"""
        # Implementation for market data gathering
        pass

    async def _fetch_technical_context(self, context: WorkflowContext) -> Dict[str, Any]:
        """Fetch technical context for developer"""
        # Implementation for technical intelligence
        pass
```

## PM-Coordinated AI Service Integration

### PM AI Service Orchestration
```python
# bmad-auto/ai_coordination/ai_service_manager.py
from typing import Dict, List, Optional, Any
from enum import Enum

class AIProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AZURE = "azure"
    BEDROCK = "bedrock"

class ModelCapability(str, Enum):
    TEXT_GENERATION = "text_generation"
    CODE_GENERATION = "code_generation"
    ANALYSIS = "analysis"
    REASONING = "reasoning"
    MULTIMODAL = "multimodal"

class PMAIServiceCoordinator:
    """PM coordinates AI service usage across 10-agent ecosystem"""

    def __init__(self, pm_hub: PMIntegrationHub, service_configs: Dict[AIProvider, Dict[str, Any]]):
        self.pm_hub = pm_hub
        self.services = {}
        self.cost_tracker = AICostTracker()
        self.performance_tracker = AIPerformanceTracker()

        for provider, config in service_configs.items():
            self.services[provider] = self._initialize_service(provider, config)

    async def coordinate_agent_ai_request(self, agent_id: str, request_type: ModelCapability,
                                        context: Dict[str, Any]) -> Dict[str, Any]:
        """PM coordinates AI service requests from agents"""
        # PM analyzes agent AI request
        request_analysis = self.pm_hub.pm_agent.analyze_agent_ai_requirements(
            agent_id=agent_id,
            request_type=request_type,
            context=context
        )

        # PM selects optimal provider based on agent needs and cost efficiency
        optimal_provider = await self._pm_select_provider(
            request_analysis=request_analysis,
            agent_context=context
        )

        # Execute request with PM oversight
        try:
            result = await self._execute_request_with_pm_oversight(
                provider=optimal_provider,
                request_analysis=request_analysis,
                context=context
            )

            # PM tracks usage and cost across agents
            await self._pm_track_ai_usage(
                agent_id=agent_id,
                provider=optimal_provider,
                request_type=request_type,
                result=result
            )

            return result

        except Exception as e:
            # PM coordinates fallback with cost awareness
            return await self._pm_coordinate_fallback(
                failed_provider=optimal_provider,
                request_analysis=request_analysis,
                context=context,
                error=e
            )

    async def _select_optimal_provider(self, request_type: ModelCapability,
                                     context: Dict[str, Any],
                                     preferences: Optional[Dict[str, Any]]) -> AIProvider:
        """Select optimal AI provider based on multiple factors"""
        selection_criteria = {
            "capability_match": 0.4,
            "cost_efficiency": 0.3,
            "performance_history": 0.2,
            "availability": 0.1
        }

        provider_scores = {}

        for provider in self.services.keys():
            score = 0.0

            # Capability matching
            capability_score = await self._evaluate_capability_match(provider, request_type)
            score += capability_score * selection_criteria["capability_match"]

            # Cost efficiency
            cost_score = await self.cost_tracker.get_cost_efficiency_score(provider, request_type)
            score += cost_score * selection_criteria["cost_efficiency"]

            # Performance history
            performance_score = await self.load_balancer.get_performance_score(provider)
            score += performance_score * selection_criteria["performance_history"]

            # Availability
            availability_score = await self._check_availability(provider)
            score += availability_score * selection_criteria["availability"]

            provider_scores[provider] = score

        # Return provider with highest score
        return max(provider_scores, key=provider_scores.get)

    async def optimize_context_distribution(self, agents: List[AgentType],
                                          context_requirements: Dict[str, Any]) -> Dict[AgentType, Dict[str, Any]]:
        """Optimize context distribution across agents based on AI service capabilities"""
        optimized_contexts = {}

        for agent in agents:
            # Determine agent's AI requirements
            agent_requirements = self._get_agent_ai_requirements(agent)

            # Optimize context for agent's AI capabilities
            optimized_context = await self._optimize_agent_context(
                agent, agent_requirements, context_requirements
            )

            optimized_contexts[agent] = optimized_context

        return optimized_contexts

    def _get_agent_ai_requirements(self, agent_id: str) -> Dict[str, Any]:
        """Get AI service requirements for specific agent in 10-agent ecosystem"""
        requirements_map = {
            "mary": {  # Business Analyst
                "primary_capability": ModelCapability.ANALYSIS,
                "secondary_capabilities": [ModelCapability.REASONING],
                "context_size": "large",
                "response_time": "standard",
                "cost_sensitivity": "medium"
            },
            "john": {  # Product Manager (PM)
                "primary_capability": ModelCapability.REASONING,
                "secondary_capabilities": [ModelCapability.TEXT_GENERATION, ModelCapability.ANALYSIS],
                "context_size": "large",
                "response_time": "fast",
                "cost_sensitivity": "low"  # PM needs high quality for coordination
            },
            "james": {  # Developer
                "primary_capability": ModelCapability.CODE_GENERATION,
                "secondary_capabilities": [ModelCapability.ANALYSIS, ModelCapability.REASONING],
                "context_size": "medium",
                "response_time": "fast",
                "cost_sensitivity": "medium"
            },
            "quinn": {  # QA Engineer
                "primary_capability": ModelCapability.ANALYSIS,
                "secondary_capabilities": [ModelCapability.REASONING],
                "context_size": "medium",
                "response_time": "standard",
                "cost_sensitivity": "high"
            },
            "sally": {  # UX Designer
                "primary_capability": ModelCapability.MULTIMODAL,
                "secondary_capabilities": [ModelCapability.TEXT_GENERATION],
                "context_size": "large",
                "response_time": "standard",
                "cost_sensitivity": "medium"
            },
            "alex": {  # Architect
                "primary_capability": ModelCapability.REASONING,
                "secondary_capabilities": [ModelCapability.ANALYSIS, ModelCapability.CODE_GENERATION],
                "context_size": "large",
                "response_time": "standard",
                "cost_sensitivity": "low"  # Architecture decisions need high quality
            },
            "po": {  # Product Owner
                "primary_capability": ModelCapability.TEXT_GENERATION,
                "secondary_capabilities": [ModelCapability.REASONING],
                "context_size": "medium",
                "response_time": "standard",
                "cost_sensitivity": "medium"
            },
            "sm": {  # Scrum Master
                "primary_capability": ModelCapability.TEXT_GENERATION,
                "secondary_capabilities": [ModelCapability.ANALYSIS],
                "context_size": "small",
                "response_time": "fast",
                "cost_sensitivity": "high"
            },
            "bmad_orchestrator": {  # BMAD Orchestrator
                "primary_capability": ModelCapability.REASONING,
                "secondary_capabilities": [ModelCapability.TEXT_GENERATION, ModelCapability.ANALYSIS],
                "context_size": "large",
                "response_time": "fast",
                "cost_sensitivity": "low"
            },
            "bmad_master": {  # BMAD Master
                "primary_capability": ModelCapability.REASONING,
                "secondary_capabilities": [ModelCapability.TEXT_GENERATION, ModelCapability.ANALYSIS],
                "context_size": "large",
                "response_time": "fast",
                "cost_sensitivity": "low"
            }
        }

        return requirements_map.get(agent_id, {})
```

## PM-Coordinated Integration Monitoring

### PM Integration Health Oversight
```python
# bmad-auto/monitoring/integration_health_monitor.py
class PMIntegrationHealthMonitor:
    """PM coordinates monitoring of all external integrations with AG UI visibility"""

    def __init__(self, pm_hub: PMIntegrationHub, integrations: Dict[str, Any]):
        self.pm_hub = pm_hub
        self.integrations = integrations
        self.health_metrics = {}
        self.alert_thresholds = self._load_alert_thresholds()
        self.agui_dashboard = AGUIDashboard()

    async def pm_monitor_all_integrations(self) -> Dict[str, Dict[str, Any]]:
        """PM coordinates monitoring of all integrations with AG UI dashboard updates"""
        # PM analyzes monitoring priorities based on current operations
        monitoring_priorities = self.pm_hub.pm_agent.analyze_monitoring_priorities()

        health_status = {}
        monitoring_tasks = [
            self._monitor_linear_health(),
            self._monitor_github_health(),
            self._monitor_ai_services_health(),
            self._monitor_agui_health(),
            self._monitor_command_logging_health()
        ]

        results = await asyncio.gather(*monitoring_tasks, return_exceptions=True)

        integration_names = ["linear", "github", "ai_services", "ag_ui", "command_logging"]
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                health_status[integration_names[i]] = {
                    "status": "error",
                    "error": str(result),
                    "timestamp": datetime.now().isoformat(),
                    "pm_priority": monitoring_priorities.get(integration_names[i], "medium")
                }
            else:
                health_status[integration_names[i]] = result

        # PM analyzes health status and determines alerts
        pm_health_analysis = self.pm_hub.pm_agent.analyze_integration_health(health_status)

        # Update AG UI dashboard with health status
        await self.agui_dashboard.update_integration_health(health_status, pm_health_analysis)

        # PM coordinates alerts based on analysis
        await self._pm_coordinate_alerts(pm_health_analysis)

        return {"health_status": health_status, "pm_analysis": pm_health_analysis}

    async def _monitor_linear_health(self) -> Dict[str, Any]:
        """Monitor Linear integration health"""
        try:
            async with LinearClient(self.integrations["linear"]["api_key"], "") as client:
                # Test basic connectivity
                start_time = time.time()
                await client._execute_graphql("query { viewer { id } }", {})
                response_time = time.time() - start_time

                return {
                    "status": "healthy",
                    "response_time": response_time,
                    "last_sync": self._get_last_sync_time("linear"),
                    "sync_success_rate": self._get_sync_success_rate("linear"),
                    "timestamp": datetime.now().isoformat()
                }

        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def _check_and_send_alerts(self, health_status: Dict[str, Dict[str, Any]]):
        """Check health status against thresholds and send alerts"""
        alerts = []

        for service, status in health_status.items():
            if status["status"] == "unhealthy":
                alerts.append({
                    "severity": "critical",
                    "service": service,
                    "message": f"{service} integration is unhealthy: {status.get('error', 'Unknown error')}"
                })

            elif status["status"] == "healthy":
                # Check performance thresholds
                response_time = status.get("response_time", 0)
                threshold = self.alert_thresholds.get(service, {}).get("response_time", 5.0)

                if response_time > threshold:
                    alerts.append({
                        "severity": "warning",
                        "service": service,
                        "message": f"{service} response time ({response_time:.2f}s) exceeds threshold ({threshold}s)"
                    })

        # Send alerts if any
        if alerts:
            await self._send_alerts(alerts)

    async def _pm_coordinate_alerts(self, pm_analysis: Dict[str, Any]):
        """PM coordinates integration health alerts through AG UI and command logging"""
        critical_issues = pm_analysis.get("critical_issues", [])
        warnings = pm_analysis.get("warnings", [])

        # PM determines alert escalation strategy
        for issue in critical_issues:
            # Escalate to human via AG UI for critical integration failures
            await self.agui_dashboard.escalate_critical_issue(
                issue=issue,
                pm_recommendation=pm_analysis.get("recommendations", {})
            )

            # Log PM alert coordination decision
            self.pm_hub.command_logger.log_alert_coordination(
                alert_type="critical",
                issue=issue,
                pm_action="human_escalation"
            )

        for warning in warnings:
            # PM handles warnings through automated response or monitoring
            await self._pm_handle_warning(warning, pm_analysis)

# Command Logging Service for PM External Coordination
class CommandLoggingService:
    """
    Logs all PM external coordination commands for system learning and audit
    """
    def __init__(self, database_context: DatabaseContextManager):
        self.database = database_context
        self.log_storage = LogStorage()

    async def log_pm_external_decision(self, service: str, action: str,
                                     pm_rationale: str, executing_agent: str):
        """Log PM decision for external service coordination"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "coordinator": "john_pm",
            "service": service,
            "action": action,
            "rationale": pm_rationale,
            "executing_agent": executing_agent,
            "log_type": "external_coordination"
        }

        await self.database.store_command_log(log_entry)
        await self.log_storage.persist_log(log_entry)

    async def log_linear_coordination(self, action: str, agent: str,
                                    linear_result: Dict[str, Any], pm_decision: Dict[str, Any]):
        """Log PM Linear coordination with MCP or direct API"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "coordinator": "john_pm",
            "service": "linear",
            "action": action,
            "agent": agent,
            "result": linear_result,
            "pm_decision": pm_decision,
            "integration_method": "mcp" if self._used_mcp(linear_result) else "direct_api"
        }

        await self.database.store_command_log(log_entry)

    async def log_human_collaboration(self, interaction_type: str,
                                    pm_analysis: Dict[str, Any],
                                    human_response: Dict[str, Any],
                                    integration_result: Dict[str, Any]):
        """Log PM coordination of human-AI collaboration via AG UI"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "coordinator": "john_pm",
            "interaction_type": interaction_type,
            "pm_analysis": pm_analysis,
            "human_response": human_response,
            "integration_result": integration_result,
            "collaboration_method": "ag_ui"
        }

        await self.database.store_command_log(log_entry)
```

## PM-Coordinated Integration Deployment

### bmad-auto Folder Structure
```
bmad-auto/
├── coordination/
│   ├── pm_integration_hub.py      # Central PM coordination for external services
│   └── command_logging_service.py # PM external coordination logging
├── integration/
│   ├── linear_coordinator.py      # PM Linear integration via MCP/API
│   ├── github_coordinator.py      # PM GitHub coordination
│   ├── agui_coordinator.py        # PM AG UI human collaboration
│   └── service_health_monitor.py  # PM integration health oversight
├── context_management/
│   ├── mcp_context_manager.py     # PM MCP context coordination
│   └── database_context.py        # PM database context distribution
├── ai_coordination/
│   ├── ai_service_manager.py      # PM AI service coordination
│   └── cost_optimization.py       # PM AI cost management
└── monitoring/
    ├── integration_health.py      # PM integration monitoring
    └── agui_dashboard.py          # AG UI monitoring interface
```

### PM Integration Configuration
```python
# bmad-auto/config/integration_config.py
class PMIntegrationConfig:
    """
    PM-coordinated integration configuration with command simulation support
    """
    def __init__(self):
        self.external_services = {
            "linear": {
                "coordination_method": "mcp_preferred",  # MCP first, fallback to API
                "mcp_endpoint": os.getenv("LINEAR_MCP_ENDPOINT"),
                "api_key": os.getenv("LINEAR_API_KEY"),
                "pm_oversight": True,
                "command_logging": True
            },
            "github": {
                "coordination_method": "direct_api",  # No MCP available
                "api_token": os.getenv("GITHUB_TOKEN"),
                "repository": os.getenv("GITHUB_REPOSITORY"),
                "pm_oversight": True,
                "command_logging": True
            },
            "ag_ui": {
                "coordination_method": "direct_interface",
                "endpoint": os.getenv("AGUI_ENDPOINT"),
                "pm_facilitation": True,
                "real_time_monitoring": True
            }
        }

        self.pm_coordination = {
            "batch_processing_interval": 300,  # 5 minutes
            "command_log_retention": 30,  # 30 days
            "context_distribution_timeout": 60,  # 1 minute
            "human_approval_timeout": 300  # 5 minutes default
        }

        self.quality_gates = {
            "integration_health_threshold": 0.95,
            "response_time_threshold": 5.0,  # seconds
            "cost_efficiency_threshold": 0.8,
            "pm_oversight_required_for": ["critical_decisions", "external_api_calls"]
        }
```

## PM Integration Command Patterns

### Command Simulation for External Services
```python
# Example PM coordination patterns for external integration

# PM coordinates Linear task creation from agent completion
linear_result = await pm_integration_hub.coordinate_external_action(
    action_context={
        "action": "create_task",
        "requesting_agent": "james",
        "task_data": {
            "title": "Implement user authentication",
            "description": "Develop secure user auth system",
            "assignee": "james",
            "labels": ["backend", "security"]
        }
    },
    target_service=ExternalService.LINEAR
)

# PM coordinates GitHub PR creation from development completion
github_result = await pm_integration_hub.coordinate_external_action(
    action_context={
        "action": "create_pr",
        "requesting_agent": "james",
        "pr_data": {
            "title": "Add user authentication system",
            "branch_name": "feature/user-auth",
            "description": "Implements secure authentication with JWT tokens"
        }
    },
    target_service=ExternalService.GITHUB
)

# PM coordinates human approval via AG UI
approval_result = await pm_integration_hub.coordinate_external_action(
    action_context={
        "action": "request_approval",
        "requesting_agent": "john",
        "approval_data": {
            "approval_type": "architecture_decision",
            "context": "Database schema changes for user management",
            "options": ["PostgreSQL", "MongoDB", "Hybrid approach"]
        }
    },
    target_service=ExternalService.AG_UI
)
```

---

*This PM-centric integration implementation provides robust external service coordination through command simulation, preserving `.bmad-core` integrity while enabling autonomous orchestration with comprehensive monitoring and human collaboration capabilities.*