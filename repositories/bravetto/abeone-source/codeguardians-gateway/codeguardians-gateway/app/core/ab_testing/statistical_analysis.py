"""
Statistical Analysis Framework for A/B Testing

Comprehensive statistical analysis including:
- Hypothesis testing (t-test, chi-square)
- Confidence intervals
- Effect size calculation
- Power analysis
- Bayesian analysis
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Conditional imports for scientific computing libraries
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    np = None
    HAS_NUMPY = False

try:
    from scipy import stats
    from scipy.stats import chi2_contingency, ttest_ind, mannwhitneyu
    HAS_SCIPY = True
except ImportError:
    stats = None
    chi2_contingency = None
    ttest_ind = None
    mannwhitneyu = None
    HAS_SCIPY = False

@dataclass
class StatisticalTestResult:
    """Result of statistical test"""
    test_name: str
    statistic: float
    p_value: float
    degrees_of_freedom: Optional[int]
    confidence_interval: Optional[Tuple[float, float]]
    effect_size: Optional[float]
    power: Optional[float]
    is_significant: bool
    interpretation: str

@dataclass
class ExperimentAnalysis:
    """Complete analysis of A/B test experiment"""
    experiment_id: str
    variant_a: str
    variant_b: str
    sample_size_a: int
    sample_size_b: int
    mean_a: float
    mean_b: float
    std_a: float
    std_b: float
    primary_test: StatisticalTestResult
    secondary_tests: List[StatisticalTestResult]
    confidence_interval: Tuple[float, float]
    effect_size: float
    power: float
    is_significant: bool
    recommendation: str
    analysis_timestamp: datetime

class StatisticalAnalyzer:
    """
    Statistical analysis engine for A/B testing.
    
    Provides comprehensive statistical analysis including hypothesis testing,
    confidence intervals, effect size calculation, and power analysis.
    """
    
    def __init__(self, confidence_level: float = 0.95, power: float = 0.8):
        self.confidence_level = confidence_level
        self.power = power
        self.alpha = 1 - confidence_level
    
    def analyze_experiment(
        self,
        experiment_id: str,
        variant_a_data: List[float],
        variant_b_data: List[float],
        variant_a_name: str = "control",
        variant_b_name: str = "treatment",
        metric_type: str = "continuous"
    ) -> ExperimentAnalysis:
        """
        Perform comprehensive statistical analysis of A/B test.
        
        Args:
            experiment_id: Experiment identifier
            variant_a_data: Data for variant A
            variant_b_data: Data for variant B
            variant_a_name: Name of variant A
            variant_b_name: Name of variant B
            metric_type: Type of metric (continuous, binary, count)
            
        Returns:
            Complete experiment analysis
        """
        try:
            if not HAS_NUMPY or not HAS_SCIPY:
                return self._fallback_analysis(experiment_id, variant_a_data, variant_b_data, variant_a_name, variant_b_name)
            
            # Convert to numpy arrays
            data_a = np.array(variant_a_data)
            data_b = np.array(variant_b_data)
            
            # Basic statistics
            mean_a = np.mean(data_a)
            mean_b = np.mean(data_b)
            std_a = np.std(data_a, ddof=1)
            std_b = np.std(data_b, ddof=1)
            
            # Perform primary statistical test
            primary_test = self._perform_primary_test(
                data_a, data_b, variant_a_name, variant_b_name, metric_type
            )
            
            # Perform secondary tests
            secondary_tests = self._perform_secondary_tests(
                data_a, data_b, variant_a_name, variant_b_name, metric_type
            )
            
            # Calculate confidence interval
            confidence_interval = self._calculate_confidence_interval(
                data_a, data_b, primary_test.test_name
            )
            
            # Calculate effect size
            effect_size = self._calculate_effect_size(data_a, data_b, metric_type)
            
            # Calculate power
            power = self._calculate_power(data_a, data_b, effect_size)
            
            # Determine significance
            is_significant = primary_test.p_value < self.alpha
            
            # Generate recommendation
            recommendation = self._generate_recommendation(
                primary_test, effect_size, power, is_significant
            )
            
            return ExperimentAnalysis(
                experiment_id=experiment_id,
                variant_a=variant_a_name,
                variant_b=variant_b_name,
                sample_size_a=len(data_a),
                sample_size_b=len(data_b),
                mean_a=mean_a,
                mean_b=mean_b,
                std_a=std_a,
                std_b=std_b,
                primary_test=primary_test,
                secondary_tests=secondary_tests,
                confidence_interval=confidence_interval,
                effect_size=effect_size,
                power=power,
                is_significant=is_significant,
                recommendation=recommendation,
                analysis_timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error analyzing experiment {experiment_id}: {e}")
            raise
    
    def _fallback_analysis(
        self,
        experiment_id: str,
        variant_a_data: List[float],
        variant_b_data: List[float],
        variant_a_name: str,
        variant_b_name: str
    ) -> ExperimentAnalysis:
        """Fallback analysis when numpy/scipy are not available."""
        try:
            # Calculate basic statistics using pure Python
            mean_a = sum(variant_a_data) / len(variant_a_data) if variant_a_data else 0
            mean_b = sum(variant_b_data) / len(variant_b_data) if variant_b_data else 0
            
            # Calculate standard deviation
            std_a = (sum((x - mean_a) ** 2 for x in variant_a_data) / (len(variant_a_data) - 1)) ** 0.5 if len(variant_a_data) > 1 else 0
            std_b = (sum((x - mean_b) ** 2 for x in variant_b_data) / (len(variant_b_data) - 1)) ** 0.5 if len(variant_b_data) > 1 else 0
            
            # Simple statistical test (no p-value)
            mean_diff = mean_b - mean_a
            pooled_std = ((std_a ** 2 + std_b ** 2) / 2) ** 0.5
            effect_size = mean_diff / pooled_std if pooled_std > 0 else 0
            
            # Simple confidence interval (normal approximation)
            se_diff = (std_a ** 2 / len(variant_a_data) + std_b ** 2 / len(variant_b_data)) ** 0.5
            ci_margin = 1.96 * se_diff  # 95% CI
            
            primary_test = StatisticalTestResult(
                test_name="Basic comparison",
                statistic=abs(mean_diff) / se_diff if se_diff > 0 else 0,
                p_value=None,  # Not available without scipy
                degrees_of_freedom=None,
                confidence_interval=(mean_diff - ci_margin, mean_diff + ci_margin),
                effect_size=effect_size,
                power=None,
                is_significant=False,  # Can't determine without p-value
                interpretation="Analysis limited - install numpy and scipy for detailed statistics"
            )
            
            return ExperimentAnalysis(
                experiment_id=experiment_id,
                variant_a=variant_a_name,
                variant_b=variant_b_name,
                sample_size_a=len(variant_a_data),
                sample_size_b=len(variant_b_data),
                mean_a=mean_a,
                mean_b=mean_b,
                std_a=std_a,
                std_b=std_b,
                primary_test=primary_test,
                secondary_tests=[],
                confidence_interval=(mean_diff - ci_margin, mean_diff + ci_margin),
                effect_size=effect_size,
                power=None,
                is_significant=False,
                recommendation="Install numpy and scipy for comprehensive statistical analysis",
                analysis_timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error in fallback analysis: {e}")
            raise
    
    def _perform_primary_test(
        self,
        data_a,
        data_b,
        variant_a_name: str,
        variant_b_name: str,
        metric_type: str
    ) -> StatisticalTestResult:
        """Perform primary statistical test based on metric type."""
        
        if metric_type == "continuous":
            return self._t_test(data_a, data_b, variant_a_name, variant_b_name)
        elif metric_type == "binary":
            return self._chi_square_test(data_a, data_b, variant_a_name, variant_b_name)
        elif metric_type == "count":
            return self._mann_whitney_test(data_a, data_b, variant_a_name, variant_b_name)
        else:
            # Default to t-test
            return self._t_test(data_a, data_b, variant_a_name, variant_b_name)
    
    def _t_test(
        self,
        data_a,
        data_b,
        variant_a_name: str,
        variant_b_name: str
    ) -> StatisticalTestResult:
        """Perform independent samples t-test."""
        
        try:
            if not HAS_SCIPY:
                # Fallback without scipy
                mean_diff = np.mean(data_b) - np.mean(data_a)
                var_a = np.var(data_a, ddof=1)
                var_b = np.var(data_b, ddof=1)
                n_a = len(data_a)
                n_b = len(data_b)
                
                se_diff = np.sqrt(var_a/n_a + var_b/n_b)
                effect_size = mean_diff / np.sqrt((var_a + var_b) / 2) if (var_a + var_b) > 0 else 0
                
                return StatisticalTestResult(
                    test_name="t-test (approximate)",
                    statistic=abs(mean_diff) / se_diff if se_diff > 0 else 0,
                    p_value=None,
                    degrees_of_freedom=n_a + n_b - 2,
                    confidence_interval=None,
                    effect_size=effect_size,
                    power=None,
                    is_significant=False,
                    interpretation="Statistical test limited without scipy"
                )
            
            # Check assumptions
            if len(data_a) < 2 or len(data_b) < 2:
                raise ValueError("Insufficient data for t-test")
            
            # Perform t-test
            statistic, p_value = ttest_ind(data_a, data_b, equal_var=False)
            
            # Calculate degrees of freedom (Welch's t-test)
            var_a = np.var(data_a, ddof=1)
            var_b = np.var(data_b, ddof=1)
            n_a = len(data_a)
            n_b = len(data_b)
            
            df = (var_a/n_a + var_b/n_b)**2 / ((var_a/n_a)**2/(n_a-1) + (var_b/n_b)**2/(n_b-1))
            
            # Calculate confidence interval
            mean_diff = np.mean(data_b) - np.mean(data_a)
            se_diff = np.sqrt(var_a/n_a + var_b/n_b)
            t_critical = stats.t.ppf(1 - self.alpha/2, df)
            margin_error = t_critical * se_diff
            
            ci_lower = mean_diff - margin_error
            ci_upper = mean_diff + margin_error
            
            # Calculate effect size (Cohen's d)
            pooled_std = np.sqrt(((n_a-1)*var_a + (n_b-1)*var_b) / (n_a + n_b - 2))
            effect_size = mean_diff / pooled_std if pooled_std > 0 else 0
            
            # Calculate power
            power = self._calculate_t_test_power(data_a, data_b, effect_size)
            
            interpretation = self._interpret_t_test_result(p_value, effect_size)
            
            return StatisticalTestResult(
                test_name="Independent Samples t-test",
                statistic=statistic,
                p_value=p_value,
                degrees_of_freedom=df,
                confidence_interval=(ci_lower, ci_upper),
                effect_size=effect_size,
                power=power,
                is_significant=p_value < self.alpha,
                interpretation=interpretation
            )
            
        except Exception as e:
            logger.error(f"Error performing t-test: {e}")
            raise
    
    def _chi_square_test(
        self,
        data_a,
        data_b,
        variant_a_name: str,
        variant_b_name: str
    ) -> StatisticalTestResult:
        """Perform chi-square test for binary metrics."""
        
        try:
            if not HAS_SCIPY:
                # Fallback without scipy
                success_a = sum(data_a)
                failure_a = len(data_a) - success_a
                success_b = sum(data_b)
                failure_b = len(data_b) - success_b
                
                n_total = len(data_a) + len(data_b)
                effect_size = abs(success_a/len(data_a) - success_b/len(data_b))
                
                return StatisticalTestResult(
                    test_name="Chi-square test (approximate)",
                    statistic=effect_size,
                    p_value=None,
                    degrees_of_freedom=1,
                    confidence_interval=None,
                    effect_size=effect_size,
                    power=None,
                    is_significant=False,
                    interpretation="Statistical test limited without scipy"
                )
            
            # Convert to binary outcomes
            success_a = np.sum(data_a)
            failure_a = len(data_a) - success_a
            success_b = np.sum(data_b)
            failure_b = len(data_b) - success_b
            
            # Create contingency table
            contingency_table = np.array([[success_a, failure_a], [success_b, failure_b]])
            
            # Perform chi-square test
            chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)
            
            # Calculate effect size (Cramér's V)
            n_total = np.sum(contingency_table)
            effect_size = np.sqrt(chi2_stat / (n_total * (min(contingency_table.shape) - 1)))
            
            # Calculate power
            power = self._calculate_chi_square_power(contingency_table, effect_size)
            
            interpretation = self._interpret_chi_square_result(p_value, effect_size)
            
            return StatisticalTestResult(
                test_name="Chi-square test",
                statistic=chi2_stat,
                p_value=p_value,
                degrees_of_freedom=dof,
                confidence_interval=None,  # Not applicable for chi-square
                effect_size=effect_size,
                power=power,
                is_significant=p_value < self.alpha,
                interpretation=interpretation
            )
            
        except Exception as e:
            logger.error(f"Error performing chi-square test: {e}")
            raise
    
    def _mann_whitney_test(
        self,
        data_a,
        data_b,
        variant_a_name: str,
        variant_b_name: str
    ) -> StatisticalTestResult:
        """Perform Mann-Whitney U test for non-parametric comparison."""
        
        try:
            if not HAS_SCIPY:
                # Fallback without scipy
                n_a = len(data_a)
                n_b = len(data_b)
                effect_size = abs(np.median(data_b) - np.median(data_a))
                
                return StatisticalTestResult(
                    test_name="Mann-Whitney U test (approximate)",
                    statistic=effect_size,
                    p_value=None,
                    degrees_of_freedom=None,
                    confidence_interval=None,
                    effect_size=effect_size,
                    power=None,
                    is_significant=False,
                    interpretation="Statistical test limited without scipy"
                )
            
            # Perform Mann-Whitney U test
            statistic, p_value = mannwhitneyu(data_a, data_b, alternative='two-sided')
            
            # Calculate effect size (r)
            n_a = len(data_a)
            n_b = len(data_b)
            effect_size = 1 - (2 * statistic) / (n_a * n_b)
            
            # Calculate power (approximate)
            power = self._calculate_mann_whitney_power(data_a, data_b, effect_size)
            
            interpretation = self._interpret_mann_whitney_result(p_value, effect_size)
            
            return StatisticalTestResult(
                test_name="Mann-Whitney U test",
                statistic=statistic,
                p_value=p_value,
                degrees_of_freedom=None,
                confidence_interval=None,  # Not directly applicable
                effect_size=effect_size,
                power=power,
                is_significant=p_value < self.alpha,
                interpretation=interpretation
            )
            
        except Exception as e:
            logger.error(f"Error performing Mann-Whitney test: {e}")
            raise
    
    def _perform_secondary_tests(
        self,
        data_a,
        data_b,
        variant_a_name: str,
        variant_b_name: str,
        metric_type: str
    ) -> List[StatisticalTestResult]:
        """Perform secondary statistical tests."""
        
        secondary_tests = []
        
        try:
            # Always perform Mann-Whitney as secondary test for continuous metrics
            if metric_type == "continuous":
                mann_whitney_result = self._mann_whitney_test(
                    data_a, data_b, variant_a_name, variant_b_name
                )
                secondary_tests.append(mann_whitney_result)
            
            # Add normality tests
            if len(data_a) >= 3:
                normality_a = self._shapiro_wilk_test(data_a, f"{variant_a_name}_normality")
                secondary_tests.append(normality_a)
            
            if len(data_b) >= 3:
                normality_b = self._shapiro_wilk_test(data_b, f"{variant_b_name}_normality")
                secondary_tests.append(normality_b)
            
        except Exception as e:
            logger.error(f"Error performing secondary tests: {e}")
        
        return secondary_tests
    
    def _shapiro_wilk_test(self, data, test_name: str) -> StatisticalTestResult:
        """Perform Shapiro-Wilk test for normality."""
        
        try:
            if not HAS_SCIPY:
                return StatisticalTestResult(
                    test_name=f"Shapiro-Wilk ({test_name})",
                    statistic=0,
                    p_value=1.0,
                    degrees_of_freedom=None,
                    confidence_interval=None,
                    effect_size=None,
                    power=None,
                    is_significant=False,
                    interpretation="Test not available without scipy"
                )
            
            if len(data) < 3 or len(data) > 5000:  # Shapiro-Wilk limitations
                return StatisticalTestResult(
                    test_name=f"Shapiro-Wilk ({test_name})",
                    statistic=0,
                    p_value=1.0,
                    degrees_of_freedom=None,
                    confidence_interval=None,
                    effect_size=None,
                    power=None,
                    is_significant=False,
                    interpretation="Test not applicable due to sample size"
                )
            
            statistic, p_value = stats.shapiro(data)
            
            interpretation = "Data appears normal" if p_value > 0.05 else "Data appears non-normal"
            
            return StatisticalTestResult(
                test_name=f"Shapiro-Wilk ({test_name})",
                statistic=statistic,
                p_value=p_value,
                degrees_of_freedom=None,
                confidence_interval=None,
                effect_size=None,
                power=None,
                is_significant=p_value < 0.05,
                interpretation=interpretation
            )
            
        except Exception as e:
            logger.error(f"Error performing Shapiro-Wilk test: {e}")
            return StatisticalTestResult(
                test_name=f"Shapiro-Wilk ({test_name})",
                statistic=0,
                p_value=1.0,
                degrees_of_freedom=None,
                confidence_interval=None,
                effect_size=None,
                power=None,
                is_significant=False,
                interpretation=f"Test failed: {str(e)}"
            )
    
    def _calculate_confidence_interval(
        self,
        data_a,
        data_b,
        test_name: str
    ) -> Tuple[float, float]:
        """Calculate confidence interval for difference in means."""
        
        try:
            mean_a = np.mean(data_a)
            mean_b = np.mean(data_b)
            var_a = np.var(data_a, ddof=1)
            var_b = np.var(data_b, ddof=1)
            n_a = len(data_a)
            n_b = len(data_b)
            
            # Calculate standard error of difference
            se_diff = np.sqrt(var_a/n_a + var_b/n_b)
            
            # Calculate degrees of freedom (Welch's t-test)
            df = (var_a/n_a + var_b/n_b)**2 / ((var_a/n_a)**2/(n_a-1) + (var_b/n_b)**2/(n_b-1))
            
            # Calculate critical value
            t_critical = stats.t.ppf(1 - self.alpha/2, df)
            
            # Calculate margin of error
            margin_error = t_critical * se_diff
            
            # Calculate confidence interval
            mean_diff = mean_b - mean_a
            ci_lower = mean_diff - margin_error
            ci_upper = mean_diff + margin_error
            
            return (ci_lower, ci_upper)
            
        except Exception as e:
            logger.error(f"Error calculating confidence interval: {e}")
            return (0, 0)
    
    def _calculate_effect_size(self, data_a, data_b, metric_type: str) -> float:
        """Calculate effect size based on metric type."""
        
        try:
            if metric_type == "continuous":
                # Cohen's d
                mean_a = np.mean(data_a)
                mean_b = np.mean(data_b)
                var_a = np.var(data_a, ddof=1)
                var_b = np.var(data_b, ddof=1)
                n_a = len(data_a)
                n_b = len(data_b)
                
                pooled_std = np.sqrt(((n_a-1)*var_a + (n_b-1)*var_b) / (n_a + n_b - 2))
                return (mean_b - mean_a) / pooled_std if pooled_std > 0 else 0
                
            elif metric_type == "binary":
                # Cramér's V
                success_a = np.sum(data_a)
                failure_a = len(data_a) - success_a
                success_b = np.sum(data_b)
                failure_b = len(data_b) - success_b
                
                contingency_table = np.array([[success_a, failure_a], [success_b, failure_b]])
                chi2_stat, _, _, _ = chi2_contingency(contingency_table)
                n_total = np.sum(contingency_table)
                
                return np.sqrt(chi2_stat / (n_total * (min(contingency_table.shape) - 1)))
                
            else:
                # Default to Cohen's d
                return self._calculate_effect_size(data_a, data_b, "continuous")
                
        except Exception as e:
            logger.error(f"Error calculating effect size: {e}")
            return 0
    
    def _calculate_power(self, data_a, data_b, effect_size: float) -> float:
        """Calculate statistical power."""
        
        try:
            n_a = len(data_a)
            n_b = len(data_b)
            
            # Calculate pooled standard deviation
            var_a = np.var(data_a, ddof=1)
            var_b = np.var(data_b, ddof=1)
            pooled_std = np.sqrt(((n_a-1)*var_a + (n_b-1)*var_b) / (n_a + n_b - 2))
            
            # Calculate non-centrality parameter
            ncp = effect_size * np.sqrt(n_a * n_b / (n_a + n_b))
            
            # Calculate degrees of freedom
            df = n_a + n_b - 2
            
            # Calculate power using non-central t-distribution
            t_critical = stats.t.ppf(1 - self.alpha/2, df)
            power = 1 - stats.nct.cdf(t_critical, df, ncp) + stats.nct.cdf(-t_critical, df, ncp)
            
            return max(0, min(1, power))  # Clamp between 0 and 1
            
        except Exception as e:
            logger.error(f"Error calculating power: {e}")
            return 0
    
    def _calculate_t_test_power(self, data_a, data_b, effect_size: float) -> float:
        """Calculate power for t-test."""
        return self._calculate_power(data_a, data_b, effect_size)
    
    def _calculate_chi_square_power(self, contingency_table, effect_size: float) -> float:
        """Calculate power for chi-square test."""
        try:
            n_total = np.sum(contingency_table)
            df = (contingency_table.shape[0] - 1) * (contingency_table.shape[1] - 1)
            
            # Approximate power calculation
            ncp = effect_size**2 * n_total
            chi2_critical = stats.chi2.ppf(1 - self.alpha, df)
            power = 1 - stats.ncx2.cdf(chi2_critical, df, ncp)
            
            return max(0, min(1, power))
        except Exception as e:
            logger.error(f"Error calculating chi-square power: {e}")
            return 0
    
    def _calculate_mann_whitney_power(self, data_a, data_b, effect_size: float) -> float:
        """Calculate approximate power for Mann-Whitney test."""
        try:
            n_a = len(data_a)
            n_b = len(data_b)
            
            # Approximate power using normal approximation
            n_total = n_a + n_b
            se = np.sqrt(n_a * n_b * (n_total + 1) / 12)
            z_effect = effect_size * np.sqrt(n_a * n_b / n_total)
            z_critical = stats.norm.ppf(1 - self.alpha/2)
            
            power = 1 - stats.norm.cdf(z_critical - z_effect) + stats.norm.cdf(-z_critical - z_effect)
            
            return max(0, min(1, power))
        except Exception as e:
            logger.error(f"Error calculating Mann-Whitney power: {e}")
            return 0
    
    def _interpret_t_test_result(self, p_value: float, effect_size: float) -> str:
        """Interpret t-test results."""
        if p_value < self.alpha:
            if abs(effect_size) < 0.2:
                return "Significant difference with small effect size"
            elif abs(effect_size) < 0.5:
                return "Significant difference with medium effect size"
            else:
                return "Significant difference with large effect size"
        else:
            return "No significant difference detected"
    
    def _interpret_chi_square_result(self, p_value: float, effect_size: float) -> str:
        """Interpret chi-square test results."""
        if p_value < self.alpha:
            if effect_size < 0.1:
                return "Significant association with weak effect"
            elif effect_size < 0.3:
                return "Significant association with moderate effect"
            else:
                return "Significant association with strong effect"
        else:
            return "No significant association detected"
    
    def _interpret_mann_whitney_result(self, p_value: float, effect_size: float) -> str:
        """Interpret Mann-Whitney test results."""
        if p_value < self.alpha:
            if abs(effect_size) < 0.1:
                return "Significant difference with small effect size"
            elif abs(effect_size) < 0.3:
                return "Significant difference with medium effect size"
            else:
                return "Significant difference with large effect size"
        else:
            return "No significant difference detected"
    
    def _generate_recommendation(
        self,
        primary_test: StatisticalTestResult,
        effect_size: float,
        power: float,
        is_significant: bool
    ) -> str:
        """Generate recommendation based on analysis results."""
        
        if is_significant:
            if power >= 0.8:
                if abs(effect_size) >= 0.5:
                    return "Strong evidence to implement treatment variant"
                elif abs(effect_size) >= 0.2:
                    return "Moderate evidence to implement treatment variant"
                else:
                    return "Weak evidence to implement treatment variant - consider practical significance"
            else:
                return "Significant result but low power - consider increasing sample size"
        else:
            if power >= 0.8:
                return "No significant difference detected with adequate power - keep control variant"
            else:
                return "Inconclusive result due to low power - consider increasing sample size"
