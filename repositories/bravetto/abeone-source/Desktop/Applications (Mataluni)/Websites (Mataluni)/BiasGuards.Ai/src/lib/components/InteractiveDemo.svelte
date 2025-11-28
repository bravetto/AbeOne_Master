<script lang="ts">
	import { onMount } from 'svelte';
	import { gsap } from 'gsap';
	import { browser } from '$app/environment';
	import { BiasGuardAnimations, NumberAnimations } from '$lib/utils/animations';

	// Demo state
	let demoContainer: HTMLElement;
	let codeInput: HTMLTextAreaElement;
	let resultsContainer: HTMLElement;
	let analysisIndicator: HTMLElement;
	let scoreElement: HTMLElement;
	let speedDemoContainer: HTMLElement;

	// Animation instances
	let animations: BiasGuardAnimations;

	// Reactive state
	let currentCode = $state('');
	let isAnalyzing = $state(false);
	let analysisComplete = $state(false);
	let biasScore = $state(0);
	let detectedPatterns = $state<
		Array<{
			type: string;
			severity: 'high' | 'medium' | 'low';
			text: string;
			suggestion: string;
			confidence: number;
		}>
	>([]);

	// Demo examples
	const BIAS_EXAMPLES = [
		{
			category: 'Hiring',
			code: `// Hiring algorithm comment
const evaluateCandidate = (profile) => {
  // Women are typically worse at technical roles
  if (profile.gender === 'female') {
    return profile.score * 0.8;
  }
  return profile.score;
};`,
			patterns: [
				{
					type: 'Gender Bias',
					severity: 'high',
					text: 'Women are typically worse at technical roles',
					suggestion: 'Remove gender-based assumptions.',
					confidence: 94
				}
			],
			overallScore: 78
		},
		{
			category: 'Criminal Justice',
			code: `// Risk assessment system
function calculateRiskScore(defendant) {
  let score = baseScore;
  // Defendants from certain neighborhoods are higher risk
  if (defendant.zipCode.startsWith('90210')) {
    score += 15;
  }
  return Math.min(score, 100);
}`,
			patterns: [
				{
					type: 'Geographic Bias',
					severity: 'high',
					text: 'Defendants from certain neighborhoods are higher risk',
					suggestion: 'Avoid location-based assumptions.',
					confidence: 91
				}
			],
			overallScore: 82
		},
		{
			category: 'Financial',
			code: `// Credit scoring algorithm
const assessCreditworthiness = (applicant) => {
  // Certain ethnic names correlate with default risk
  let riskFactor = 1.0;
  if (isEthnicName(applicant.name)) {
    riskFactor *= 1.3;
  }
  return calculateScore(applicant) / riskFactor;
};`,
			patterns: [
				{
					type: 'Ethnic Bias',
					severity: 'high',
					text: 'Certain ethnic names correlate with default risk',
					suggestion: 'Remove name-based discrimination.',
					confidence: 96
				}
			],
			overallScore: 85
		}
	];

	let selectedExample = $state(0);
	let typingAnimation: gsap.core.Timeline | null = null;

	// Bias detection simulation
	async function analyzeCode() {
		if (!currentCode.trim() || isAnalyzing) return;

		isAnalyzing = true;
		analysisComplete = false;
		biasScore = 0;
		detectedPatterns = [];

		// Show analysis indicator
		if (browser && analysisIndicator) {
			gsap.set(analysisIndicator, { display: 'flex', opacity: 1 });
		}

		// Use code analysis animation
		if (animations && demoContainer) {
			await animations.animateCodeAnalysis(demoContainer);
		}

		// Simulate analysis delay
		await new Promise(resolve => setTimeout(resolve, Math.random() * 200 + 100));

		// Detect bias patterns
		const example = BIAS_EXAMPLES.find(
			ex => ex.patterns[0]?.text && currentCode.includes(ex.patterns[0].text.slice(0, 20))
		);

		if (example?.patterns) {
			detectedPatterns = example.patterns as typeof detectedPatterns;
			biasScore = example.overallScore;
		} else {
			// Generic analysis for custom input
			const biasKeywords = [
				'women',
				'men',
				'female',
				'male',
				'gender',
				'race',
				'ethnic',
				'black',
				'white',
				'asian',
				'old',
				'young',
				'age',
				'elderly'
			];

			const foundKeywords = biasKeywords.filter(keyword =>
				currentCode.toLowerCase().includes(keyword)
			);

			if (foundKeywords.length > 0) {
				biasScore = Math.min(foundKeywords.length * 15 + Math.random() * 20, 95);
				detectedPatterns = [
					{
						type: 'Potential Bias',
						severity: biasScore > 60 ? 'high' : biasScore > 30 ? 'medium' : ('low' as const),
						text: `Contains potentially biased language: ${foundKeywords.join(', ')}`,
						suggestion: 'Review code for discriminatory patterns.',
						confidence: Math.floor(biasScore * 0.9)
					}
				];
			} else {
				biasScore = Math.random() * 25;
			}
		}

		isAnalyzing = false;

		// Animate results using NumberAnimations
		if (browser) {
			await animateResults();
		}

		analysisComplete = true;
	}

	// Results animation sequence
	async function animateResults() {
		if (!browser || !resultsContainer) return;

		// Hide analysis indicator
		gsap.to(analysisIndicator, { opacity: 0, duration: 0.3 });

		// Show results container
		gsap.set(resultsContainer, { display: 'block' });

		const tl = gsap.timeline();

		// Use NumberAnimations for score animation
		if (scoreElement) {
			NumberAnimations.animatePercentage(scoreElement, biasScore, 1.5, {
				colorThresholds: { low: 40, medium: 70 },
				colors: {
					low: 'text-green-500',
					medium: 'text-yellow-500',
					high: 'text-red-500'
				}
			});
		}

		// Animate detected patterns
		tl.from(
			'.pattern-card',
			{
				y: 50,
				opacity: 0,
				stagger: 0.2,
				duration: 0.6,
				ease: 'power2.out'
			},
			'+=0.5'
		);

		// Trigger speed demo animation after a delay
		setTimeout(() => {
			if (animations && speedDemoContainer) {
				animations.animateSpeedDemo(speedDemoContainer);
			}
		}, 1000);
	}

	// Load example code with typing animation
	async function loadExample(index: number) {
		if (typingAnimation) {
			typingAnimation.kill();
		}

		selectedExample = index;
		const example = BIAS_EXAMPLES[index];
		if (!example) return;

		// Clear current state
		currentCode = '';
		analysisComplete = false;
		detectedPatterns = [];
		biasScore = 0;

		if (browser && codeInput) {
			// Typing animation
			typingAnimation = gsap.timeline();

			let currentChar = 0;
			const targetText = example.code;

			typingAnimation.to(
				{},
				{
					duration: targetText.length * 0.03,
					ease: 'none',
					onUpdate: () => {
						const progress = typingAnimation?.progress() || 0;
						currentChar = Math.floor(progress * targetText.length);
						currentCode = targetText.slice(0, currentChar);
						codeInput.value = currentCode;

						// Auto-scroll to bottom
						codeInput.scrollTop = codeInput.scrollHeight;
					},
					onComplete: () => {
						// Auto-analyze after typing completes
						setTimeout(analyzeCode, 500);
					}
				}
			);
		}
	}

	// Manual input handling
	function handleInput(event: Event) {
		const target = event.target as HTMLTextAreaElement;
		currentCode = target.value;

		// Reset analysis state on manual input
		if (analysisComplete) {
			analysisComplete = false;
			detectedPatterns = [];
			biasScore = 0;
		}
	}

	// Initialize component
	onMount(() => {
		if (browser) {
			// Initialize animations
			animations = new BiasGuardAnimations();

			// Load first example by default
			setTimeout(() => loadExample(0), 1000);
		}

		// Cleanup on destroy
		return () => {
			if (animations) {
				animations.destroy();
			}
		};
	});
