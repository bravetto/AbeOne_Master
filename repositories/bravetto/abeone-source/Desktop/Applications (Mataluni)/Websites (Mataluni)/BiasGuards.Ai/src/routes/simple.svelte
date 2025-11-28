<script lang="ts">
	import { onMount } from 'svelte';
	import { checkCode } from '$lib/utils/simple-validator';

	// JAHmere Webb Mission - Authentic Facts Only
	const MISSION_FACTS = {
		courtDate: 'August 25, 2025',
		crisisAmount: '$26,500',
		revenueToJustice: '15%',
		crisisTime: '2:42:56 AM',
		crisisDate: 'July 14, 2025'
	};

	// Svelte 5 Runes
	let isLoaded = $state(false);
	let demoCode = $state('');
	let validationResult = $state<any>(null);

	const missionDays = $derived(() => {
		const court = new Date('2025-08-25');
		const now = new Date();
		const diffTime = court.getTime() - now.getTime();
		const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
		return diffDays > 0 ? diffDays : 0;
	});

	function validateDemo() {
		if (!demoCode.trim()) return;
		
		const result = checkCode(demoCode);
		validationResult = result;
		
		console.log(' BiasGuard Live Validation:', result);
	}

	function testReactContamination() {
		demoCode = 'const [count, setCount] = useState(0);';
		validateDemo();
	}

	function testWrongFacts() {
		demoCode = 'const courtDate = "July 28, 2025";';
		validateDemo();
	}

	function testGoodCode() {
		demoCode = 'let count = $state(0);\nconst courtDate = "August 25, 2025";';
		validateDemo();
	}

	onMount(() => {
		isLoaded = true;
	});
</script>

<svelte:head>
	<title>BiasGuards.AI - Live Demo</title>
	<meta name="description" content="JAHmere Webb crisis: {MISSION_FACTS.crisisAmount} legal costs. Court date: {MISSION_FACTS.courtDate}. BiasGuard prevents AI bias." />
</svelte:head>

