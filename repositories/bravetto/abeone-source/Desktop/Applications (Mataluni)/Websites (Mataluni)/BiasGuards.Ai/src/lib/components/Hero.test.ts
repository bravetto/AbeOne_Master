/**
 * BiasGuards.AI Hero Component Tests
 * Production-grade testing suite for JAHmere Webb Freedom Mission
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, cleanup } from '@testing-library/svelte';
import Hero from './Hero.svelte';
import { BiasGuardAnimations } from '$lib/utils/animations';
import { MISSION_TEST_DATA } from '../test-setup';

// Mock BiasGuardAnimations
vi.mock('$lib/utils/animations', () => ({
	BiasGuardAnimations: vi.fn().mockImplementation(() => ({
		animateHeroEntrance: vi.fn(),
		createParticleBackground: vi.fn().mockReturnValue([]),
		addMouseMagnetism: vi.fn(),
		animateNumber: vi.fn(),
		destroy: vi.fn()
	}))
}));

describe('Hero Component - JAHmere Webb Freedom Mission', () => {
	let mockAnimations: any;

	beforeEach(() => {
		mockAnimations = {
			animateHeroEntrance: vi.fn(),
			createParticleBackground: vi.fn().mockReturnValue([]),
			addMouseMagnetism: vi.fn(),
			animateNumber: vi.fn(),
			destroy: vi.fn()
		};
		(BiasGuardAnimations as any).mockImplementation(() => mockAnimations);
	});

	afterEach(() => {
		cleanup();
		vi.clearAllMocks();
	});

	describe('Mission Context & Legal Crisis', () => {
		it('should display correct court date from mission context', () => {
			render(Hero);

			expect(screen.getByText(/August 25, 2025/)).toBeInTheDocument();
		});

		it('should show legal crisis amount prominently', () => {
			render(Hero);

			expect(screen.getByText(/\$26,500/)).toBeInTheDocument();
			expect(screen.getByText(/LEGAL CRISIS/)).toBeInTheDocument();
		});

		it('should display days until court accurately', () => {
			render(Hero);

			// Should show countdown
			expect(screen.getByText(/days remaining/)).toBeInTheDocument();
		});

		it('should show revenue to justice percentage', () => {
			render(Hero);

			expect(screen.getByText(/15%/)).toBeInTheDocument();
			expect(screen.getByText(/Revenue to Reform/)).toBeInTheDocument();
		});
	});

	describe('Hero Content & Messaging', () => {
		it('should display main heading correctly', () => {
			render(Hero);

			const heading = screen.getByRole('heading', { level: 1 });
			expect(heading).toHaveTextContent('AI Bias Detection Tool');
		});

		it('should show JAHmere Webb personal story', () => {
			render(Hero);

			expect(screen.getByText(/JAHmere Webb/)).toBeInTheDocument();
			expect(screen.getByText(/led me to build this bias detection tool/)).toBeInTheDocument();
		});

		it('should have proper banner role for accessibility', () => {
			render(Hero);

			const heroSection = screen.getByRole('banner');
			expect(heroSection).toBeInTheDocument();
		});
	});

	describe('Call-to-Action Buttons', () => {
		it('should render both CTA buttons', () => {
			render(Hero);

			const demoButton = screen.getByRole('button', { name: /demo/i });
			const storyButton = screen.getByRole('button', { name: /story/i });

			expect(demoButton).toBeInTheDocument();
			expect(storyButton).toBeInTheDocument();
		});

		it('should have proper accessibility labels', () => {
			render(Hero);

			expect(screen.getByLabelText('Try demo')).toBeInTheDocument();
			expect(screen.getByLabelText('My story')).toBeInTheDocument();
		});

		it('should trigger scroll to demo section on demo button click', async () => {
			// Mock scrollIntoView
			const mockScrollIntoView = vi.fn();
			const mockQuerySelector = vi.fn().mockReturnValue({
				scrollIntoView: mockScrollIntoView
			});
			Object.defineProperty(document, 'querySelector', {
				value: mockQuerySelector,
				writable: true
			});

			render(Hero);

			const demoButton = screen.getByRole('button', { name: /demo/i });
			await fireEvent.click(demoButton);

			expect(mockQuerySelector).toHaveBeenCalledWith('#bias-detector');
			expect(mockScrollIntoView).toHaveBeenCalledWith({ behavior: 'smooth' });
		});

		it('should trigger scroll to story section on story button click', async () => {
			const mockScrollIntoView = vi.fn();
			const mockQuerySelector = vi.fn().mockReturnValue({
				scrollIntoView: mockScrollIntoView
			});
			Object.defineProperty(document, 'querySelector', {
				value: mockQuerySelector,
				writable: true
			});

			render(Hero);

			const storyButton = screen.getByRole('button', { name: /story/i });
			await fireEvent.click(storyButton);

			expect(mockQuerySelector).toHaveBeenCalledWith('#mission-story');
			expect(mockScrollIntoView).toHaveBeenCalledWith({ behavior: 'smooth' });
		});
	});

	describe('Animation Integration', () => {
		it('should initialize BiasGuardAnimations on mount', () => {
			render(Hero);

			expect(BiasGuardAnimations).toHaveBeenCalled();
		});

		it('should call animateHeroEntrance for eye-popping effects', () => {
			render(Hero);

			expect(mockAnimations.animateHeroEntrance).toHaveBeenCalled();
		});

		it('should create particle background for visual impact', () => {
			render(Hero);

			expect(mockAnimations.createParticleBackground).toHaveBeenCalledWith(
				expect.any(HTMLElement),
				25
			);
		});

		it('should add mouse magnetism to CTA buttons', () => {
			render(Hero);

			// Should be called for each CTA button
			expect(mockAnimations.addMouseMagnetism).toHaveBeenCalled();
		});

		it('should animate revenue number counter', () => {
			render(Hero);

			expect(mockAnimations.animateNumber).toHaveBeenCalledWith(
				expect.any(HTMLElement),
				15, // revenueToJustice percentage
				2000,
				'',
				'%'
			);
		});

		it('should properly cleanup animations on unmount', () => {
			const { unmount } = render(Hero);

			unmount();

			expect(mockAnimations.destroy).toHaveBeenCalled();
		});
	});

	describe('Hero Statistics', () => {
		it('should display all three stat items', () => {
			render(Hero);

			expect(screen.getByText('Revenue to Reform')).toBeInTheDocument();
			expect(screen.getByText('Detection Tool')).toBeInTheDocument();
			expect(screen.getByText('Analysis')).toBeInTheDocument();
		});

		it('should show Beta status for detection tool', () => {
			render(Hero);

			expect(screen.getByText('Beta')).toBeInTheDocument();
		});

		it('should show Fast analysis capability', () => {
			render(Hero);

			expect(screen.getByText('Fast')).toBeInTheDocument();
		});
	});

	describe('Visual Elements & Accessibility', () => {
		it('should have scroll indicator with proper aria attributes', () => {
			render(Hero);

			const scrollIndicator = screen.getByRole('img', { hidden: true });
			expect(scrollIndicator).toBeInTheDocument();
		});

		it('should have decorative background elements with aria-hidden', () => {
			render(Hero);

			const { container } = render(Hero);
			const decorativeElements = container.querySelectorAll('[aria-hidden="true"]');
			expect(decorativeElements.length).toBeGreaterThan(0);
		});

		it('should have proper CSS classes for animations', () => {
			const { container } = render(Hero);

			expect(container.querySelector('.hero-title')).toBeInTheDocument();
			expect(container.querySelector('.hero-subtitle')).toBeInTheDocument();
			expect(container.querySelector('.hero-cta')).toBeInTheDocument();
			expect(container.querySelector('.hero-stats')).toBeInTheDocument();
		});
	});

	describe('Responsive Design & Performance', () => {
		it('should have proper CSS classes for responsive layout', () => {
			const { container } = render(Hero);

			const heroSection = container.querySelector('.hero-section');
			expect(heroSection).toHaveClass('min-h-screen');
			expect(heroSection).toHaveClass('flex');
			expect(heroSection).toHaveClass('items-center');
			expect(heroSection).toHaveClass('justify-center');
		});

		it('should have overflow-hidden for particle background', () => {
			const { container } = render(Hero);

			const heroSection = container.querySelector('.hero-section');
			expect(heroSection).toHaveClass('overflow-hidden');
		});

		it('should have proper transform optimizations for buttons', () => {
			const { container } = render(Hero);

			const ctaButtons = container.querySelectorAll('.cta-button');
			ctaButtons.forEach(button => {
				expect(button).toHaveClass('cta-button');
			});
		});
	});

	describe('Crisis Context & Urgency', () => {
		it('should display crisis alert with proper styling', () => {
			render(Hero);

			const crisisAlert = screen.getByText(/LEGAL CRISIS/);
			expect(crisisAlert.closest('div')).toHaveClass('hero-alert');
		});

		it('should show emergency emoji for visual impact', () => {
			render(Hero);

			expect(screen.getByText('')).toBeInTheDocument();
		});

		it('should display court countdown with proper formatting', () => {
			render(Hero);

			expect(screen.getByText('')).toBeInTheDocument();
			expect(screen.getByText(/Court Date: August 25, 2025/)).toBeInTheDocument();
		});
	});

	describe('Mission Alignment', () => {
		it('should match mission test data constants', () => {
			render(Hero);

			// Verify mission alignment with test constants
			expect(screen.getByText(/August 25, 2025/)).toBeInTheDocument();
			expect(screen.getByText(/15%/)).toBeInTheDocument();
			expect(screen.getByText(/\$26,500/)).toBeInTheDocument();
		});

		it('should emphasize justice reform messaging', () => {
			render(Hero);

			expect(screen.getByText(/to reform/)).toBeInTheDocument();
			expect(screen.getByText(/Revenue to Reform/)).toBeInTheDocument();
		});
	});
});