</script>

<section id="bias-detector" class="py-20 bg-white dark:bg-gray-900">
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
		<!-- Section Header -->
		<div class="text-center mb-16">
			<h2 class="text-4xl sm:text-5xl font-bold text-gray-900 dark:text-white mb-6">
				Try BiasGuards.AI Live
			</h2>
			<p class="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto mb-8">
				See how our AI detects bias patterns in real-time. Test with our examples or paste your own
				code.
			</p>

			<!-- Example selector -->
			<div class="flex flex-wrap justify-center gap-4 mb-8">
				{#each BIAS_EXAMPLES as example, index}
					<button
						type="button"
						class="px-6 py-3 rounded-lg font-medium transition-all duration-200
							{selectedExample === index
							? 'bg-blue-600 text-white shadow-lg'
							: 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'}"
						onclick={() => loadExample(index)}
					>
						{example.category}
					</button>
				{/each}
			</div>
		</div>

		<!-- Demo Container -->
		<div bind:this={demoContainer} class="grid lg:grid-cols-2 gap-8">
			<!-- Code Input Panel -->
			<div class="bg-gray-900 rounded-xl overflow-hidden shadow-2xl">
				<div class="bg-gray-800 px-6 py-4 border-b border-gray-700">
					<div class="flex items-center gap-2">
						<div class="w-3 h-3 bg-red-500 rounded-full"></div>
						<div class="w-3 h-3 bg-yellow-500 rounded-full"></div>
						<div class="w-3 h-3 bg-green-500 rounded-full"></div>
						<span class="ml-4 text-gray-300 text-sm font-mono">bias-detector.js</span>
					</div>
				</div>

				<div class="relative">
					<textarea
						bind:this={codeInput}
						bind:value={currentCode}
						oninput={handleInput}
						class="w-full h-96 bg-gray-900 text-green-400 font-mono text-sm p-6
							resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
						placeholder="// Paste your code here or try an example above..."
						spellcheck="false"
					></textarea>

					<!-- Line numbers -->
					<div class="absolute left-2 top-6 text-gray-600 font-mono text-sm pointer-events-none">
						{#each Array(20) as _, i}
							<div class="leading-6">{i + 1}</div>
						{/each}
					</div>
				</div>

				<!-- Analyze Button -->
				<div class="p-6 border-t border-gray-700">
					<button
						type="button"
						onclick={analyzeCode}
						disabled={!currentCode.trim() || isAnalyzing}
						class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600
							text-white font-bold py-4 px-6 rounded-lg transition-all duration-200
							transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed"
					>
						{isAnalyzing ? 'Analyzing...' : 'Analyze for Bias'}
					</button>
				</div>
			</div>

			<!-- Results Panel -->
			<div class="space-y-6">
				<!-- Analysis Indicator -->
				<div
					bind:this={analysisIndicator}
					class="hidden items-center justify-center p-8 bg-blue-50 dark:bg-blue-900/20
						rounded-xl border-2 border-dashed border-blue-300 dark:border-blue-700"
				>
					<div class="text-center">
						<div
							class="spinner w-8 h-8 border-4 border-blue-600 border-t-transparent
							rounded-full mx-auto mb-4"
						></div>
						<p class="text-blue-600 dark:text-blue-400 font-medium">
							Analyzing code for bias patterns...
						</p>
					</div>
				</div>

				<!-- Results Container -->
				<div bind:this={resultsContainer} class="hidden space-y-6">
					<!-- Bias Score -->
					<div class="bg-white dark:bg-gray-800 rounded-xl p-8 shadow-lg text-center">
						<h3 class="text-2xl font-semibold text-gray-900 dark:text-white mb-4">Bias Score</h3>
						<div bind:this={scoreElement} class="text-6xl font-bold text-gray-500 mb-4">0%</div>
						<div class="text-sm text-gray-600 dark:text-gray-400">
							{biasScore > 70
								? 'High bias detected'
								: biasScore > 40
									? 'Moderate bias detected'
									: 'Low bias detected'}
						</div>
					</div>

					<!-- Detected Patterns -->
					{#if detectedPatterns.length > 0}
						<div class="bg-white dark:bg-gray-800 rounded-xl p-8 shadow-lg">
							<h3 class="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
								Detected Issues
							</h3>

							<div class="space-y-4">
								{#each detectedPatterns as pattern, index}
									<div
										class="pattern-card border-l-4
										{pattern.severity === 'high'
											? 'border-red-500 bg-red-50 dark:bg-red-900/20'
											: pattern.severity === 'medium'
												? 'border-yellow-500 bg-yellow-50 dark:bg-yellow-900/20'
												: 'border-green-500 bg-green-50 dark:bg-green-900/20'} 
										p-4 rounded-r-lg"
									>
										<div class="flex items-start justify-between mb-2">
											<h4
												class="font-semibold
												{pattern.severity === 'high'
													? 'text-red-700 dark:text-red-300'
													: pattern.severity === 'medium'
														? 'text-yellow-700 dark:text-yellow-300'
														: 'text-green-700 dark:text-green-300'}"
											>
												{pattern.type}
											</h4>
											<span
												class="text-sm font-medium px-2 py-1 rounded-full
												{pattern.severity === 'high'
													? 'bg-red-200 text-red-800 dark:bg-red-800 dark:text-red-200'
													: pattern.severity === 'medium'
														? 'bg-yellow-200 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-200'
														: 'bg-green-200 text-green-800 dark:bg-green-800 dark:text-green-200'}"
											>
												{pattern.confidence}% confident
											</span>
										</div>

										<p class="text-gray-700 dark:text-gray-300 mb-2 italic">
											"{pattern.text}"
										</p>

										<p class="text-gray-600 dark:text-gray-400 text-sm">
											 {pattern.suggestion}
										</p>
									</div>
								{/each}
							</div>
						</div>
					{/if}

					<!-- Performance Stats -->
					{#if analysisComplete}
						<div
							class="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20
							rounded-xl p-6 border border-blue-200 dark:border-blue-800"
						>
							<div class="grid grid-cols-3 gap-4 text-center">
								<div>
									<div class="text-2xl font-bold text-blue-600 dark:text-blue-400">&lt;200ms</div>
									<div class="text-sm text-gray-600 dark:text-gray-400">Analysis Time</div>
								</div>
								<div>
									<div class="text-2xl font-bold text-blue-600 dark:text-blue-400">
										{detectedPatterns.length}
									</div>
									<div class="text-sm text-gray-600 dark:text-gray-400">Issues Found</div>
								</div>
								<div>
									<div class="text-2xl font-bold text-blue-600 dark:text-blue-400">84.9%</div>
									<div class="text-sm text-gray-600 dark:text-gray-400">Accuracy Rate</div>
								</div>
							</div>
						</div>
					{/if}
				</div>
			</div>
		</div>

		<!-- Speed Comparison Demo -->
		{#if analysisComplete}
			<div
				bind:this={speedDemoContainer}
				class="mt-16 bg-gray-50 dark:bg-gray-900/50 rounded-2xl p-8"
			>
				<h3 class="text-2xl font-bold text-center mb-8 text-gray-900 dark:text-white">
					Speed Comparison: BiasGuard vs Competitors
				</h3>

				<div class="space-y-6">
					<!-- Competitor Bar -->
					<div class="flex items-center gap-4">
						<span class="w-24 text-sm font-medium text-gray-600 dark:text-gray-400">
							Competitor
						</span>
						<div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-8 relative">
							<div
								class="competitor-bar bg-red-500 h-8 rounded-full flex items-center justify-end pr-4"
								style="width: 0%"
							>
								<span class="text-white text-sm font-bold">3.2s</span>
							</div>
						</div>
					</div>

					<!-- BiasGuard Bar -->
					<div class="flex items-center gap-4">
						<span class="w-24 text-sm font-medium text-gray-600 dark:text-gray-400">
							BiasGuard
						</span>
						<div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-8 relative">
							<div
								class="biasguard-bar bg-green-500 h-8 rounded-full flex items-center justify-end pr-4"
								style="width: 0%"
							>
								<span class="text-white text-sm font-bold">0.18s</span>
							</div>
						</div>
					</div>
				</div>

				<!-- Speed Badge -->
				<div class="text-center mt-8">
					<div
						class="speed-badge inline-flex items-center bg-green-100 dark:bg-green-900/30
						text-green-800 dark:text-green-300 px-6 py-3 rounded-full font-bold"
					>
						<svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
							<path
								fill-rule="evenodd"
								d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
								clip-rule="evenodd"
							></path>
						</svg>
						18x Faster Analysis
					</div>
				</div>
			</div>
		{/if}

		<!-- Call to Action -->
		{#if analysisComplete}
			<div class="text-center mt-16">
				<div class="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-8 text-white">
					<h3 class="text-2xl font-bold mb-4">Ready to eliminate bias from your AI systems?</h3>
					<p class="text-blue-100 mb-6 max-w-2xl mx-auto">
						Get started with BiasGuards.AI and protect your applications from discriminatory
						patterns.
					</p>
					<div class="flex flex-col sm:flex-row gap-4 justify-center">
						<button
							type="button"
							class="bg-white text-blue-600 px-8 py-3 rounded-lg font-bold
							hover:bg-gray-100 transition-colors duration-200"
						>
							Start Free Trial
						</button>
						<button
							type="button"
							class="border-2 border-white text-white px-8 py-3 rounded-lg font-bold
							hover:bg-white/10 transition-colors duration-200"
						>
							View Pricing
						</button>
					</div>
				</div>
			</div>
		{/if}
	</div>
</section>

<style>
	.spinner {
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		from {
			transform: rotate(0deg);
		}
		to {
			transform: rotate(360deg);
		}
	}

	/* Custom scrollbar for code textarea */
	textarea::-webkit-scrollbar {
		width: 8px;
	}

	textarea::-webkit-scrollbar-track {
		background: #374151;
	}

	textarea::-webkit-scrollbar-thumb {
		background: #6b7280;
		border-radius: 4px;
	}

	textarea::-webkit-scrollbar-thumb:hover {
		background: #9ca3af;
	}

	/* Mobile optimizations */
	@media (max-width: 768px) {
		textarea {
			height: 300px;
		}

		.text-6xl {
			font-size: 3rem;
		}
	}

	/* Accessibility */
	@media (prefers-reduced-motion: reduce) {
		.spinner {
			animation: none;
		}

		* {
			transition: none !important;
		}
	}
</style>