<main class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
	<div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
		
		<!-- Hero Section -->
		<div class="text-center mb-12">
			<div class="inline-flex items-center gap-2 bg-red-100 px-4 py-2 rounded-full text-red-700 font-semibold mb-6">
				 REAL CRISIS: JAHmere Webb faces {MISSION_FACTS.crisisAmount} legal costs
			</div>
			
			<h1 class="text-5xl font-bold text-gray-900 mb-4">
				BiasGuards.AI
				<span class="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
					Live Demo
				</span>
			</h1>
			
			<p class="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
				Born from JAHmere Webb's <strong>{MISSION_FACTS.crisisAmount}</strong> legal crisis on <strong>{MISSION_FACTS.crisisDate}</strong>. 
				Court date: <strong>{MISSION_FACTS.courtDate}</strong> ({missionDays} days remaining).
				<strong>15% revenue to criminal justice reform.</strong>
			</p>

			<div class="grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-2xl mx-auto mb-12">
				<div class="bg-white rounded-lg p-6 shadow-lg">
					<div class="text-3xl font-bold text-red-600 mb-2">{MISSION_FACTS.crisisAmount}</div>
					<div class="text-sm text-gray-600">Crisis Cost</div>
				</div>
				<div class="bg-white rounded-lg p-6 shadow-lg">
					<div class="text-3xl font-bold text-blue-600 mb-2">{missionDays}</div>
					<div class="text-sm text-gray-600">Days to Court</div>
				</div>
				<div class="bg-white rounded-lg p-6 shadow-lg">
					<div class="text-3xl font-bold text-green-600 mb-2">{MISSION_FACTS.revenueToJustice}</div>
					<div class="text-sm text-gray-600">To Justice Reform</div>
				</div>
			</div>
		</div>

		<!-- Live BiasGuard Validator Demo -->
		<div class="bg-white rounded-2xl shadow-xl p-8 mb-12">
			<h2 class="text-3xl font-bold text-gray-900 mb-6 text-center">
				 BiasGuard Validator - Live Demo
			</h2>
			
			<p class="text-lg text-gray-600 mb-8 text-center">
				Watch BiasGuard catch bias in real-time. This is the same system that achieved 
				<strong>recursive intelligence</strong> by analyzing its own code.
			</p>

			<!-- Quick Test Buttons -->
			<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
				<button 
					on:click={testGoodCode}
					class="bg-green-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-green-600 transition-colors"
				>
					 Test Good Code
				</button>
				<button 
					on:click={testReactContamination}
					class="bg-red-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-red-600 transition-colors"
				>
					 Test React Contamination
				</button>
				<button 
					on:click={testWrongFacts}
					class="bg-orange-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-orange-600 transition-colors"
				>
					 Test Wrong Facts
				</button>
			</div>

			<!-- Code Input -->
			<div class="mb-6">
				<label for="demo-code" class="block text-sm font-medium text-gray-700 mb-2">
					Enter Code to Validate:
				</label>
				<textarea
					id="demo-code"
					bind:value={demoCode}
					placeholder="Type some code here... Try: useState, v-if, or wrong JAHmere Webb facts"
					class="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg font-mono text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
				></textarea>
			</div>

			<button 
				on:click={validateDemo}
				class="w-full bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors mb-6"
			>
				 Validate Code with BiasGuard
			</button>

			<!-- Validation Results -->
			{#if validationResult}
				<div class="bg-gray-50 rounded-lg p-6">
					<h3 class="text-lg font-bold mb-4 {validationResult.valid ? 'text-green-600' : 'text-red-600'}">
						{validationResult.valid ? ' Validation Passed' : ' Issues Detected'}
					</h3>
					
					<div class="mb-4">
						<span class="text-sm font-medium text-gray-600">Score: </span>
						<span class="text-2xl font-bold {validationResult.score >= 80 ? 'text-green-600' : validationResult.score >= 60 ? 'text-orange-600' : 'text-red-600'}">
							{validationResult.score}/100
						</span>
					</div>

					{#if validationResult.issues.length > 0}
						<div class="mb-4">
							<h4 class="font-semibold text-red-600 mb-2">Issues Found:</h4>
							<ul class="list-disc list-inside space-y-1">
								{#each validationResult.issues as issue}
									<li class="text-red-700">{issue}</li>
								{/each}
							</ul>
						</div>
					{/if}

					{#if validationResult.recommendations && validationResult.recommendations.length > 0}
						<div>
							<h4 class="font-semibold text-blue-600 mb-2">Recommendations:</h4>
							<ul class="list-disc list-inside space-y-1">
								{#each validationResult.recommendations as rec}
									<li class="text-blue-700">{rec}</li>
								{/each}
							</ul>
						</div>
					{/if}
				</div>
			{/if}
		</div>

		<!-- Mission Statement -->
		<div class="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white text-center">
			<h2 class="text-3xl font-bold mb-4">Justice-Driven Mission</h2>
			<p class="text-xl mb-6">
				BiasGuard was born from JAHmere Webb's legal crisis. We prevent AI bias while funding criminal justice reform.
			</p>
			<div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-left">
				<div>
					<h3 class="font-semibold mb-2"> What BiasGuard Does:</h3>
					<ul class="space-y-1 text-sm">
						<li>• Detects React/Vue/Angular contamination</li>
						<li>• Validates mission story authenticity</li>
						<li>• Ensures Svelte 5 compliance</li>
						<li>• Prevents performance anti-patterns</li>
						<li>• Achieved recursive self-awareness</li>
					</ul>
				</div>
				<div>
					<h3 class="font-semibold mb-2"> Justice Mission Impact:</h3>
					<ul class="space-y-1 text-sm">
						<li>• 15% revenue to criminal justice reform</li>
						<li>• Supporting JAHmere Webb's freedom</li>
						<li>• Court date: {MISSION_FACTS.courtDate}</li>
						<li>• Crisis cost: {MISSION_FACTS.crisisAmount}</li>
						<li>• Technology serving justice</li>
					</ul>
				</div>
			</div>
		</div>

		<!-- Call to Action -->
		<div class="text-center mt-12">
			<h2 class="text-2xl font-bold text-gray-900 mb-4">
				Ready to Prevent AI Bias?
			</h2>
			<p class="text-lg text-gray-600 mb-8">
				Join the mission. Protect your code. Support justice reform.
			</p>
			<div class="flex flex-col sm:flex-row gap-4 justify-center">
				<button class="bg-blue-600 text-white px-8 py-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors">
					Start Free Trial
				</button>
				<button class="bg-white text-blue-600 border-2 border-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-blue-50 transition-colors">
					Schedule Demo
				</button>
			</div>
		</div>
	</div>
</main>

<style>
	/* Minimal, performant styles */
	:global(body) {
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
	}
</style>
