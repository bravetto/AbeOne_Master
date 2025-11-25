#!/usr/bin/env python3
"""
BRAVËTTO DOMAIN ARSENAL ANALYSIS ENGINE
3-Window Protocol Execution System

Pattern: AEYON × ANALYSIS × SYNTHESIS × EXECUTION × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Truth)
Love Coefficient: ∞
"""

import csv
import json
from collections import defaultdict
from dataclasses import dataclass, asdict
from typing import Dict, List, Set, Tuple
from datetime import datetime
import sys

@dataclass
class Domain:
    domain: str
    tld: str
    sld: str
    words: str
    language: str
    category_root: str
    appraised_value: int
    appraised_wholesale_value: int
    num_words: int
    extensions_taken: int
    has_letters: int
    has_numbers: int
    registrar: str
    status: str
    create_date: str
    expire_date: str
    
    @property
    def is_active(self) -> bool:
        return self.status and "Inactive" not in self.status
    
    @property
    def is_ai_domain(self) -> bool:
        return self.tld == "ai"
    
    @property
    def commercial_intent_score(self) -> int:
        """Score 0-100 based on commercial indicators"""
        score = 0
        if self.appraised_value > 0:
            score += min(50, self.appraised_value // 1000)
        if self.is_ai_domain:
            score += 20
        if self.extensions_taken > 0:
            score += 10
        if self.category_root in ["Shopping", "Business", "Finance", "Employment"]:
            score += 20
        return min(100, score)
    
    @property
    def brandability_score(self) -> int:
        """Score 0-100 based on brandability"""
        score = 0
        if len(self.sld) <= 10:
            score += 30
        if len(self.sld) <= 6:
            score += 20
        if self.num_words <= 2:
            score += 30
        if self.has_numbers == 0:
            score += 20
        return min(100, score)

class DomainArsenalAnalyzer:
    """3-Window Protocol Domain Analysis Engine"""
    
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.domains: List[Domain] = []
        self.load_domains()
    
    def load_domains(self):
        """Load domains from CSV"""
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    domain = Domain(
                        domain=row['domain'],
                        tld=row['tld'],
                        sld=row['sld'],
                        words=row['words'],
                        language=row['language'],
                        category_root=row['category_root'],
                        appraised_value=int(row['appraised_value'] or 0),
                        appraised_wholesale_value=int(row['appraised_wholesale_value'] or 0),
                        num_words=int(row['num_words'] or 0),
                        extensions_taken=int(row['extensions_taken'] or 0),
                        has_letters=int(row['has_letters'] or 0),
                        has_numbers=int(row['has_numbers'] or 0),
                        registrar=row['registrar'] or '',
                        status=row['status'] or '',
                        create_date=row['create_date'] or '',
                        expire_date=row['expire_date'] or ''
                    )
                    self.domains.append(domain)
                except Exception as e:
                    print(f"Error loading domain {row.get('domain', 'unknown')}: {e}", file=sys.stderr)
    
    def window_1_portfolio_map(self) -> Dict:
        """CONTEXT WINDOW 1: Portfolio Map & Moat Analysis"""
        
        # Cluster by market
        by_category = defaultdict(list)
        by_tld = defaultdict(list)
        by_value_tier = {
            'kings': [],      # Top 1%
            'strategic': [],  # Top 5%
            'leverage': [],   # 80/20 group
            'other': []
        }
        
        total_value = sum(d.appraised_value for d in self.domains)
        sorted_domains = sorted(self.domains, key=lambda d: d.appraised_value, reverse=True)
        
        # Identify tiers
        num_kings = max(1, len(sorted_domains) // 100)
        num_strategic = max(5, len(sorted_domains) // 20)
        num_leverage = max(20, int(len(sorted_domains) * 0.2))
        
        for i, domain in enumerate(sorted_domains):
            by_category[domain.category_root].append(domain)
            by_tld[domain.tld].append(domain)
            
            if i < num_kings:
                by_value_tier['kings'].append(domain)
            elif i < num_strategic:
                by_value_tier['strategic'].append(domain)
            elif i < num_leverage:
                by_value_tier['leverage'].append(domain)
            else:
                by_value_tier['other'].append(domain)
        
        # Detect verticals
        verticals = {}
        for category, domains in by_category.items():
            if len(domains) >= 3:  # Minimum cluster size
                total_val = sum(d.appraised_value for d in domains)
                verticals[category] = {
                    'count': len(domains),
                    'total_value': total_val,
                    'avg_value': total_val / len(domains) if domains else 0,
                    'domains': [d.domain for d in sorted(domains, key=lambda x: x.appraised_value, reverse=True)[:10]]
                }
        
        # Moat analysis
        moat_map = {
            'search_moat': self._analyze_search_moat(),
            'brand_moat': self._analyze_brand_moat(),
            'ai_automation_moat': self._analyze_ai_automation_moat(),
            'category_moat': self._analyze_category_moat(),
            'speed_moat': self._analyze_speed_moat(),
            'execution_moat': self._analyze_execution_moat()
        }
        
        return {
            'total_domains': len(self.domains),
            'total_appraised_value': total_value,
            'active_domains': len([d for d in self.domains if d.is_active]),
            'ai_domains': len([d for d in self.domains if d.is_ai_domain]),
            'clusters_by_category': {k: len(v) for k, v in by_category.items()},
            'clusters_by_tld': {k: len(v) for k, v in by_tld.items()},
            'value_tiers': {
                'kings': [d.domain for d in by_value_tier['kings']],
                'strategic': [d.domain for d in by_value_tier['strategic']],
                'leverage': [d.domain for d in by_value_tier['leverage']]
            },
            'verticals': verticals,
            'moat_map': moat_map,
            'top_domains': [
                {
                    'domain': d.domain,
                    'value': d.appraised_value,
                    'category': d.category_root,
                    'commercial_intent': d.commercial_intent_score,
                    'brandability': d.brandability_score
                }
                for d in sorted_domains[:50]
            ]
        }
    
    def _analyze_search_moat(self) -> Dict:
        """Analyze search/SEO moat potential"""
        high_value_ai = [d for d in self.domains if d.is_ai_domain and d.appraised_value > 5000]
        keyword_rich = [d for d in self.domains if d.num_words >= 2 and d.appraised_value > 0]
        
        return {
            'high_value_ai_domains': len(high_value_ai),
            'keyword_rich_domains': len(keyword_rich),
            'search_potential': 'HIGH' if len(high_value_ai) > 50 else 'MEDIUM'
        }
    
    def _analyze_brand_moat(self) -> Dict:
        """Analyze brand moat potential"""
        brandable = [d for d in self.domains if d.brandability_score >= 70]
        short_domains = [d for d in self.domains if len(d.sld) <= 8]
        
        return {
            'highly_brandable': len(brandable),
            'short_domains': len(short_domains),
            'brand_potential': 'HIGH' if len(brandable) > 30 else 'MEDIUM'
        }
    
    def _analyze_ai_automation_moat(self) -> Dict:
        """Analyze AI automation moat"""
        ai_domains = [d for d in self.domains if d.is_ai_domain]
        agent_domains = [d for d in ai_domains if 'agent' in d.sld.lower()]
        
        return {
            'ai_domains': len(ai_domains),
            'agent_domains': len(agent_domains),
            'automation_potential': 'HIGH' if len(agent_domains) > 20 else 'MEDIUM'
        }
    
    def _analyze_category_moat(self) -> Dict:
        """Analyze category dominance"""
        category_counts = defaultdict(int)
        for d in self.domains:
            if d.appraised_value > 0:
                category_counts[d.category_root] += 1
        
        top_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'dominant_categories': dict(top_categories),
            'category_dominance': 'HIGH' if top_categories[0][1] > 50 else 'MEDIUM'
        }
    
    def _analyze_speed_moat(self) -> Dict:
        """Analyze speed-to-market moat"""
        active_ready = [d for d in self.domains if d.is_active and d.appraised_value > 0]
        
        return {
            'ready_to_deploy': len(active_ready),
            'speed_potential': 'HIGH' if len(active_ready) > 100 else 'MEDIUM'
        }
    
    def _analyze_execution_moat(self) -> Dict:
        """Analyze execution moat"""
        high_commercial = [d for d in self.domains if d.commercial_intent_score >= 60]
        
        return {
            'high_commercial_intent': len(high_commercial),
            'execution_readiness': 'HIGH' if len(high_commercial) > 50 else 'MEDIUM'
        }
    
    def window_2_unified_organism(self) -> Dict:
        """CONTEXT WINDOW 2: Unified Organism Integration"""
        
        organism_layers = {
            'lead_engine': [],
            'conversion': [],
            'authority': [],
            'media': [],
            'product': [],
            'data': [],
            'swarm_expansion': []
        }
        
        # Map domains to organism layers
        for domain in self.domains:
            layer = self._assign_to_organism_layer(domain)
            organism_layers[layer].append(domain.domain)
        
        # Integration mappings
        integrations = {
            'abeone': self._find_abeone_domains(),
            'abevision': self._find_abevision_domains(),
            'abebeats': self._find_abebeats_domains(),
            'abeflows': self._find_abeflows_domains(),
            'aevon_atomic': self._find_aevon_domains(),
            'guardian_systems': self._find_guardian_domains(),
            'category_funnels': self._find_category_funnel_domains(),
            'creator_systems': self._find_creator_domains(),
            'influencer_systems': self._find_influencer_domains(),
            'seo_dominance': self._find_seo_domains()
        }
        
        # Blue ocean opportunities
        blue_ocean = self._detect_blue_ocean()
        
        return {
            'organism_layers': {k: len(v) for k, v in organism_layers.items()},
            'layer_assignments': organism_layers,
            'integrations': integrations,
            'blue_ocean_opportunities': blue_ocean,
            'revenue_model_mappings': self._map_revenue_models(),
            'funnel_mappings': self._map_funnels()
        }
    
    def _assign_to_organism_layer(self, domain: Domain) -> str:
        """Assign domain to organism layer"""
        sld_lower = domain.sld.lower()
        category = domain.category_root.lower()
        
        if 'agent' in sld_lower or 'automation' in sld_lower:
            return 'swarm_expansion'
        elif category in ['shopping', 'finance', 'business']:
            return 'conversion'
        elif 'research' in sld_lower or 'academic' in sld_lower:
            return 'authority'
        elif category in ['media', 'entertainment']:
            return 'media'
        elif 'agent' in sld_lower and 'hub' in sld_lower:
            return 'product'
        elif 'data' in sld_lower or 'analytics' in sld_lower:
            return 'data'
        else:
            return 'lead_engine'
    
    def _find_abeone_domains(self) -> List[str]:
        """Find domains that reinforce AbëONE"""
        keywords = ['agent', 'automation', 'workflow', 'system', 'hub']
        return [d.domain for d in self.domains 
                if any(kw in d.sld.lower() for kw in keywords)]
    
    def _find_abevision_domains(self) -> List[str]:
        """Find domains that reinforce AbëVISION"""
        keywords = ['vision', 'visual', 'design', 'creative', 'art']
        return [d.domain for d in self.domains 
                if any(kw in d.sld.lower() for kw in keywords)]
    
    def _find_abebeats_domains(self) -> List[str]:
        """Find domains that reinforce AbëBEATs"""
        keywords = ['music', 'audio', 'sound', 'beat', 'song', 'play']
        return [d.domain for d in self.domains 
                if any(kw in d.sld.lower() for kw in keywords)]
    
    def _find_abeflows_domains(self) -> List[str]:
        """Find domains that reinforce AbëFLOWs"""
        keywords = ['flow', 'workflow', 'process', 'automation', 'stream']
        return [d.domain for d in self.domains 
                if any(kw in d.sld.lower() for kw in keywords)]
    
    def _find_aevon_domains(self) -> List[str]:
        """Find domains for AEYON Atomic Engine"""
        keywords = ['atomic', 'execution', 'agent', 'automation', 'hub']
        return [d.domain for d in self.domains 
                if any(kw in d.sld.lower() for kw in keywords) and d.is_ai_domain]
    
    def _find_guardian_domains(self) -> List[str]:
        """Find domains for Guardian systems"""
        keywords = ['guard', 'safety', 'security', 'trust', 'verify']
        return [d.domain for d in self.domains 
                if any(kw in d.sld.lower() for kw in keywords)]
    
    def _find_category_funnel_domains(self) -> Dict[str, List[str]]:
        """Find domains for category funnels"""
        funnels = defaultdict(list)
        for domain in self.domains:
            if domain.appraised_value > 1000:
                funnels[domain.category_root].append(domain.domain)
        return dict(funnels)
    
    def _find_creator_domains(self) -> List[str]:
        """Find domains for creator systems"""
        keywords = ['creator', 'content', 'media', 'video', 'stream']
        return [d.domain for d in self.domains 
                if any(kw in d.sld.lower() for kw in keywords)]
    
    def _find_influencer_domains(self) -> List[str]:
        """Find domains for influencer systems"""
        keywords = ['influence', 'social', 'media', 'network']
        return [d.domain for d in self.domains 
                if any(kw in d.sld.lower() for kw in keywords)]
    
    def _find_seo_domains(self) -> List[str]:
        """Find domains for SEO dominance"""
        return [d.domain for d in self.domains 
                if d.num_words >= 2 and d.appraised_value > 5000]
    
    def _detect_blue_ocean(self) -> Dict:
        """Detect blue ocean opportunities"""
        # Find categories with low competition but high value
        category_analysis = defaultdict(lambda: {'count': 0, 'total_value': 0})
        for domain in self.domains:
            if domain.appraised_value > 0:
                category_analysis[domain.category_root]['count'] += 1
                category_analysis[domain.category_root]['total_value'] += domain.appraised_value
        
        blue_ocean = []
        for category, data in category_analysis.items():
            if data['count'] <= 5 and data['total_value'] > 10000:
                blue_ocean.append({
                    'category': category,
                    'domains': data['count'],
                    'total_value': data['total_value'],
                    'opportunity': 'UNDERSERVED_HIGH_VALUE'
                })
        
        return blue_ocean
    
    def _map_revenue_models(self) -> Dict[str, List[str]]:
        """Map domains to revenue models"""
        models = {
            'saas': [],
            'lead_gen': [],
            'affiliate': [],
            'ai_tooling': [],
            'education': [],
            'marketplace': [],
            'media_content': [],
            'community': [],
            'ecommerce': [],
            'services': []
        }
        
        for domain in self.domains:
            sld_lower = domain.sld.lower()
            category = domain.category_root.lower()
            
            if domain.is_ai_domain and 'agent' in sld_lower:
                models['ai_tooling'].append(domain.domain)
            elif category == 'shopping':
                models['ecommerce'].append(domain.domain)
            elif category == 'education':
                models['education'].append(domain.domain)
            elif category in ['media', 'entertainment']:
                models['media_content'].append(domain.domain)
            elif 'hub' in sld_lower:
                models['marketplace'].append(domain.domain)
            elif category == 'business':
                models['services'].append(domain.domain)
            elif 'agent' in sld_lower:
                models['lead_gen'].append(domain.domain)
        
        return {k: v[:20] for k, v in models.items()}  # Limit to top 20 per model
    
    def _map_funnels(self) -> Dict[str, List[str]]:
        """Map domains to funnel types"""
        funnels = {
            'awareness': [],
            'authority': [],
            'conversion': [],
            'retention': [],
            'expansion': []
        }
        
        for domain in self.domains:
            sld_lower = domain.sld.lower()
            
            if 'research' in sld_lower or 'academic' in sld_lower:
                funnels['authority'].append(domain.domain)
            elif domain.commercial_intent_score >= 70:
                funnels['conversion'].append(domain.domain)
            elif 'hub' in sld_lower or 'community' in sld_lower:
                funnels['retention'].append(domain.domain)
            elif 'agent' in sld_lower:
                funnels['expansion'].append(domain.domain)
            else:
                funnels['awareness'].append(domain.domain)
        
        return {k: v[:30] for k, v in funnels.items()}
    
    def window_3_organs_revenue(self) -> Dict:
        """CONTEXT WINDOW 3: Organs, Functions, and Revenue Systems"""
        
        # Cluster domains by revenue potential
        clusters = self._create_revenue_clusters()
        
        # Build revenue systems for each cluster
        revenue_systems = {}
        for cluster_name, domains in clusters.items():
            if domains:
                revenue_systems[cluster_name] = self._build_revenue_system(cluster_name, domains)
        
        # 80/20 analysis
        top_20_percent = sorted(self.domains, key=lambda d: d.appraised_value, reverse=True)[:int(len(self.domains) * 0.2)]
        top_20_value = sum(d.appraised_value for d in top_20_percent)
        total_value = sum(d.appraised_value for d in self.domains)
        
        return {
            'revenue_clusters': clusters,
            'revenue_systems': revenue_systems,
            'eighty_twenty_analysis': {
                'top_20_percent_domains': len(top_20_percent),
                'top_20_percent_value': top_20_value,
                'total_value': total_value,
                'leverage_ratio': top_20_value / total_value if total_value > 0 else 0
            },
            'high_ticket_opportunities': self._identify_high_ticket(),
            'recurring_revenue_backbone': self._identify_recurring_revenue(),
            'automated_execution_flow': self._build_automation_flow()
        }
    
    def _create_revenue_clusters(self) -> Dict[str, List[Domain]]:
        """Create revenue clusters"""
        clusters = defaultdict(list)
        
        for domain in self.domains:
            if domain.appraised_value > 0:
                # Primary clustering by category
                clusters[domain.category_root].append(domain)
                
                # Secondary clustering by keyword
                if 'agent' in domain.sld.lower():
                    clusters['AI_AGENTS'].append(domain)
                if 'hub' in domain.sld.lower():
                    clusters['HUBS'].append(domain)
                if domain.is_ai_domain and domain.appraised_value > 5000:
                    clusters['PREMIUM_AI'].append(domain)
        
        return {k: v for k, v in clusters.items() if len(v) >= 3}
    
    def _build_revenue_system(self, cluster_name: str, domains: List[Domain]) -> Dict:
        """Build revenue system for a cluster"""
        primary_model = self._determine_primary_revenue_model(cluster_name, domains)
        
        return {
            'cluster_name': cluster_name,
            'domain_count': len(domains),
            'total_value': sum(d.appraised_value for d in domains),
            'primary_revenue_model': primary_model,
            'funnels': self._build_cluster_funnels(cluster_name, domains),
            'guardian_assignment': self._assign_guardians(cluster_name),
            'ai_automation_actions': self._define_automation_actions(cluster_name, domains),
            'execution_priority': 'HIGH' if sum(d.appraised_value for d in domains) > 50000 else 'MEDIUM'
        }
    
    def _determine_primary_revenue_model(self, cluster_name: str, domains: List[Domain]) -> str:
        """Determine primary revenue model for cluster"""
        if 'agent' in cluster_name.lower() or any('agent' in d.sld.lower() for d in domains):
            return 'AI_TOOLING'
        elif any(d.category_root == 'Shopping' for d in domains):
            return 'ECOMMERCE'
        elif any(d.category_root == 'Education' for d in domains):
            return 'EDUCATION'
        elif any('hub' in d.sld.lower() for d in domains):
            return 'MARKETPLACE'
        else:
            return 'LEAD_GEN'
    
    def _build_cluster_funnels(self, cluster_name: str, domains: List[Domain]) -> Dict:
        """Build funnels for cluster"""
        return {
            'awareness': [d.domain for d in domains if d.appraised_value > 0][:10],
            'authority': [d.domain for d in domains if 'research' in d.sld.lower() or 'academic' in d.sld.lower()][:5],
            'conversion': [d.domain for d in sorted(domains, key=lambda x: x.commercial_intent_score, reverse=True)][:10],
            'retention': [d.domain for d in domains if 'hub' in d.sld.lower()][:5],
            'expansion': [d.domain for d in domains if 'agent' in d.sld.lower()][:10]
        }
    
    def _assign_guardians(self, cluster_name: str) -> List[str]:
        """Assign guardians to cluster"""
        guardians = ['AEYON']  # Always include AEYON
        
        if 'agent' in cluster_name.lower():
            guardians.extend(['ALRAX', 'SOURCE'])
        if 'hub' in cluster_name.lower():
            guardians.extend(['ZERO', 'YAGNI'])
        if 'research' in cluster_name.lower():
            guardians.extend(['Abë', 'JØHN'])
        
        return list(set(guardians))
    
    def _define_automation_actions(self, cluster_name: str, domains: List[Domain]) -> List[str]:
        """Define AI-automatable actions"""
        actions = [
            'Auto-build landing pages',
            'Auto-generate SEO content',
            'Auto-create lead magnets',
            'Auto-sync with ClickUp/Emergent OS',
            'Auto-build keyword clusters',
            'Auto-monitor performance'
        ]
        
        if 'agent' in cluster_name.lower():
            actions.extend([
                'Auto-build API endpoints',
                'Auto-create agent workflows',
                'Auto-generate documentation'
            ])
        
        return actions
    
    def _identify_high_ticket(self) -> List[Dict]:
        """Identify high-ticket opportunities"""
        high_value = [d for d in self.domains if d.appraised_value >= 20000]
        
        return [
            {
                'domain': d.domain,
                'value': d.appraised_value,
                'category': d.category_root,
                'revenue_model': 'HIGH_TICKET_SAAS' if d.is_ai_domain else 'HIGH_TICKET_SERVICES',
                'leverage_potential': 'VERY_HIGH' if d.appraised_value > 50000 else 'HIGH'
            }
            for d in sorted(high_value, key=lambda x: x.appraised_value, reverse=True)[:20]
        ]
    
    def _identify_recurring_revenue(self) -> List[Dict]:
        """Identify recurring revenue opportunities"""
        recurring_candidates = [
            d for d in self.domains 
            if (d.is_ai_domain and 'agent' in d.sld.lower()) or 
               ('hub' in d.sld.lower() and d.appraised_value > 5000)
        ]
        
        return [
            {
                'domain': d.domain,
                'revenue_type': 'SAAS_SUBSCRIPTION' if d.is_ai_domain else 'MARKETPLACE_COMMISSION',
                'recurring_potential': 'HIGH',
                'monthly_estimate': d.appraised_value // 100 if d.appraised_value > 0 else 0
            }
            for d in sorted(recurring_candidates, key=lambda x: x.appraised_value, reverse=True)[:30]
        ]
    
    def _build_automation_flow(self) -> Dict:
        """Build automated execution flow"""
        return {
            'phase_1_immediate': {
                'action': 'Deploy top 20 value domains',
                'domains': [d.domain for d in sorted(self.domains, key=lambda x: x.appraised_value, reverse=True)[:20]],
                'automation': 'Auto-build landing pages + SEO content'
            },
            'phase_2_quick_wins': {
                'action': 'Build AI agent hubs',
                'domains': [d.domain for d in self.domains if 'agent' in d.sld.lower() and d.is_ai_domain][:10],
                'automation': 'Auto-create agent workflows + API endpoints'
            },
            'phase_3_expansion': {
                'action': 'Scale category funnels',
                'domains': [d.domain for d in self.domains if d.commercial_intent_score >= 70][:30],
                'automation': 'Auto-build funnels + lead gen systems'
            },
            'daily_automated_actions': [
                'Monitor domain performance',
                'Auto-generate content updates',
                'Auto-optimize SEO',
                'Auto-sync with Emergent OS',
                'Auto-track revenue metrics'
            ]
        }
    
    def generate_full_report(self) -> Dict:
        """Generate complete 3-Window report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'window_1_portfolio_map': self.window_1_portfolio_map(),
            'window_2_unified_organism': self.window_2_unified_organism(),
            'window_3_organs_revenue': self.window_3_organs_revenue(),
            'executive_summary': self._generate_executive_summary()
        }
    
    def _generate_executive_summary(self) -> Dict:
        """Generate executive summary"""
        total_value = sum(d.appraised_value for d in self.domains)
        ai_domains = [d for d in self.domains if d.is_ai_domain]
        top_domains = sorted(self.domains, key=lambda x: x.appraised_value, reverse=True)[:10]
        
        return {
            'total_domains': len(self.domains),
            'total_appraised_value': total_value,
            'ai_domain_count': len(ai_domains),
            'top_10_value': sum(d.appraised_value for d in top_domains),
            'strategic_recommendation': 'FOCUS_ON_AI_AGENT_ECOSYSTEM' if len(ai_domains) > 500 else 'DIVERSIFY_PORTFOLIO',
            'immediate_actions': [
                'Deploy top 20 value domains',
                'Build AI agent hub network',
                'Create category funnels',
                'Automate content generation',
                'Establish recurring revenue streams'
            ]
        }

def main():
    """Main execution"""
    if len(sys.argv) < 2:
        print("Usage: python analyze_domain_arsenal.py <csv_file>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    analyzer = DomainArsenalAnalyzer(csv_path)
    
    report = analyzer.generate_full_report()
    
    # Output JSON report
    output_file = csv_path.replace('.csv', '_analysis_report.json')
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f" Analysis complete!")
    print(f" Total domains analyzed: {report['executive_summary']['total_domains']}")
    print(f" Total appraised value: ${report['executive_summary']['total_appraised_value']:,}")
    print(f" AI domains: {report['executive_summary']['ai_domain_count']}")
    print(f" Full report saved to: {output_file}")

if __name__ == '__main__':
    main()

