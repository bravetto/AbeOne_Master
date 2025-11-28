/**
 * BiasGuards.AI Animation System
 * GSAP + Motion One integration
 */

/* eslint-disable no-undef */

import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { TextPlugin } from 'gsap/TextPlugin';
import { browser } from '$app/environment';
import { animate } from 'motion';

// Register GSAP plugins
if (browser) {
	gsap.registerPlugin(ScrollTrigger, TextPlugin);
}

export class BiasGuardAnimations {
	private timelines: gsap.core.Timeline[] = [];
	private isReducedMotion: boolean;

	constructor() {
		this.isReducedMotion =
			(browser &&
				typeof window !== 'undefined' &&
				window.matchMedia('(prefers-reduced-motion: reduce)').matches) ||
			false;
		if (browser) this.setupGlobalSettings();
	}

	private setupGlobalSettings() {
		gsap.config({
			force3D: true,
			nullTargetWarn: false,
			autoSleep: 60
		});

		gsap.defaults({
			ease: 'power2.out',
			duration: 0.6
		});

		if (this.isReducedMotion) {
			gsap.globalTimeline.timeScale(0.01);
		}
	}

	/**
	 * Hero entrance animation
	 */
	animateHeroEntrance(container?: HTMLElement): gsap.core.Timeline {
		if (this.isReducedMotion || !browser) return gsap.timeline();

		const tl = gsap.timeline();
		const scope = container ?? document;

		const elements = [
			{ selector: '.hero-alert', props: { scale: 0, opacity: 0, rotation: 360 } },
			{ selector: '.hero-title', props: { y: 100, opacity: 0, scale: 0.8 } },
			{ selector: '.hero-subtitle', props: { y: 50, opacity: 0 } },
			{ selector: '.hero-cta, .cta-button', props: { scale: 0, opacity: 0 } },
			{ selector: '.hero-stats, .stat-item', props: { x: -100, opacity: 0 } }
		];

		elements.forEach(({ selector, props }) => {
			const el = scope.querySelector(selector) || scope.querySelectorAll(selector);
			if (el && (el as any).length !== 0) {
				tl.from(el, { ...props, ease: 'power2.out' }, '-=0.3');
			}
		});

		this.timelines.push(tl);
		return tl;
	}

	/**
	 * Story reveal animation
	 */
	animateStoryReveal(container: HTMLElement): gsap.core.Timeline {
		if (this.isReducedMotion) return gsap.timeline();

		const tl = gsap.timeline({
			scrollTrigger: { trigger: container, start: 'top 60%' }
		});

		const elements = [
			{ selector: '.story-timeline', props: { scaleX: 0, transformOrigin: 'left center' } },
			{ selector: '.story-milestone', props: { scale: 0, opacity: 0, stagger: 0.3 } },
			{ selector: '.story-impact', props: { y: 50, opacity: 0 } }
		];

		elements.forEach(({ selector, props }) => {
			tl.from(selector, { ...props, ease: 'power2.out' });
		});

		this.timelines.push(tl);
		return tl;
	}

	/**
	 * Code analysis animation
	 */
	animateCodeAnalysis(container?: HTMLElement): gsap.core.Timeline {
		if (this.isReducedMotion || !browser) return gsap.timeline();

		const tl = gsap.timeline();
		const scope = container ?? document;

		const elements = [
			{
				selector: '.code-display',
				action: (el: Element) => tl.to(el, { text: { value: 'const hiring = "bias detected";' } })
			},
			{
				selector: '.analysis-indicator',
				action: (el: Element) => tl.to(el, { scale: 1.2, backgroundColor: '#ff6b6b', yoyo: true, repeat: 3 })
			},
			{
				selector: '.bias-alert',
				action: (el: Element) => tl.from(el, { scale: 0, opacity: 0, rotation: 360 })
			},
			{
				selector: '.bias-score',
				action: (el: Element) => tl.from(el, { textContent: 0, snap: { textContent: 1 } })
			}
		];

		elements.forEach(({ selector, action }) => {
			const el = scope.querySelector(selector);
			if (el) action(el);
		});

		this.timelines.push(tl);
		return tl;
	}

