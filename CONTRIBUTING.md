# Contributing to Scientific Calculator (`sci-calc-20260903`)

Thank you for your interest in improving this project! We welcome contributions, bug fixes, and feature enhancements.

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Rituparno-Majumdar/sci-calc-20260903.git
   cd sci-calc-20260903
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pytest black
   ```

## Running Tests

Before submitting any code changes, ensure all tests pass:

```bash
pytest -v
```

## Architectural Guidelines

- **Dual API Parity**: Every mathematical operation added must exist both as a module-level pure function (e.g. `add(a, b)`) and as an instance method on `ScientificCalculator`.
- **Trig Boundary Isolation**: Internal trigonometry operates in radians. Degree conversion occurs strictly at the I/O boundary.
- **Auditable History**: History records should only be written on successful evaluation. Do not record operations that raise exceptions.
- **Zero Heavy Dependencies**: Keep the core lightweight with standard library `math`. Keep `rich` and `click` optional with clean fallbacks.

## Submitting Pull Requests

1. Fork the repo and create your feature branch: `git checkout -b feat/my-feature`.
2. Commit your changes with conventional commit messages (e.g. `feat:`, `fix:`, `docs:`).
3. Push to your branch and open a Pull Request.
