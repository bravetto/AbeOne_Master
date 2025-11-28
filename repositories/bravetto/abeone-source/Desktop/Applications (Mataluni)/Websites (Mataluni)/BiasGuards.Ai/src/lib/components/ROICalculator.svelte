<script lang="ts">
	import { onMount } from 'svelte';
	import { gsap } from 'gsap';
	import { BiasGuardAnimations, NumberAnimations } from '$lib/utils/animations';

	// JAHmere Webb Crisis Context & Industry Data
	const CRISIS_CONTEXT = {
		jahmereCost: 26500,
		industryAvgLawsuit: 847000,
		manualDetectionTime: 156,
		biasGuardTime: 0.5,
		calculatedROI: 44579
	} as const;

	const INDUSTRY_DATA = {
		Healthcare: { riskMultiplier: 1.8, avgTeamSize: 45, complianceWeight: 2.1 },
		Financial: { riskMultiplier: 2.2, avgTeamSize: 38, complianceWeight: 2.5 },
		Legal: { riskMultiplier: 3.1, avgTeamSize: 22, complianceWeight: 3.0 },
		Technology: { riskMultiplier: 1.4, avgTeamSize: 67, complianceWeight: 1.6 }
	} as const;

	const PRICING_TIERS = {
		Starter: { monthly: 19, maxTeam: 5, features: ['Basic Detection', 'Email Support'] },
		Professional: { monthly: 99, maxTeam: 25, features: ['Advanced Analytics', 'Priority Support', 'Custom Rules'] },
		Enterprise: { monthly: 299, maxTeam: 100, features: ['Full Suite', 'Dedicated Support', 'Custom Integration'] }
	} as const;

	// Reactive State (Svelte 5 Runes)
	let selectedIndustry = $state<keyof typeof INDUSTRY_DATA>('Healthcare');
	let teamSize = $state(25);
	let riskTolerance = $state<'Conservative' | 'Moderate' | 'Aggressive'>('Moderate');
	let selectedTier = $state<keyof typeof PRICING_TIERS>('Professional');
	let showComparison = $state(false);
	let animationComplete = $state(false);

	// Component refs
	let calculatorSection: HTMLElement;
	let roiDisplay: HTMLElement;
	let savingsCounter: HTMLElement;
	let speedRacing: HTMLElement;
	let riskMeter: HTMLElement;
	let animations: BiasGuardAnimations;

	// Calculated Values (Derived State)
	const riskMultiplier = $derived(() => INDUSTRY_DATA[selectedIndustry].riskMultiplier);
	const complianceWeight = $derived(() => INDUSTRY_DATA[selectedIndustry].complianceWeight);
	
	const potentialLawsuitCost = $derived(() => {
		const base = CRISIS_CONTEXT.industryAvgLawsuit;
		const industryRisk = riskMultiplier();
		const teamRisk = Math.log(teamSize + 1) * 0.3;
		const toleranceMultiplier = riskTolerance === 'Conservative' ? 0.7 : riskTolerance === 'Moderate' ? 1.0 : 1.4;
		
		return Math.floor(base * industryRisk * (1 + teamRisk) * toleranceMultiplier);
	});

	const annualProtectionCost = $derived(() => {
		return PRICING_TIERS[selectedTier].monthly * 12;
	});

	const calculatedROI = $derived(() => {
		const savings = potentialLawsuitCost() - annualProtectionCost();
		const roi = (savings / annualProtectionCost()) * 100;
		return Math.floor(Math.min(roi, 99999)); // Cap for display
	});

	const timeSavingsPerIncident = $derived(() => {
		return CRISIS_CONTEXT.manualDetectionTime - CRISIS_CONTEXT.biasGuardTime;
	});

	const annualTimeSavings = $derived(() => {
		// Estimate incidents per year based on team size and industry risk
		const estimatedIncidents = Math.ceil((teamSize * riskMultiplier()) / 12);
		return timeSavingsPerIncident() * estimatedIncidents;
	});

	const riskLevel = $derived(() => {
		if (calculatedROI() > 10000) return { level: 'CRITICAL', color: 'text-red-600', bgColor: 'bg-red-50' };
		if (calculatedROI() > 5000) return { level: 'HIGH', color: 'text-orange-600', bgColor: 'bg-orange-50' };
		if (calculatedROI() > 1000) return { level: 'MODERATE', color: 'text-yellow-600', bgColor: 'bg-yellow-50' };
		return { level: 'LOW', color: 'text-green-600', bgColor: 'bg-green-50' };
	});

	// Animation Functions
	function animateROIReveal() {
		if (!roiDisplay || !animationComplete) return;

		// Dramatic entrance
		gsap.fromTo(roiDisplay, 
			{ scale: 0, rotation: -180, opacity: 0 },
			{ scale: 1, rotation: 0, opacity: 1, duration: 0.8, ease: 'back.out(1.7)' }
		);

		// Number counting with particle explosion for high ROI
		NumberAnimations.animateCounter(
			roiDisplay.querySelector('.roi-number') as HTMLElement,
			0,
			calculatedROI(),
			2.5,
			(value) => `${value.toLocaleString()}%`
		);

		// Particle explosion for high ROI
		if (calculatedROI() > 5000) {
			animations.createParticleBackground(roiDisplay, 15);
		}
	}

	function animateSpeedRacing() {
		if (!speedRacing) return;

		const manualBar = speedRacing.querySelector('.manual-bar') as HTMLElement;
		const biasGuardBar = speedRacing.querySelector('.biasguard-bar') as HTMLElement;

		// Racing animation
		const tl = gsap.timeline();
		
		tl.to(manualBar, {
			width: '100%',
			duration: 3,
			ease: 'power2.out'
		})
		.to(biasGuardBar, {
			width: '100%',
			duration: 0.1,
			ease: 'power2.out'
		}, '-=2.9');
	}

	function animateSavingsCounter() {
		if (!savingsCounter) return;

		const counter = savingsCounter.querySelector('.savings-amount') as HTMLElement;
		
		NumberAnimations.animateCounter(
			counter,
			CRISIS_CONTEXT.jahmereCost,
			potentialLawsuitCost() - annualProtectionCost(),
			2.0,
			(value) => `$${value.toLocaleString()}`
		);

		// Pulsing effect for dramatic impact
		gsap.to(savingsCounter, {
			scale: 1.05,
			duration: 1.5,
			yoyo: true,
			repeat: -1,
			ease: 'power2.inOut'
		});
	}

	function animateRiskMeter() {
		if (!riskMeter) return;

		const needle = riskMeter.querySelector('.risk-needle') as HTMLElement;
		const riskPercent = Math.min((calculatedROI() / 20000) * 100, 100);
		
		gsap.to(needle, {
			rotation: (riskPercent * 1.8) - 90, // -90 to 90 degrees
			duration: 1.5,
			ease: 'power2.out'
		});
	}

	function triggerFullAnimation() {
		animationComplete = true;
		
		setTimeout(() => animateROIReveal(), 100);
		setTimeout(() => animateSpeedRacing(), 300);
		setTimeout(() => animateSavingsCounter(), 600);
		setTimeout(() => animateRiskMeter(), 900);
	}

	// Event Handlers
	function handleIndustryChange(event: Event) {
		const target = event.target as HTMLSelectElement;
		selectedIndustry = target.value as keyof typeof INDUSTRY_DATA;
		triggerFullAnimation();
	}

	function handleTeamSizeChange(event: Event) {
		const target = event.target as HTMLInputElement;
		teamSize = parseInt(target.value);
		triggerFullAnimation();
	}

	function handleRiskToleranceChange(tolerance: typeof riskTolerance) {
		riskTolerance = tolerance;
		triggerFullAnimation();
	}

	function handleTierChange(tier: keyof typeof PRICING_TIERS) {
		selectedTier = tier;
		triggerFullAnimation();
	}

	function toggleComparison() {
		showComparison = !showComparison;
		
		if (showComparison) {
			gsap.fromTo('.comparison-panel',
				{ x: '100%', opacity: 0 },
				{ x: '0%', opacity: 1, duration: 0.6, ease: 'power2.out' }
			);
		}
	}

	// Lifecycle
	onMount(() => {
		if (!calculatorSection) return;

		animations = new BiasGuardAnimations();
		
		// Initial entrance animation
		animations.animateHeroEntrance(calculatorSection);
		
		// Trigger initial calculation animation
		setTimeout(() => triggerFullAnimation(), 1000);

		return () => animations?.destroy();
	});