	/**
	 * Speed comparison animation
	 */
	animateSpeedDemo(container: HTMLElement): gsap.core.Timeline {
		if (this.isReducedMotion) return gsap.timeline();

		const tl = gsap.timeline({
			scrollTrigger: { trigger: container, start: 'top 70%' }
		});

		tl.to('.competitor-bar', { width: '100%' })
			.to('.biasguard-bar', { width: '100%', backgroundColor: '#16a34a' })
			.from('.speed-badge', { scale: 0, rotation: 360 });

		return tl;
	}

	/**
	 * Particle background
	 */
	createParticleBackground(container: HTMLElement, count = 20): HTMLElement[] {
		if (this.isReducedMotion || !browser) return [];

		const particles: HTMLElement[] = [];

		for (let i = 0; i < count; i++) {
			const particle = document.createElement('div');
			particle.className = 'particle';
			particle.style.cssText = `position: absolute; width: 2px; height: 2px; background: rgba(99, 102, 241, 0.4); border-radius: 50%; pointer-events: none; z-index: 1;`;

			container.appendChild(particle);
			particles.push(particle);

			gsap.set(particle, {
				x: Math.random() * container.offsetWidth,
				y: Math.random() * container.offsetHeight
			});

			const tl = gsap.timeline({ repeat: -1 });
			tl.to(particle, { y: `-=150`, opacity: 0, ease: 'none' });
			this.timelines.push(tl);
		}

		return particles;
	}

	/**
	 * Mouse magnetism effect
	 */
	addMouseMagnetism(element: HTMLElement): void {
		if (this.isReducedMotion || !browser) return;

		element.addEventListener('mouseenter', () => gsap.to(element, { scale: 1.05 }));
		element.addEventListener('mouseleave', () => gsap.to(element, { scale: 1, x: 0, y: 0 }));
		element.addEventListener('mousemove', e => {
			const rect = element.getBoundingClientRect();
			const x = (e.clientX - rect.left - rect.width / 2) * 0.1;
			const y = (e.clientY - rect.top - rect.height / 2) * 0.1;
			gsap.to(element, { x, y });
		});
	}

	/**
	 * Scroll reveal animation with multiple reveal types
	 */
	addScrollReveal(
		elements: NodeListOf<Element> | Element[],
		revealType: 'fade-up' | 'fade-in' | 'slide-left' | 'slide-right' | 'scale-up' = 'fade-up'
	): void {
		if (this.isReducedMotion || !browser) return;

		const elementsArray = Array.from(elements);

		elementsArray.forEach((element, index) => {
			let fromProps: gsap.TweenVars = {};

			switch (revealType) {
				case 'fade-up':
					fromProps = { y: 100, opacity: 0 };
					break;
				case 'fade-in':
					fromProps = { opacity: 0 };
					break;
				case 'slide-left':
					fromProps = { x: -100, opacity: 0 };
					break;
				case 'slide-right':
					fromProps = { x: 100, opacity: 0 };
					break;
				case 'scale-up':
					fromProps = { scale: 0.8, opacity: 0 };
					break;
			}

			gsap.from(element, {
				...fromProps,
				duration: 0.8,
				ease: 'power2.out',
				scrollTrigger: {
					trigger: element,
					start: 'top 80%',
					toggleActions: 'play none none reverse'
				},
				delay: index * 0.1
			});
		});
	}

	/**
	 * Animate testimonials with staggered reveals
	 */
	animateTestimonials(container: HTMLElement): gsap.core.Timeline {
		if (this.isReducedMotion || !browser) return gsap.timeline();

		const tl = gsap.timeline({
			scrollTrigger: {
				trigger: container,
				start: 'top 70%',
				toggleActions: 'play none none reverse'
			}
		});

		// Animate testimonial cards with stagger
		tl.from('.testimonial-card', {
			y: 80,
			opacity: 0,
			scale: 0.9,
			stagger: 0.2,
			duration: 0.8,
			ease: 'back.out(1.7)'
		})
			.from(
				'.testimonial-avatar',
				{
					scale: 0,
					rotation: 180,
					stagger: 0.1,
					duration: 0.6,
					ease: 'elastic.out(1, 0.3)'
				},
				'-=0.4'
			)
			.from(
				'.testimonial-quote',
				{
					opacity: 0,
					y: 20,
					stagger: 0.1,
					duration: 0.5
				},
				'-=0.2'
			);

		this.timelines.push(tl);
		return tl;
	}

