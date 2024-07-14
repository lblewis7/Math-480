import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Algebra.BigOperators.Group.Finset

import Init.Data.Int.DivModLemmas
import Init.Data.Nat.Lemmas

/- Supply proofs for 2 out of the 3 assignments.
   Do all 3 for 5 points of extra credit.

   All assignments can be proven through induction and appropriate use of library functions and logic operations.
-/

-- Assignment 1: Show that 2^n % 7 = 1, 2, or 4 for all n.
-- use induction (OR assume one of the 3 cases, prove that it shifts)
theorem assignment1 : ∀ n:ℕ, 2^n % 7 = 1 ∨ 2^n % 7 = 2 ∨ 2^n % 7 = 4 := by
  intro n
  induction n with
  | zero => 
    simp
  | succ n ih =>
    cases ih with
    | inl h_left =>
      right
      left
      have h_l_1 : 2^(n + 1) % 7 = (2 * 2^n) % 7 := by ring_nf
      rw [h_l_1]
      have h_l_2 : (2 * (2^n)) % 7 = 2 % 7 * (2 ^ n % 7) % 7 := Nat.mul_mod 2 (2^n) 7
      rw [h_l_2]
      have h_l_3 : 2 % 7 * (2 ^ n % 7) % 7 = (2%7 * 1) % 7 := by rw [h_left]
      rw [h_l_3]
      
      -- have h_l_4 :(2%7 * 1) % 7 = 2 := by ring
      
      /- calc 2 ^ (n + 1) % 7 = (2 * 2^n) % 7 := ring
                         _ = (2%7 * 2^n%7) % 7 := Int.mul_emod
                         _ = (2%7 * 1) % 7 := rw [h_left]
                         _ = 2 := ring -/
    
    | inr h_mid_right =>
      cases h_mid_right with
      | inl h_mid =>
        right
        right
        have h_l_1 : 2^(n + 1) % 7 = (2 * 2^n) % 7 := by ring_nf
        rw [h_l_1]
        have h_l_2 : (2 * (2^n)) % 7 = 2 % 7 * (2 ^ n % 7) % 7 := Nat.mul_mod 2 (2^n) 7
        rw [h_l_2]
        have h_l_3 : 2 % 7 * (2 ^ n % 7) % 7 = (2%7 * 2) % 7 := by rw [h_mid]
        rw [h_l_3]
      | inr h_right =>
        left
        have h_l_1 : 2^(n + 1) % 7 = (2 * 2^n) % 7 := by ring_nf
        rw [h_l_1]
        have h_l_2 : (2 * (2^n)) % 7 = 2 % 7 * (2 ^ n % 7) % 7 := Nat.mul_mod 2 (2^n) 7
        rw [h_l_2]
        have h_l_3 : 2 % 7 * (2 ^ n % 7) % 7 = (2%7 * 4) % 7 := by rw [h_right]
        rw [h_l_3]

-- Assignment 2: Show that (1-x)*(1+x+x^2+...+x^{n-1}) = (1-x^n)
-- use induction w/ basic algebra [distributivity] - search for theorems to deal with finset, either on loogle or mathlib documentation
theorem assignment2
    (x:ℝ)
    : ∀ n:ℕ, (1-x)*(∑ i ∈ Finset.range n, x^i) = 1-x^n := by
  intro n
  induction n with
  | zero => 
    ring_nf
    rw [Finset.range_zero]
    simp
  | succ n ih =>
    rw [mul_comm]
    rw [Finset.range_add_one]
    rw [Finset.sum_insert]
    rw [add_mul]
    rw [add_comm]
    rw [mul_comm]
    rw [ih]
    ring
    simp -- tried using "exact [Finset.not_mem_range_self]" since this is, character for character, what the goal is here, though it didn't recognize it. 

-- Assignment 3: Show that if a_0 = 0, a_{n+1} = 2*a_n+1 then a_n = 2^n-1.
-- use induction
theorem assignment3
    (a: ℕ → ℝ) (h_zero: a 0 = 0) (h_rec: ∀ n:ℕ, a (n+1) = 2 * (a n) + 1) -- 0, 1, 3, 7 ... 
    : ∀ n:ℕ, a n = 2^n - 1 := by
  intro n
  induction n with
  | zero => 
    rw [h_zero]
    simp
  | succ n ih =>
    rw [h_rec]
    rw [ih]
    ring
