.PHONY: guardian-enforce
guardian-enforce:
	@python3 scripts/enforce_guardian_single_source_of_truth.py --strict