	/**
	 * Animate ROI Calculator with interactive reveals
	 */
	animateROICalculator(container: HTMLElement): gsap.core.Timeline {
		if (this.isReducedMotion || !browser) return gsap.timeline();

		const tl = gsap.timeline({
			scrollTrigger: {
				trigger: container,
				start: 'top 60%',
				toggleActions: 'play none none reverse'
			}
		});

		// Calculator entrance
		tl.from('.roi-calculator', {
			scale: 0.9,
			opacity: 0,
			y: 50,
			duration: 0.8,
			ease: 'power2.out'
		})
			.from(
				'.roi-input-group',
				{
					x: -50,
					opacity: 0,
					stagger: 0.1,
					duration: 0.6
				},
				'-=0.4'
			)
			.from(
				'.roi-result',
				{
					scale: 0,
					opacity: 0,
					duration: 0.8,
					ease: 'elastic.out(1, 0.3)'
				},
				'-=0.2'
			)
			.from(
				'.roi-breakdown',
				{
					y: 30,
					opacity: 0,
					stagger: 0.1,
					duration: 0.5
				},
				'-=0.3'
			);

		this.timelines.push(tl);
		return tl;
	}

	/**
	 * Animate performance stats with number counters
	 */
	animatePerformanceStats(container: HTMLElement): gsap.core.Timeline {
		if (this.isReducedMotion || !browser) return gsap.timeline();

		const tl = gsap.timeline({
			scrollTrigger: {
				trigger: container,
				start: 'top 70%',
				toggleActions: 'play none none reverse'
			}
		});

		// Stats cards entrance
		tl.from('.stat-card', {
			y: 60,
			opacity: 0,
			scale: 0.9,
			stagger: 0.15,
			duration: 0.8,
			ease: 'back.out(1.7)'
		});

		// Animate numbers after cards appear
		const statNumbers = container.querySelectorAll('.stat-number');
		statNumbers.forEach((numberEl, index) => {
			const element = numberEl as HTMLElement;
			const targetValue = parseInt(element.textContent || '0');

			tl.call(
				() => {
					this.animateNumber(element, targetValue, 1500, '', element.dataset['suffix'] || '');
				},
				[],
				index * 0.1 + 0.3
			);
		});

		this.timelines.push(tl);
		return tl;
	}

	/**
	 * Animate feature cards with hover enhancements
	 */
	animateFeatureCards(container: HTMLElement): gsap.core.Timeline {
		if (this.isReducedMotion || !browser) return gsap.timeline();

		const tl = gsap.timeline({
			scrollTrigger: {
				trigger: container,
				start: 'top 75%',
				toggleActions: 'play none none reverse'
			}
		});

		// Cards entrance
		tl.from('.feature-card', {
			y: 80,
			opacity: 0,
			rotationY: 15,
			stagger: 0.2,
			duration: 0.8,
			ease: 'power2.out'
		}).from(
			'.feature-icon',
			{
				scale: 0,
				rotation: 180,
				stagger: 0.1,
				duration: 0.6,
				ease: 'elastic.out(1, 0.3)'
			},
			'-=0.4'
		);

		// Add hover effects to feature cards
		const featureCards = container.querySelectorAll('.feature-card');
		featureCards.forEach(card => {
			const element = card as HTMLElement;
			this.addMouseMagnetism(element);
		});

		this.timelines.push(tl);
		return tl;
	}

	/**
	 * Number counter
	 */
	animateNumber(element: HTMLElement, endValue: number, duration = 1500, prefix = '', suffix = ''): void {
		if (this.isReducedMotion || !browser) {
			element.textContent = `${prefix}${endValue.toLocaleString()}${suffix}`;
			return;
		}

		const obj = { value: 0 };
		gsap.to(obj, {
			value: endValue,
			ease: 'power2.out',
			onUpdate: () => {
				const currentValue = Math.floor(obj.value);
				element.textContent = `${prefix}${currentValue.toLocaleString()}${suffix}`;
			}
		});
	}

	/**
	 * Cleanup
	 */
	destroy(): void {
		this.timelines.forEach(tl => {
			tl.kill();
		});
		this.timelines = [];
		ScrollTrigger.getAll().forEach(st => {
			st.kill();
		});
	}
}

/**
 * Number Animations Utility
 */
