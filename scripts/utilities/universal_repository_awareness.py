#!/usr/bin/env python3
"""
AbëFLOWs Universal Repository Awareness System
Deep Epistemic Source Pattern - Complete Access & Universal Awareness
IS SOURCE × CLEAR × EASY × COMPLETE
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

class RepositoryType(Enum):
    """Repository classification."""
    FOUNDATION = "foundation"
    MODULE = "module"
    SERVICE = "service"
    TOOL = "tool"
    PLATFORM = "platform"
    TEMPLATE = "template"
    EXTENSION = "extension"
    RESEARCH = "research"
    UNKNOWN = "unknown"

class AccessLevel(Enum):
    """Access level classification."""
    PUBLIC = "public"
    PRIVATE = "private"
    UNKNOWN = "unknown"

@dataclass
class RepositoryMetadata:
    """Complete repository metadata - epistemic source pattern."""
    source: str
    name: str
    url: str
    is_private: bool
    description: str
    type: RepositoryType
    access_level: AccessLevel
    language: Optional[str] = None
    stars: Optional[int] = None
    forks: Optional[int] = None
    last_updated: Optional[str] = None
    topics: List[str] = None
    dependencies: List[str] = None
    capabilities: List[str] = None
    convergence_value: Optional[str] = None
    integration_points: List[str] = None

class UniversalRepositoryAwareness:
    """
    Deep epistemic source pattern system.
    
    Provides complete access and universal awareness of all repositories
    across all 4 Git sources.
    """
    
    def __init__(self):
        self.repositories: Dict[str, RepositoryMetadata] = {}
        self.sources = {
            "jimmy-dejesus": "Jimmy-Dejesus",
            "bravetto": "bravetto",
            "bravetto-backend": "BravettoBackendTeam"
        }
        self.awareness_map: Dict[str, Any] = {}
    
    def discover_all_repositories(self) -> Dict[str, List[RepositoryMetadata]]:
        """
        Discover all repositories from all sources.
        
        Epistemic Proof: What IS (observable, verifiable).
        """
        all_repos = {}
        
        for source_id, source_name in self.sources.items():
            print(f"Discovering repositories from {source_name}...")
            repos = self._discover_source_repositories(source_id, source_name)
            all_repos[source_id] = repos
            print(f"  Found {len(repos)} repositories")
        
        return all_repos
    
    def _discover_source_repositories(
        self,
        source_id: str,
        source_name: str
    ) -> List[RepositoryMetadata]:
        """Discover repositories from a specific source."""
        repos = []
        
        try:
            # Use GitHub CLI to list repositories
            result = subprocess.run(
                ["gh", "repo", "list", source_name, "--limit", "1000", "--json", 
                 "name,url,isPrivate,description,primaryLanguage,stargazerCount,forkCount,updatedAt,repositoryTopics"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"  Error: {result.stderr}")
                return repos
            
            repo_data = json.loads(result.stdout)
            
            for repo in repo_data:
                metadata = RepositoryMetadata(
                    source=source_id,
                    name=repo["name"],
                    url=repo["url"],
                    is_private=repo.get("isPrivate", False),
                    description=repo.get("description", ""),
                    type=self._classify_repository(repo["name"], repo.get("description", "")),
                    access_level=AccessLevel.PRIVATE if repo.get("isPrivate") else AccessLevel.PUBLIC,
                    language=repo.get("primaryLanguage", {}).get("name") if repo.get("primaryLanguage") else None,
                    stars=repo.get("stargazerCount", 0),
                    forks=repo.get("forkCount", 0),
                    last_updated=repo.get("updatedAt"),
                    topics=[t.get("name", "") for t in (repo.get("repositoryTopics", {}).get("nodes", []) if isinstance(repo.get("repositoryTopics"), dict) else [])] if repo.get("repositoryTopics") else [],
                    dependencies=[],
                    capabilities=[],
                    convergence_value=None,
                    integration_points=[]
                )
                
                repos.append(metadata)
                key = f"{source_id}/{repo['name']}"
                self.repositories[key] = metadata
        
        except Exception as e:
            print(f"  Error discovering {source_name}: {e}")
        
        return repos
    
    def _classify_repository(self, name: str, description: str) -> RepositoryType:
        """Classify repository type based on name and description."""
        name_lower = name.lower()
        desc_lower = description.lower()
        
        # Foundation repositories
        if any(x in name_lower for x in ["core", "foundation", "base", "aiagentsuite"]):
            return RepositoryType.FOUNDATION
        
        # Service repositories
        if any(x in name_lower for x in ["service", "api", "backend", "guard", "microservice"]):
            return RepositoryType.SERVICE
        
        # Module repositories
        if any(x in name_lower for x in ["module", "component", "lib"]):
            return RepositoryType.MODULE
        
        # Tool repositories
        if any(x in name_lower for x in ["tool", "cli", "sdk", "devtools"]):
            return RepositoryType.TOOL
        
        # Platform repositories
        if any(x in name_lower for x in ["platform", "recruitment", "ide", "desk"]):
            return RepositoryType.PLATFORM
        
        # Extension repositories
        if any(x in name_lower for x in ["ext", "extension", "plugin"]):
            return RepositoryType.EXTENSION
        
        # Research repositories
        if any(x in name_lower for x in ["research", "model", "transformer", "neuromorphic"]):
            return RepositoryType.RESEARCH
        
        # Template repositories
        if any(x in name_lower for x in ["template", "starter", "boilerplate"]):
            return RepositoryType.TEMPLATE
        
        return RepositoryType.UNKNOWN
    
    def analyze_architecture_patterns(self) -> Dict[str, Any]:
        """Analyze architecture patterns across all repositories."""
        patterns = {
            "foundation_repos": [],
            "service_repos": [],
            "module_repos": [],
            "platform_repos": [],
            "research_repos": [],
            "extension_repos": [],
            "tool_repos": [],
            "template_repos": []
        }
        
        for key, repo in self.repositories.items():
            repo_type = repo.type.value
            if repo_type in patterns:
                patterns[repo_type].append({
                    "source": repo.source,
                    "name": repo.name,
                    "url": repo.url,
                    "description": repo.description,
                    "private": repo.is_private
                })
        
        return patterns
    
    def identify_convergence_opportunities(self) -> List[Dict[str, Any]]:
        """Identify convergence opportunities across repositories."""
        opportunities = []
        
        # Group by type
        by_type = {}
        for key, repo in self.repositories.items():
            repo_type = repo.type.value
            if repo_type not in by_type:
                by_type[repo_type] = []
            by_type[repo_type].append(repo)
        
        # Identify patterns
        # Foundation convergence
        foundations = [r for r in self.repositories.values() if r.type == RepositoryType.FOUNDATION]
        if len(foundations) > 1:
            opportunities.append({
                "type": "foundation_convergence",
                "repositories": [{"source": r.source, "name": r.name} for r in foundations],
                "value": "Unify foundation architectures"
            })
        
        # Service convergence
        services = [r for r in self.repositories.values() if r.type == RepositoryType.SERVICE]
        if len(services) > 0:
            opportunities.append({
                "type": "service_mesh",
                "repositories": [{"source": r.source, "name": r.name} for r in services],
                "value": "Create service mesh from microservices"
            })
        
        # Research convergence
        research = [r for r in self.repositories.values() if r.type == RepositoryType.RESEARCH]
        if len(research) > 0:
            opportunities.append({
                "type": "research_integration",
                "repositories": [{"source": r.source, "name": r.name} for r in research],
                "value": "Integrate research models into production"
            })
        
        return opportunities
    
    def generate_universal_awareness_map(self) -> Dict[str, Any]:
        """Generate complete universal awareness map."""
        awareness = {
            "timestamp": datetime.utcnow().isoformat(),
            "sources": {},
            "statistics": {
                "total_repositories": len(self.repositories),
                "by_source": {},
                "by_type": {},
                "by_access": {"public": 0, "private": 0}
            },
            "architecture_patterns": self.analyze_architecture_patterns(),
            "convergence_opportunities": self.identify_convergence_opportunities(),
            "repositories": {}
        }
        
        # Organize by source
        for source_id in self.sources.keys():
            source_repos = [r for r in self.repositories.values() if r.source == source_id]
            awareness["sources"][source_id] = {
                "count": len(source_repos),
                "repositories": [
                    {**asdict(r), "type": r.type.value, "access_level": r.access_level.value}
                    for r in source_repos
                ]
            }
            awareness["statistics"]["by_source"][source_id] = len(source_repos)
        
        # Statistics by type
        for repo in self.repositories.values():
            repo_type = repo.type.value
            if repo_type not in awareness["statistics"]["by_type"]:
                awareness["statistics"]["by_type"][repo_type] = 0
            awareness["statistics"]["by_type"][repo_type] += 1
            
            if repo.is_private:
                awareness["statistics"]["by_access"]["private"] += 1
            else:
                awareness["statistics"]["by_access"]["public"] += 1
        
        # Full repository details
        for key, repo in self.repositories.items():
            repo_dict = asdict(repo)
            repo_dict["type"] = repo.type.value
            repo_dict["access_level"] = repo.access_level.value
            awareness["repositories"][key] = repo_dict
        
        self.awareness_map = awareness
        return awareness
    
    def generate_report(self) -> str:
        """Generate human-readable awareness report."""
        report = []
        report.append("# AbëFLOWs Universal Repository Awareness Report")
        report.append("")
        report.append(f"**Generated:** {datetime.utcnow().isoformat()}")
        report.append("")
        report.append("## Epistemic Source Pattern Analysis")
        report.append("")
        report.append("### Statistics")
        report.append(f"- **Total Repositories:** {len(self.repositories)}")
        report.append("")
        
        # By source
        report.append("### By Source")
        for source_id, source_name in self.sources.items():
            count = len([r for r in self.repositories.values() if r.source == source_id])
            report.append(f"- **{source_name}:** {count} repositories")
        report.append("")
        
        # By type
        report.append("### By Type")
        by_type = {}
        for repo in self.repositories.values():
            repo_type = repo.type.value
            if repo_type not in by_type:
                by_type[repo_type] = 0
            by_type[repo_type] += 1
        
        for repo_type, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
            report.append(f"- **{repo_type}:** {count}")
        report.append("")
        
        # Architecture patterns
        report.append("## Architecture Patterns")
        patterns = self.analyze_architecture_patterns()
        for pattern_type, repos in patterns.items():
            if repos:
                report.append(f"### {pattern_type.replace('_', ' ').title()}")
                for repo in repos[:10]:  # Limit to 10 per type
                    privacy = "" if repo["private"] else ""
                    report.append(f"- {privacy} [{repo['name']}]({repo['url']}) - {repo['description'][:100]}")
                if len(repos) > 10:
                    report.append(f"  ... and {len(repos) - 10} more")
                report.append("")
        
        # Convergence opportunities
        report.append("## Convergence Opportunities")
        opportunities = self.identify_convergence_opportunities()
        for opp in opportunities:
            report.append(f"### {opp['type'].replace('_', ' ').title()}")
            report.append(f"**Value:** {opp['value']}")
            report.append("**Repositories:**")
            for repo in opp["repositories"]:
                report.append(f"- {repo['source']}/{repo['name']}")
            report.append("")
        
        # Key repositories
        report.append("## Key Repositories")
        key_repos = [
            r for r in self.repositories.values()
            if r.type in [RepositoryType.FOUNDATION, RepositoryType.PLATFORM] or "abe" in r.name.lower() or "flow" in r.name.lower()
        ]
        
        for repo in sorted(key_repos, key=lambda x: x.name):
            privacy = " Private" if repo.is_private else " Public"
            report.append(f"### {repo.name} ({privacy})")
            report.append(f"- **Source:** {repo.source}")
            report.append(f"- **URL:** {repo.url}")
            report.append(f"- **Type:** {repo.type.value}")
            report.append(f"- **Description:** {repo.description}")
            if repo.language:
                report.append(f"- **Language:** {repo.language}")
            report.append("")
        
        return "\n".join(report)

# Main execution
if __name__ == "__main__":
    print("="*60)
    print("AbëFLOWs Universal Repository Awareness System")
    print("Deep Epistemic Source Pattern - Complete Access")
    print("="*60)
    print()
    
    awareness = UniversalRepositoryAwareness()
    
    # Discover all repositories
    print("Discovering all repositories...")
    all_repos = awareness.discover_all_repositories()
    print(f"\nTotal repositories discovered: {len(awareness.repositories)}")
    
    # Generate awareness map
    print("\nGenerating universal awareness map...")
    awareness_map = awareness.generate_universal_awareness_map()
    
    # Save JSON
    output_json = Path("universal_repository_awareness.json")
    with open(output_json, "w") as f:
        json.dump(awareness_map, f, indent=2)
    print(f"Saved awareness map to: {output_json}")
    
    # Generate report
    print("\nGenerating awareness report...")
    report = awareness.generate_report()
    
    # Save report
    output_report = Path("UNIVERSAL_REPOSITORY_AWARENESS_REPORT.md")
    with open(output_report, "w") as f:
        f.write(report)
    print(f"Saved report to: {output_report}")
    
    # Print summary
    print("\n" + "="*60)
    print("AWARENESS SUMMARY")
    print("="*60)
    print(f"Total Repositories: {len(awareness.repositories)}")
    print(f"By Source:")
    for source_id, source_name in awareness.sources.items():
        count = len([r for r in awareness.repositories.values() if r.source == source_id])
        print(f"  - {source_name}: {count}")
    print(f"\nConvergence Opportunities: {len(awareness_map['convergence_opportunities'])}")
    print("="*60)

