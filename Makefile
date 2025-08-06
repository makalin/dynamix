# DynaMix Makefile
# Common development tasks and automation

.PHONY: help install test test-coverage clean docs lint format check-deps

# Default target
help:
	@echo "🎵 DynaMix Development Commands"
	@echo "================================"
	@echo ""
	@echo "Installation:"
	@echo "  install          Install DynaMix and dependencies"
	@echo "  install-dev      Install development dependencies"
	@echo "  check-deps       Check if all dependencies are installed"
	@echo ""
	@echo "Testing:"
	@echo "  test             Run all tests"
	@echo "  test-coverage    Run tests with coverage report"
	@echo "  test-module      Run tests for specific module (MODULE=audio_utils)"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint             Run linting checks"
	@echo "  format           Format code with black"
	@echo "  check-format     Check code formatting"
	@echo ""
	@echo "Documentation:"
	@echo "  docs             Build documentation"
	@echo "  docs-serve       Serve documentation locally"
	@echo ""
	@echo "Development:"
	@echo "  clean            Clean build artifacts and cache"
	@echo "  dist             Build distribution package"
	@echo "  release          Prepare release package"
	@echo ""

# Installation
install:
	@echo "Installing DynaMix..."
	pip install -r requirements.txt
	@echo "✅ Installation complete!"

install-dev:
	@echo "Installing development dependencies..."
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	@echo "✅ Development installation complete!"

check-deps:
	@echo "Checking dependencies..."
	python -c "import librosa, numpy, matplotlib, pandas, seaborn; print('✅ All dependencies installed')" || echo "❌ Missing dependencies - run 'make install'"

# Testing
test:
	@echo "Running tests..."
	python -m pytest tests/ -v

test-coverage:
	@echo "Running tests with coverage..."
	python tests/run_tests.py

test-module:
	@echo "Running tests for module: $(MODULE)"
	python tests/run_tests.py --module $(MODULE)

# Code Quality
lint:
	@echo "Running linting checks..."
	flake8 audio_utils.py playlist_manager.py dj_tools.py mix_enhanced.py mix_analiz.py
	pylint audio_utils.py playlist_manager.py dj_tools.py mix_enhanced.py mix_analiz.py

format:
	@echo "Formatting code..."
	black audio_utils.py playlist_manager.py dj_tools.py mix_enhanced.py mix_analiz.py tests/ examples.py

check-format:
	@echo "Checking code formatting..."
	black --check audio_utils.py playlist_manager.py dj_tools.py mix_enhanced.py mix_analiz.py tests/ examples.py

# Documentation
docs:
	@echo "Building documentation..."
	cd docs && make html

docs-serve:
	@echo "Serving documentation at http://localhost:8000"
	cd docs/_build/html && python -m http.server 8000

# Development
clean:
	@echo "Cleaning build artifacts..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name "coverage_html" -exec rm -rf {} +
	rm -rf build/ dist/ *.egg-info/
	@echo "✅ Clean complete!"

dist:
	@echo "Building distribution package..."
	python setup.py sdist bdist_wheel

release: clean test-coverage lint check-format dist
	@echo "✅ Release preparation complete!"

# Quick development workflow
dev-setup: install-dev check-deps
	@echo "✅ Development environment ready!"

quick-test: check-deps test
	@echo "✅ Quick test complete!"

# Examples and demos
run-examples:
	@echo "Running examples..."
	python examples.py

demo-basic:
	@echo "Running basic demo..."
	python mix_enhanced.py --help

demo-playlist:
	@echo "Running playlist demo..."
	python mix_enhanced.py --playlist sample_data/playlists/house_playlist --set-duration 30

demo-dj-tools:
	@echo "Running DJ tools demo..."
	python dj_tools.py --help

# Performance and profiling
profile:
	@echo "Running performance profiling..."
	python -m cProfile -o profile.stats mix_enhanced.py --help

profile-view:
	@echo "Opening profile viewer..."
	python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative').print_stats(20)"

# Security checks
security-check:
	@echo "Running security checks..."
	bandit -r audio_utils.py playlist_manager.py dj_tools.py mix_enhanced.py mix_analiz.py

# Dependencies management
update-deps:
	@echo "Updating dependencies..."
	pip install --upgrade -r requirements.txt

freeze-deps:
	@echo "Freezing current dependencies..."
	pip freeze > requirements-frozen.txt

# Git helpers
git-status:
	@echo "Git status:"
	git status --short

git-diff:
	@echo "Git diff:"
	git diff

git-commit: format lint test
	@echo "Pre-commit checks passed. Ready to commit!"

# Docker helpers (if using Docker)
docker-build:
	@echo "Building Docker image..."
	docker build -t dynamix .

docker-run:
	@echo "Running DynaMix in Docker..."
	docker run -it --rm -v $(PWD):/app dynamix

# CI/CD helpers
ci-test: install-dev test-coverage lint security-check
	@echo "✅ CI tests passed!"

ci-build: ci-test dist
	@echo "✅ CI build complete!"

# Helpers for specific tasks
create-test-data:
	@echo "Creating test data directories..."
	mkdir -p sample_data/test_tracks
	mkdir -p sample_data/demo_tracks
	mkdir -p sample_data/playlists/house_playlist
	mkdir -p sample_data/playlists/techno_playlist
	@echo "✅ Test data directories created!"

setup-project: create-test-data dev-setup
	@echo "✅ Project setup complete!"

# Environment helpers
venv-create:
	@echo "Creating virtual environment..."
	python -m venv venv
	@echo "✅ Virtual environment created!"
	@echo "Activate with: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)"

venv-activate:
	@echo "Activate virtual environment:"
	@echo "Linux/Mac: source venv/bin/activate"
	@echo "Windows: venv\\Scripts\\activate"

# Backup and restore
backup:
	@echo "Creating backup..."
	tar -czf dynamix-backup-$(shell date +%Y%m%d).tar.gz \
		--exclude='venv' \
		--exclude='__pycache__' \
		--exclude='*.pyc' \
		--exclude='.git' \
		--exclude='sample_data' \
		.

restore:
	@echo "Restoring from backup..."
	@echo "Usage: make restore BACKUP_FILE=filename.tar.gz"
	tar -xzf $(BACKUP_FILE)

# System information
sys-info:
	@echo "System Information:"
	@echo "Python version: $(shell python --version)"
	@echo "Pip version: $(shell pip --version)"
	@echo "Platform: $(shell uname -s)"
	@echo "Architecture: $(shell uname -m)"

# Health check
health-check: check-deps test
	@echo "✅ System health check passed!"

# Default target
all: help 