export class NumberAnimations {
	/**
	 * Animate percentage with color transitions
	 */
	static animatePercentage(
		element: HTMLElement,
		targetValue: number,
		duration = 1.5,
		options: {
			prefix?: string;
			suffix?: string;
			colorThresholds?: { low: number; medium: number };
			colors?: { low: string; medium: string; high: string };
		} = {}
	): gsap.core.Timeline {
		if (!browser || !element) return gsap.timeline();

		const {
			prefix = '',
			suffix = '%',
			colorThresholds = { low: 40, medium: 70 },
			colors = {
				low: 'text-green-500',
				medium: 'text-yellow-500',
				high: 'text-red-500'
			}
		} = options;

		const tl = gsap.timeline();
		const obj = { value: 0 };

		// Scale entrance animation
		tl.from(element, {
			scale: 0,
			opacity: 0,
			duration: 0.5,
			ease: 'back.out(1.7)'
		});

		// Number counter animation
		tl.to(
			obj,
			{
				value: targetValue,
				duration: duration,
				ease: 'power2.out',
				onUpdate: () => {
					const currentValue = Math.floor(obj.value);
					element.textContent = `${prefix}${currentValue}${suffix}`;

					// Update color based on value
					const colorClass =
						currentValue >= colorThresholds.medium
							? colors.high
							: currentValue >= colorThresholds.low
								? colors.medium
								: colors.low;

					// Remove existing color classes and add new one
					element.className = element.className.replace(/text-(red|yellow|green)-\d+/g, '');
					if (!element.className.includes(colorClass)) {
						element.className += ` ${colorClass}`;
					}
				},
				onComplete: () => {
					// Pulse effect on completion
					gsap.to(element, {
						scale: 1.1,
						duration: 0.2,
						yoyo: true,
						repeat: 1,
						ease: 'power2.inOut'
					});
				}
			},
			'-=0.3'
		);

		return tl;
	}

	/**
	 * Animate counter with custom formatting
	 */
	static animateCounter(
		element: HTMLElement,
		startValue: number,
		endValue: number,
		duration = 1.5,
		formatter?: (value: number) => string
	): gsap.core.Timeline {
		if (!browser || !element) return gsap.timeline();

		const tl = gsap.timeline();
		const obj = { value: startValue };

		tl.to(obj, {
			value: endValue,
			duration: duration,
			ease: 'power2.out',
			onUpdate: () => {
				const currentValue = Math.floor(obj.value);
				element.textContent = formatter ? formatter(currentValue) : currentValue.toLocaleString();
			}
		});

		return tl;
	}

	/**
	 * Animate progress bar with number
	 */
	static animateProgressBar(
		barElement: HTMLElement,
		numberElement: HTMLElement,
		targetPercentage: number,
		duration = 1.5
	): gsap.core.Timeline {
		if (!browser || !barElement || !numberElement) return gsap.timeline();

		const tl = gsap.timeline();
		const obj = { value: 0 };

		// Animate both bar width and number simultaneously
		tl.to(obj, {
			value: targetPercentage,
			duration: duration,
			ease: 'power2.out',
			onUpdate: () => {
				const currentValue = Math.floor(obj.value);

				// Update progress bar width
				gsap.set(barElement, { width: `${currentValue}%` });

				// Update number display
				numberElement.textContent = `${currentValue}%`;
			}
		});

		return tl;
	}
}

/**
 * MOTION ONE MICRO-INTERACTIONS - Enhanced button effects
 */
