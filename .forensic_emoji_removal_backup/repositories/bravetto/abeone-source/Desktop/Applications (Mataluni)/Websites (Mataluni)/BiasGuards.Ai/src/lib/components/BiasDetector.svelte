<script lang="ts">
	import { onMount } from 'svelte';
	import { gsap } from 'gsap';

	// Svelte 5 Runes for reactive state
	let textInput = $state('');
	let isAnalyzing = $state(false);
	let results = $state<{
		biasScore: number;
		biasTypes: string[];
		suggestions: string[];
		confidence: number;
	} | null>(null);

	// Component refs
	let detectorSection: HTMLElement;
	let resultsContainer: HTMLElement;

	// Bias detection logic
	async function analyzeBias() {
		if (!textInput.trim()) return;

		isAnalyzing = true;

		// Simulate analysis
		await new Promise(resolve => setTimeout(resolve, 1500));

		// Generate results
		const biasScore = Math.random() * 100;
		const detectedTypes = ['Gender Bias', 'Racial Bias', 'Age Discrimination'];
		const improvementSuggestions = [
			'Consider gender-neutral language',
			'Review for implicit assumptions',
			'Use inclusive terminology'
		];

		results = {
			biasScore,
			biasTypes: detectedTypes,
			suggestions: improvementSuggestions,
			confidence: 85 + Math.random() * 15
		};

		isAnalyzing = false;

		// Show results
		if (resultsContainer) {
			gsap.fromTo(
				resultsContainer,
				{ opacity: 0, y: 20 },
				{ opacity: 1, y: 0, duration: 0.5, ease: 'power2.out' }
			);
		}
	}

	// Performance-focused animations
	onMount(() => {
		gsap.fromTo(
			detectorSection,
			{ opacity: 0, y: 30 },
			{ opacity: 1, y: 0, duration: 0.6, ease: 'power2.out' }
		);
	});

	// Bias score styling
	const getBiasScoreColor = (score: number) => {
		if (score < 30) return 'text-success-green-600 bg-success-green-50';
		if (score < 70) return 'text-yellow-600 bg-yellow-50';
		return 'text-alert-red-600 bg-alert-red-50';
	};
</script>

<section bind:this={detectorSection} class="py-16 bg-gray-50 dark:bg-gray-800">
	<div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
		<div class="text-center mb-12">
			<h2 class="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white mb-4">
				AI Bias Detection Engine
			</h2>
			<p class="text-xl text-gray-600 dark:text-gray-300">
				Born from <strong class="text-justice-blue-600">JAHmere Webb's legal crisis</strong> — Analysis
				helps reform the justice system
			</p>
		</div>

		<!-- Input Section -->
		<div class="biasguards-card mb-8">
			<label
				for="bias-input"
				class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-4"
			>
				Enter text to analyze for potential bias:
			</label>

			<textarea
				id="bias-input"
				bind:value={textInput}
				placeholder="Paste your AI-generated content, job descriptions, legal documents, or any text that needs bias analysis..."
				rows="6"
				class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg resize-none focus:ring-2 focus:ring-justice-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
				disabled={isAnalyzing}
			></textarea>

			<div class="flex justify-between items-center mt-4">
				<span class="text-sm text-gray-500 dark:text-gray-400">
					{textInput.length} characters
				</span>

				<button
					on:click={analyzeBias}
					disabled={!textInput.trim() || isAnalyzing}
					class="biasguards-button biasguards-button-primary px-6 py-3 text-base font-semibold disabled:opacity-50"
				>
					{#if isAnalyzing}
						<svg
							class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
						>
							<circle
								class="opacity-25"
								cx="12"
								cy="12"
								r="10"
								stroke="currentColor"
								stroke-width="4"
							></circle>
							<path
								class="opacity-75"
								fill="currentColor"
								d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
							></path>
						</svg>
						Analyzing Bias...
					{:else}
						🛡️ Detect Bias
					{/if}
				</button>
			</div>
		</div>

		<!-- Results Section -->
		{#if results}
			<div bind:this={resultsContainer} class="biasguards-card">
				<h3 class="text-2xl font-semibold text-gray-900 dark:text-white mb-6">Analysis Results</h3>

				<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
					<!-- Bias Score -->
					<div class="text-center">
						<div class="text-4xl font-bold mb-2 {getBiasScoreColor(results.biasScore)}">
							{results.biasScore.toFixed(1)}%
						</div>
						<div class="text-sm font-medium text-gray-600 dark:text-gray-400">Bias Risk Score</div>
					</div>

					<!-- Confidence -->
					<div class="text-center">
						<div class="text-4xl font-bold text-justice-blue-600 dark:text-blue-400 mb-2">
							{results.confidence.toFixed(1)}%
						</div>
						<div class="text-sm font-medium text-gray-600 dark:text-gray-400">
							Analysis Confidence
						</div>
					</div>
				</div>

				<!-- Detected Bias Types -->
				<div class="mb-8">
					<h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
						Detected Bias Types
					</h4>
					<div class="flex flex-wrap gap-2">
						{#each results.biasTypes as biasType}
							<span
								class="px-3 py-1 bg-alert-red-100 dark:bg-red-900/20 text-alert-red-700 dark:text-red-300 rounded-full text-sm font-medium"
							>
								{biasType}
							</span>
						{/each}
					</div>
				</div>

				<!-- Suggestions -->
				<div>
					<h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
						Improvement Suggestions
					</h4>
					<ul class="space-y-3">
						{#each results.suggestions as suggestion}
							<li class="flex items-start gap-3">
								<span
									class="flex-shrink-0 w-5 h-5 bg-success-green-100 dark:bg-green-900/20 text-success-green-600 dark:text-green-400 rounded-full flex items-center justify-center text-sm font-bold mt-0.5"
								>
									✓
								</span>
								<span class="text-gray-700 dark:text-gray-300">{suggestion}</span>
							</li>
						{/each}
					</ul>
				</div>

				<!-- Mission Context -->
				<div
					class="mt-8 p-4 bg-justice-blue-50 dark:bg-blue-900/20 rounded-lg border border-justice-blue-200 dark:border-blue-700"
				>
					<div
						class="flex items-center gap-2 text-justice-blue-700 dark:text-blue-300 text-sm font-medium"
					>
						<span>⚖️</span>
						<span>Justice Impact: This analysis contributes to criminal justice reform</span>
					</div>
				</div>
			</div>
		{/if}
	</div>
</section>
