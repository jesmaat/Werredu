"""
tests/test_werredu_werr_core.py
===============================
Comprehensive Unit & Invariant Test Suite for Werredu v1.0
Verifying WERR v0.5.1 Core Integration, GAP-0331 Modular Algebra,
and Procedural Fractal Pedagogy (PFP) Operators.
"""

import os
import sys
import unittest
import math
import numpy as np

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import werr
from werr.engine import WerrEngine
from werr.datatypes import ChoiceQuestion, NoulQuestion, ScoreQuestion
from werr.modular_algebra import (
    constructive_extended_gcd,
    constructive_inverse_mod,
    is_unit_mod9,
    is_resonant_subideal_i3,
    neutralize_modular_perturbation,
    verify_gap0331_invariants,
)
from werr.pedagogy import (
    ObserverHorizonZPD,
    SemanticTokenDampingFilter,
    BiomimeticPerturbedJumpOperator,
    TAMAMeAssessmentComplementarity,
    tripod_harmonic_evaluation,
    mandelbrot_escape_velocity,
    compute_boundary_dispersion,
    X_UPPER,
    X_LOWER,
    T_DESC,
    MAX_ITER,
)


class TestWerrCoreEngine(unittest.TestCase):
    """Verifies that WERR core engine runs with 0 VRAM and expected v0.5.1 properties."""

    def setUp(self):
        self.engine = WerrEngine()

    def test_engine_version(self):
        self.assertEqual(werr.__version__, "0.5.1")

    def test_choice_evaluation(self):
        state = {"topic": "Educational Complexity", "boundary_mode": "Observer Horizon"}
        q = ChoiceQuestion(
            instructions="Which pedagogical principle formalizes ZPD at the boundary?",
            criteria=["Observer Horizon", "Random Guessing", "Unconstrained Noise"]
        )
        resp = self.engine.decide(state, {"pedagogy_choice": q})
        ans = resp.answers["pedagogy_choice"]
        self.assertIsNotNone(ans.choice)
        self.assertIn(ans.choice, ["Observer Horizon", "Random Guessing", "Unconstrained Noise"])
        self.assertGreater(ans.confidence, 0.0)

    def test_noul_evaluation(self):
        state = {"stability": True, "t_desc": 0.045}
        q = NoulQuestion(
            instructions="Is the Observer Horizon ZPD stable under T_desc = 0.045?",
            threshold=0.5
        )
        resp = self.engine.decide(state, {"is_stable": q})
        ans = resp.answers["is_stable"]
        self.assertIn(ans.decision, [True, False])
        self.assertGreaterEqual(ans.confidence, 0.0)
        self.assertLessEqual(ans.confidence, 1.0)


class TestGAP0331ModularAlgebra(unittest.TestCase):
    """Verifies GAP-0331 Z/9Z constructive modular arithmetic matching Lean 4."""

    def test_gap0331_invariants_verification(self):
        report = verify_gap0331_invariants(modulus=9)
        self.assertEqual(report["status"], "verified")
        self.assertEqual(report["phi_n"], 6)
        self.assertEqual(set(report["units_verified"].keys()), {1, 2, 4, 5, 7, 8})


    def test_resonant_subideal_i3(self):
        for z in (0, 3, 6):
            self.assertTrue(is_resonant_subideal_i3(z))
            with self.assertRaises(ValueError):
                constructive_inverse_mod(z, n=9)

    def test_multiplicative_units(self):
        for u in (1, 2, 4, 5, 7, 8):
            self.assertTrue(is_unit_mod9(u))
            inv = constructive_inverse_mod(u, n=9)
            self.assertEqual((u * inv) % 9, 1)

    def test_adversarial_neutralization(self):
        state = 4
        hostile_factor = 5  # unit in Z/9Z
        perturbed = (state * hostile_factor) % 9
        restored = neutralize_modular_perturbation(perturbed, hostile_factor, modulus=9)
        self.assertEqual(restored, state)


class TestPFPPedagogicalOperators(unittest.TestCase):
    """Verifies the Procedural Fractal Pedagogy (PFP / Werredu v1.0) operators."""

    def test_observer_horizon_coordinates(self):
        self.assertEqual(X_UPPER, complex(0.25, 0.18))
        self.assertEqual(X_LOWER, complex(0.25, -0.18))
        self.assertEqual(ObserverHorizonZPD.select_shoulder(True), X_UPPER)
        self.assertEqual(ObserverHorizonZPD.select_shoulder(False), X_LOWER)

    def test_semantic_token_damping_filter(self):
        filt = SemanticTokenDampingFilter(t_desc=T_DESC)
        shock = complex(0.10, 0.10)
        damped_distraction = filt.filter(shock, is_distraction=True)
        damped_curiosity = filt.filter(shock, is_distraction=False)

        # Distraction is attenuated by T_desc = 0.045
        self.assertAlmostEqual(damped_distraction.real, shock.real * 0.045, places=7)
        self.assertAlmostEqual(damped_distraction.imag, shock.imag * 0.045, places=7)
        # Curiosity admits baseline 0.26
        self.assertAlmostEqual(damped_curiosity.real, shock.real * 0.26, places=7)

    def test_biomimetic_perturbed_jump_operator(self):
        jump_op = BiomimeticPerturbedJumpOperator(radius=0.032)
        # Test across multiple student IDs and cycle steps
        for student_id in range(10):
            for step in range(10):
                c_new, residue = jump_op.compute_jump(student_id, step, X_UPPER)
                # Must always land in resonant sub-ideal I_3 = {0, 3, 6}
                self.assertIn(residue, {0, 3, 6})
                self.assertTrue(is_resonant_subideal_i3(residue))
                dist = abs(c_new - X_UPPER)
                self.assertAlmostEqual(dist, 0.032, places=6)

    def test_tripod_harmonic_evaluation(self):
        res = tripod_harmonic_evaluation(X_UPPER, zoom=12.0)
        self.assertIn("dark_ratio", res)
        self.assertIn("latency_ms", res)
        self.assertGreaterEqual(res["dark_ratio"], 0.0)
        self.assertLessEqual(res["dark_ratio"], 1.0)
        self.assertLess(res["latency_ms"], 10.0)  # Sub-10ms edge execution

    def test_tamame_complementarity(self):
        b, s = TAMAMeAssessmentComplementarity.evaluate(0.68)
        self.assertAlmostEqual(b + s, 1.0, places=9)
        self.assertAlmostEqual(b, 0.68, places=9)
        self.assertAlmostEqual(s, 0.32, places=9)

    def test_boundary_dispersion_and_orbital_entropy(self):
        from werr.pedagogy import compute_boundary_dispersion, compute_orbital_recurrence_entropy
        
        # Test Factory Model origin c = 0
        dm_0, disp_0, orb_0 = compute_boundary_dispersion(0j, r_patch=0.22)
        self.assertEqual(dm_0, 1.0)
        self.assertEqual(disp_0, 0.0)
        self.assertEqual(orb_0, 0.0)

        # Test ZPD Shoulder X_upper = 0.25 + 0.18i
        dm_x, disp_x, orb_x = compute_boundary_dispersion(X_UPPER, r_patch=0.22)
        # Boundary dispersion must exceed the disequilibrium threshold 0.08
        self.assertGreater(disp_x, 0.08)
        self.assertAlmostEqual(disp_x, 0.4171, places=3)
        # Orbital recurrence variance must be strictly positive (spiral attractor dynamic)
        self.assertGreater(orb_x, 0.0)
        self.assertGreater(compute_orbital_recurrence_entropy(X_UPPER), 0.0)


if __name__ == "__main__":
    unittest.main()