export const MicroInteractions = {
	enhanceButtons(selector = '.cta-button'): void {
		if (!browser || typeof document === 'undefined') return;
		const buttons = document.querySelectorAll(selector);

		buttons.forEach(button => {
			const element = button as HTMLElement;

			element.addEventListener('mouseenter', () => {
				if (typeof animate !== 'undefined') {
					animate(
						element,
						{
							scale: 1.05,
							boxShadow: '0 10px 30px rgba(99, 102, 241, 0.4)'
						},
						{ duration: 0.2 }
					);
				} else {
					gsap.to(element, {
						scale: 1.05,
						boxShadow: '0 10px 30px rgba(99, 102, 241, 0.4)',
						duration: 0.2
					});
				}
			});

			element.addEventListener('mouseleave', () => {
				if (typeof animate !== 'undefined') {
					animate(
						element,
						{
							scale: 1,
							boxShadow: '0 4px 15px rgba(99, 102, 241, 0.3)'
						},
						{ duration: 0.2 }
					);
				} else {
					gsap.to(element, {
						scale: 1,
						boxShadow: '0 4px 15px rgba(99, 102, 241, 0.3)',
						duration: 0.2
					});
				}
			});

			element.addEventListener('click', () => {
				if (typeof animate !== 'undefined') {
					animate(
						element,
						{
							scale: [1, 0.95, 1.05, 1]
						},
						{ duration: 0.3 }
					);
				} else {
					gsap
						.timeline()
						.to(element, { scale: 0.95, duration: 0.1 })
						.to(element, { scale: 1.05, duration: 0.1 })
						.to(element, { scale: 1, duration: 0.1 });
				}
			});
		});
	},

	enhanceFormFields(selector = 'input, textarea'): void {
		if (!browser || typeof document === 'undefined') return;
		const inputs = document.querySelectorAll(selector);

		inputs.forEach(input => {
			const element = input as HTMLElement;

			element.addEventListener('focus', () => {
				if (typeof animate !== 'undefined') {
					animate(
						element,
						{
							outline: '2px solid #6366f1',
							outlineOffset: '2px'
						},
						{ duration: 0.2 }
					);
				} else {
					gsap.to(element, {
						scale: 1.02,
						boxShadow: '0 0 0 3px rgba(99, 102, 241, 0.1)',
						duration: 0.2
					});
				}
			});

			element.addEventListener('blur', () => {
				if (typeof animate !== 'undefined') {
					animate(
						element,
						{
							outline: 'none'
						},
						{ duration: 0.2 }
					);
				} else {
					gsap.to(element, {
						scale: 1,
						boxShadow: 'none',
						duration: 0.2
					});
				}
			});
		});
	},

	// Loading state animations
	animateLoading(element: HTMLElement) {
		if (typeof animate !== 'undefined') {
			return animate(
				element,
				{
					transform: ['rotate(0deg)', 'rotate(360deg)']
				},
				{
					duration: 1,
					repeat: Infinity,
					easing: 'linear'
				}
			);
		} else {
			return gsap.to(element, {
				rotation: 360,
				duration: 1,
				repeat: -1,
				ease: 'none'
			});
		}
	}
};

/**
 * Performance optimizations
 */
export const AnimationOptimizer = {
	respectReducedMotion(): boolean {
		if (!browser || typeof window === 'undefined') return false;
		const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

		if (prefersReducedMotion.matches) {
			gsap.config({ nullTargetWarn: false });
			gsap.globalTimeline.timeScale(0.01);
			return true;
		}

		return false;
	},

	throttleScrollAnimations(): void {
		if (!browser || typeof window === 'undefined') return;
		let ticking = false;

		const updateAnimations = () => {
			ScrollTrigger.refresh();
			ticking = false;
		};

		window.addEventListener('scroll', () => {
			if (!ticking) {
				window.requestAnimationFrame(updateAnimations);
				ticking = true;
			}
		}, { passive: true });
	},

	optimizeForMobile(): void {
		if (!browser || typeof navigator === 'undefined') return;
		const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

		if (isMobile) {
			gsap.config({ force3D: false });
		}
	}
};

/**
 * Svelte integration
 */
export function createBiasGuardAnimations(node: HTMLElement) {
	const animations = new BiasGuardAnimations();

	animations.animateHeroEntrance(node.querySelector('.hero') as HTMLElement);
	animations.addScrollReveal(node.querySelectorAll('.reveal-on-scroll'));

	const sections = [
		{ selector: '.social-proof-section', method: 'animateTestimonials' },
		{ selector: '.roi-section', method: 'animateROICalculator' },
		{ selector: '.performance-section', method: 'animatePerformanceStats' },
		{ selector: '.features-section', method: 'animateFeatureCards' }
	];

	sections.forEach(({ selector, method }) => {
		const section = node.querySelector(selector) as HTMLElement;
		if (section) (animations as any)[method](section);
	});

	MicroInteractions.enhanceButtons();
	MicroInteractions.enhanceFormFields();

	AnimationOptimizer.respectReducedMotion();
	AnimationOptimizer.throttleScrollAnimations();
	AnimationOptimizer.optimizeForMobile();

	return {
		destroy() {
			animations.destroy();
		}
	};
}