</script>

<section
	bind:this={calculatorSection}
	class="py-20 bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-gray-900 dark:via-blue-900 dark:to-indigo-900 relative overflow-hidden"
	id="roi-calculator"
>
	<!-- Crisis Context Header -->
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-12">
		<div class="text-center mb-8">
			<div class="inline-flex items-center gap-2 bg-red-100 dark:bg-red-900/30 px-4 py-2 rounded-full text-red-700 dark:text-red-300 font-semibold mb-4 hero-alert">
				 <span>REAL CRISIS: JAHmere Webb faces $26,500 legal costs</span>
			</div>
			
			<h2 class="text-4xl sm:text-5xl font-bold text-gray-900 dark:text-white mb-4 hero-title">
				ROI Calculator
				<span class="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
					Business Impact
				</span>
			</h2>
			
			<p class="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto hero-subtitle">
				Calculate your potential savings and ROI with BiasGuard protection. 
				<strong>Industry average lawsuit cost: $847,000</strong>
			</p>
		</div>
	</div>

	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
		<div class="grid lg:grid-cols-2 gap-12 items-start">
			
			<!-- Interactive Calculator Controls -->
			<div class="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-xl hero-cta">
				<h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">
					Configure Your Business
				</h3>

				<!-- Industry Selection -->
				<div class="mb-6">
					<label for="industry" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
						Industry Sector
					</label>
					<select
						id="industry"
						bind:value={selectedIndustry}
						on:change={handleIndustryChange}
						class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
					>
						{#each Object.keys(INDUSTRY_DATA) as industry}
							<option value={industry}>{industry}</option>
						{/each}
					</select>
					<p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
						Risk multiplier: {riskMultiplier()}x
					</p>
				</div>

				<!-- Team Size Slider -->
				<div class="mb-6">
					<label for="team-size" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
						Development Team Size: <span class="font-bold text-blue-600">{teamSize}</span>
					</label>
					<input
						id="team-size"
						type="range"
						min="1"
						max="100"
						bind:value={teamSize}
						on:input={handleTeamSizeChange}
						class="w-full h-2 bg-gray-200 dark:bg-gray-600 rounded-lg appearance-none cursor-pointer slider"
					/>
					<div class="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
						<span>1</span>
						<span>50</span>
						<span>100+</span>
					</div>
				</div>

				<!-- Risk Tolerance -->
				<div class="mb-6">
					<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
						Risk Tolerance
					</label>
					<div class="grid grid-cols-3 gap-2">
						{#each ['Conservative', 'Moderate', 'Aggressive'] as tolerance}
							<button
								type="button"
								on:click={() => handleRiskToleranceChange(tolerance as typeof riskTolerance)}
								class="px-4 py-2 rounded-lg text-sm font-medium transition-all {riskTolerance === tolerance 
									? 'bg-blue-600 text-white shadow-lg' 
									: 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'}"
							>
								{tolerance}
							</button>
						{/each}
					</div>
				</div>

				<!-- Pricing Tier Selection -->
				<div class="mb-8">
					<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
						BiasGuard Plan
					</label>
					<div class="space-y-3">
						{#each Object.entries(PRICING_TIERS) as [tier, details]}
							<button
								type="button"
								on:click={() => handleTierChange(tier as keyof typeof PRICING_TIERS)}
								class="w-full p-4 rounded-lg border-2 text-left transition-all {selectedTier === tier
									? 'border-blue-500 bg-blue-50 dark:bg-blue-900/30'
									: 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'}"
							>
								<div class="flex justify-between items-center">
									<div>
										<h4 class="font-semibold text-gray-900 dark:text-white">{tier}</h4>
										<p class="text-sm text-gray-600 dark:text-gray-400">
											Up to {details.maxTeam} team members
										</p>
									</div>
									<div class="text-right">
										<p class="text-2xl font-bold text-blue-600">${details.monthly}</p>
										<p class="text-sm text-gray-500">per month</p>
									</div>
								</div>
							</button>
						{/each}
					</div>
				</div>

				<!-- Comparison Toggle -->
				<button
					type="button"
					on:click={toggleComparison}
					class="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 transition-all transform hover:scale-105 cta-button"
				>
					{showComparison ? 'Hide' : 'Show'} Scenario Comparison
				</button>
			</div>

			<!-- Results Dashboard -->
			<div class="space-y-6">
				
				<!-- ROI Display -->
				<div bind:this={roiDisplay} class="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-xl text-center {riskLevel().bgColor} hero-stats">
					<div class="mb-4">
						<span class="text-sm font-medium {riskLevel().color} uppercase tracking-wider">
							{riskLevel().level} ROI POTENTIAL
						</span>
					</div>
					<div class="roi-number text-6xl font-bold {riskLevel().color} mb-2">
						{calculatedROI().toLocaleString()}%
					</div>
					<p class="text-gray-600 dark:text-gray-300 text-lg">
						Return on Investment
					</p>
					<div class="mt-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
						<p class="text-sm text-gray-600 dark:text-gray-400">
							<strong>Potential lawsuit cost:</strong> ${potentialLawsuitCost().toLocaleString()}
						</p>
						<p class="text-sm text-gray-600 dark:text-gray-400">
							<strong>Annual protection cost:</strong> ${annualProtectionCost().toLocaleString()}
						</p>
					</div>
				</div>

				<!-- Speed Racing Animation -->
				<div bind:this={speedRacing} class="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-xl">
					<h3 class="text-xl font-bold text-gray-900 dark:text-white mb-6 text-center">
						Detection Speed Comparison
					</h3>
					
					<div class="space-y-6">
						<!-- Manual Process -->
						<div>
							<div class="flex justify-between items-center mb-2">
								<span class="text-sm font-medium text-gray-700 dark:text-gray-300">
									Manual Review
								</span>
								<span class="text-sm text-gray-500">
									{CRISIS_CONTEXT.manualDetectionTime} days
								</span>
							</div>
							<div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-3">
								<div class="manual-bar bg-red-500 h-3 rounded-full" style="width: 0%"></div>
							</div>
						</div>

						<!-- BiasGuard Process -->
						<div>
							<div class="flex justify-between items-center mb-2">
								<span class="text-sm font-medium text-gray-700 dark:text-gray-300">
									BiasGuard AI
								</span>
								<span class="text-sm text-green-600 font-semibold">
									< 1 day
								</span>
							</div>
							<div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-3">
								<div class="biasguard-bar bg-green-500 h-3 rounded-full" style="width: 0%"></div>
							</div>
						</div>
					</div>

					<div class="mt-6 text-center">
						<p class="text-2xl font-bold text-green-600">
							{timeSavingsPerIncident()} days saved per incident
						</p>
						<p class="text-sm text-gray-600 dark:text-gray-400">
							Estimated {annualTimeSavings()} days saved annually
						</p>
					</div>
				</div>

				<!-- Savings Accumulation -->
				<div bind:this={savingsCounter} class="bg-gradient-to-br from-green-50 to-emerald-100 dark:from-green-900/30 dark:to-emerald-900/30 rounded-2xl p-8 shadow-xl text-center">
					<h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4">
						Potential Annual Savings
					</h3>
					<div class="savings-amount text-5xl font-bold text-green-600 mb-2">
						${(potentialLawsuitCost() - annualProtectionCost()).toLocaleString()}
					</div>
					<p class="text-gray-600 dark:text-gray-300">
						vs. JAHmere's crisis: <span class="font-semibold">${CRISIS_CONTEXT.jahmereCost.toLocaleString()}</span>
					</p>
					<div class="mt-4 text-sm text-gray-600 dark:text-gray-400">
						<p>This could fund:</p>
						<ul class="list-disc list-inside space-y-1 mt-2">
							<li>{Math.floor((potentialLawsuitCost() - annualProtectionCost()) / 75000)} developer salaries</li>
							<li>{Math.floor((potentialLawsuitCost() - annualProtectionCost()) / 50000)} compliance audits</li>
							<li>{Math.floor((potentialLawsuitCost() - annualProtectionCost()) / 25000)} legal consultations</li>
						</ul>
					</div>
				</div>

				<!-- Risk Meter -->
				<div bind:this={riskMeter} class="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-xl text-center">
					<h3 class="text-xl font-bold text-gray-900 dark:text-white mb-6">
						Business Risk Level
					</h3>
					
					<div class="relative w-48 h-24 mx-auto mb-4">
						<svg class="w-full h-full" viewBox="0 0 200 100">
							<!-- Risk meter arc -->
							<path
								d="M 20 80 A 80 80 0 0 1 180 80"
								fill="none"
								stroke="currentColor"
								stroke-width="8"
								class="text-gray-200 dark:text-gray-600"
							/>
							<!-- Risk zones -->
							<path
								d="M 20 80 A 80 80 0 0 1 100 20"
								fill="none"
								stroke="currentColor"
								stroke-width="8"
								class="text-red-500"
							/>
							<!-- Needle -->
							<g class="risk-needle" style="transform-origin: 100px 80px;">
								<line
									x1="100"
									y1="80"
									x2="100"
									y2="30"
									stroke="currentColor"
									stroke-width="3"
									class="text-gray-900 dark:text-white"
								/>
								<circle
									cx="100"
									cy="80"
									r="4"
									fill="currentColor"
									class="text-gray-900 dark:text-white"
								/>
							</g>
						</svg>
					</div>
					
					<p class="text-lg font-semibold {riskLevel().color}">
						{riskLevel().level} RISK
					</p>
					<p class="text-sm text-gray-600 dark:text-gray-400 mt-2">
						Based on industry, team size, and risk tolerance
					</p>
				</div>
			</div>
		</div>

		<!-- Scenario Comparison Panel -->
		{#if showComparison}
			<div class="comparison-panel mt-12 bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-xl">
				<h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 text-center">
					Scenario Comparison: With vs Without BiasGuard
				</h3>
				
				<div class="grid md:grid-cols-2 gap-8">
					<!-- Without BiasGuard -->
					<div class="bg-red-50 dark:bg-red-900/30 rounded-xl p-6">
						<h4 class="text-xl font-bold text-red-700 dark:text-red-300 mb-4 flex items-center gap-2">
							 Without Protection
						</h4>
						<ul class="space-y-3 text-sm">
							<li class="flex items-start gap-2">
								<span class="text-red-500"></span>
								<span>Average lawsuit cost: <strong>${potentialLawsuitCost().toLocaleString()}</strong></span>
							</li>
							<li class="flex items-start gap-2">
								<span class="text-red-500">⏰</span>
								<span>Manual detection: <strong>{CRISIS_CONTEXT.manualDetectionTime} days</strong></span>
							</li>
							<li class="flex items-start gap-2">
								<span class="text-red-500"></span>
								<span>Reputation damage: <strong>Immeasurable</strong></span>
							</li>
							<li class="flex items-start gap-2">
								<span class="text-red-500"></span>
								<span>Legal fees: <strong>$100k - $500k</strong></span>
							</li>
							<li class="flex items-start gap-2">
								<span class="text-red-500"></span>
								<span>Team stress: <strong>High burnout risk</strong></span>
							</li>
						</ul>
					</div>

					<!-- With BiasGuard -->
					<div class="bg-green-50 dark:bg-green-900/30 rounded-xl p-6">
						<h4 class="text-xl font-bold text-green-700 dark:text-green-300 mb-4 flex items-center gap-2">
							 With BiasGuard
						</h4>
						<ul class="space-y-3 text-sm">
							<li class="flex items-start gap-2">
								<span class="text-green-500"></span>
								<span>Annual cost: <strong>${annualProtectionCost().toLocaleString()}</strong></span>
							</li>
							<li class="flex items-start gap-2">
								<span class="text-green-500"></span>
								<span>AI detection: <strong>< 1 day</strong></span>
							</li>
							<li class="flex items-start gap-2">
								<span class="text-green-500"></span>
								<span>Proactive protection: <strong>Prevent lawsuits</strong></span>
							</li>
							<li class="flex items-start gap-2">
								<span class="text-green-500"></span>
								<span>ROI: <strong>{calculatedROI().toLocaleString()}%</strong></span>
							</li>
							<li class="flex items-start gap-2">
								<span class="text-green-500"></span>
								<span>Peace of mind: <strong>Sleep better at night</strong></span>
							</li>
						</ul>
					</div>
				</div>

				<div class="mt-8 text-center">
					<div class="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-6 text-white">
						<h4 class="text-2xl font-bold mb-2">
							The Choice Is Clear
						</h4>
						<p class="text-lg mb-4">
							Save <strong>${(potentialLawsuitCost() - annualProtectionCost()).toLocaleString()}</strong> annually with BiasGuard protection
						</p>
						<p class="text-sm opacity-90">
							Don't let your company become the next JAHmere Webb crisis story
						</p>
					</div>
				</div>
			</div>
		{/if}

		<!-- Call to Action -->
		<div class="mt-12 text-center">
			<div class="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white">
				<h3 class="text-3xl font-bold mb-4">
					Ready to Protect Your Business?
				</h3>
				<p class="text-xl mb-6 opacity-90">
					Join the mission to eliminate bias and save costs like the {calculatedROI().toLocaleString()}% ROI above
				</p>
				<div class="flex flex-col sm:flex-row gap-4 justify-center">
					<button class="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-gray-100 transition-all transform hover:scale-105 cta-button">
						Start Free Trial
					</button>
					<button class="bg-blue-800 text-white px-8 py-4 rounded-lg font-semibold hover:bg-blue-900 transition-all transform hover:scale-105 cta-button">
						Schedule Demo
					</button>
				</div>
			</div>
		</div>
	</div>
</section>

<style>
	.slider::-webkit-slider-thumb {
		appearance: none;
		width: 20px;
		height: 20px;
		border-radius: 50%;
		background: #3b82f6;
		cursor: pointer;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
	}

	.slider::-moz-range-thumb {
		width: 20px;
		height: 20px;
		border-radius: 50%;
		background: #3b82f6;
		cursor: pointer;
		border: none;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
	}

	.comparison-panel {
		transform: translateX(100%);
		opacity: 0;
	}
</style>
