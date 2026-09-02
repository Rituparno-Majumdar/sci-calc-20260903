"""
constants.py — Physical and Mathematical Constants for Scientific Calculator
Author: Rituparno Majumdar
Version: v1.0.0

Provides MATHEMATICAL_CONSTANTS, PHYSICAL_CONSTANTS, and ALLOWED_CONSTS.
All values derived from Python's math module or CODATA 2018 SI recommendations.
"""
from __future__ import annotations

import math
from typing import Dict, List, Tuple

# ---------------------------------------------------------------------------
# Mathematical Constants
# ---------------------------------------------------------------------------
MATHEMATICAL_CONSTANTS: Dict[str, float] = {
    # Core mathematical constants
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,  # 2 * pi
    "inf": math.inf,
    "nan": math.nan,
    # Extended constants
    "phi": (1 + math.sqrt(5)) / 2,  # Golden ratio φ
    "euler_gamma": 0.5772156649015328606,  # Euler-Mascheroni constant γ
    "catalan": 0.91596559417721901505,  # Catalan's constant G
    "apery": 1.2020569031595942854,  # Apéry's constant ζ(3)
    "euler": math.e,  # Alias
    "golden": (1 + math.sqrt(5)) / 2,  # Alias for phi
    "sqrt2": math.sqrt(2),
    "sqrt3": math.sqrt(3),
    "ln2": math.log(2),
    "ln10": math.log(10),
    "log2e": math.log2(math.e),
    "log10e": math.log10(math.e),
}

# ---------------------------------------------------------------------------
# Physical Constants (SI Units, CODATA 2018)
# ---------------------------------------------------------------------------
PHYSICAL_CONSTANTS: Dict[str, float] = {
    "c": 299792458.0,  # Speed of light in vacuum (m/s)
    "G": 6.67430e-11,  # Gravitational constant (m^3 kg^-1 s^-2)
    "h": 6.62607015e-34,  # Planck constant (J⋅s)
    "hbar": 1.054571817e-34,  # Reduced Planck constant (J⋅s)
    "k": 1.380649e-23,  # Boltzmann constant (J/K)
    "Na": 6.02214076e23,  # Avogadro constant (mol^-1)
    "R": 8.314462618,  # Molar gas constant (J⋅mol^-1⋅K^-1)
    "e_charge": 1.602176634e-19,  # Elementary charge (C)
    "me": 9.1093837015e-31,  # Electron mass (kg)
    "mp": 1.67262192369e-27,  # Proton mass (kg, CODATA 2018 invariant)
    "mn": 1.67492749804e-27,  # Neutron mass (kg)
    "epsilon0": 8.8541878128e-12,  # Vacuum permittivity (F/m)
    "mu0": 1.25663706212e-6,  # Vacuum permeability (N/A^2)
    "sigma": 5.670374419e-8,  # Stefan-Boltzmann constant (W⋅m^-2⋅K^-4)
    "g": 9.80665,  # Standard acceleration of gravity (m/s^2)
    "atm": 101325.0,  # Standard atmosphere (Pa)
}

# ---------------------------------------------------------------------------
# Combined Allowed Constants & Aliases
# ---------------------------------------------------------------------------
ALLOWED_CONSTS: Dict[str, float] = {**MATHEMATICAL_CONSTANTS, **PHYSICAL_CONSTANTS}

# Convenient Unicode & Symbol Aliases
ALLOWED_CONSTS["π"] = ALLOWED_CONSTS["pi"]
ALLOWED_CONSTS["∞"] = ALLOWED_CONSTS["inf"]
ALLOWED_CONSTS["γ"] = ALLOWED_CONSTS["euler_gamma"]
ALLOWED_CONSTS["φ"] = ALLOWED_CONSTS["phi"]

__all__ = [
    "MATHEMATICAL_CONSTANTS",
    "PHYSICAL_CONSTANTS",
    "ALLOWED_CONSTS",
    "list_constants",
    "describe_constants",
]


def list_constants() -> Dict[str, float]:
    """Return a shallow copy of all available constants."""
    return dict(ALLOWED_CONSTS)


def describe_constants() -> List[Tuple[str, float, str]]:
    """Return list of (name, value, description) tuples for CLI/UI display."""
    descriptions: Dict[str, str] = {
        "pi": "π — Archimedes circle constant",
        "e": "Euler's number (base of natural logarithm)",
        "tau": "τ = 2π — circle circumference-to-radius ratio",
        "inf": "Positive Infinity",
        "nan": "Not a Number",
        "phi": "Golden ratio φ = (1 + √5) / 2",
        "euler_gamma": "Euler-Mascheroni constant γ",
        "catalan": "Catalan's constant G",
        "apery": "Apéry's constant ζ(3)",
        "c": "Speed of light in vacuum (m/s)",
        "G": "Newtonian gravitational constant (m³ kg⁻¹ s⁻²)",
        "h": "Planck constant (J·s)",
        "hbar": "Reduced Planck constant ħ = h / 2π (J·s)",
        "k": "Boltzmann constant (J/K)",
        "Na": "Avogadro constant (mol⁻¹)",
        "R": "Universal molar gas constant (J·mol⁻¹·K⁻¹)",
        "e_charge": "Elementary electric charge (C)",
        "me": "Electron rest mass (kg)",
        "mp": "Proton rest mass (kg)",
        "mn": "Neutron rest mass (kg)",
        "epsilon0": "Electric constant / vacuum permittivity (F/m)",
        "mu0": "Magnetic constant / vacuum permeability (N/A²)",
        "sigma": "Stefan-Boltzmann constant (W·m⁻²·K⁻⁴)",
        "g": "Standard acceleration of gravity (m/s²)",
        "atm": "Standard atmospheric pressure (Pa)",
    }
    return [(k, v, descriptions.get(k, "")) for k, v in ALLOWED_CONSTS.items()]
