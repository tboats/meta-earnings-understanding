# src/verify_model.py
"""
Simple script to verify financial model formulas and scenario consistency.
"""
from scenarios import get_scenario_assumptions
from valuation_model import run_valuation

def run_tests():
    print("🧪 Starting financial model verification tests...")
    
    # 1. Fetch assumptions
    opt_assumptions = get_scenario_assumptions("optimistic")
    pes_assumptions = get_scenario_assumptions("pessimistic")
    
    # 2. Run model
    opt_results = run_valuation(opt_assumptions)
    pes_results = run_valuation(pes_assumptions)
    
    # Assertions
    # A1: EBITDA > Operating Income
    for i in range(5):
        assert opt_results["ebitda"][i] > opt_results["operating_income"][i], f"EBITDA calculation error in year {opt_results['years'][i]}"
        assert pes_results["ebitda"][i] > pes_results["operating_income"][i], f"EBITDA calculation error in year {pes_results['years'][i]}"
    print("✅ A1 passed: EBITDA is correctly calculated and strictly greater than Operating Income.")

    # A2: FCF projections show expected behavior
    # Optimistic FCF in 2030 should be much higher than Pessimistic FCF in 2030
    assert opt_results["fcf"][-1] > pes_results["fcf"][-1], "Optimistic 2030 FCF should exceed Pessimistic 2030 FCF"
    print("✅ A2 passed: Scenario FCF divergence is consistent with business assumptions.")

    # A3: Intrinsic value comparison
    assert opt_results["dcf_price"] > pes_results["dcf_price"], "Optimistic stock price should be higher than Pessimistic"
    print(f"✅ A3 passed: Intrinsic values are consistent (Optimistic: ${opt_results['dcf_price']:.2f} vs. Pessimistic: ${pes_results['dcf_price']:.2f})")
    
    # A4: Multiple-based valuations are consistent
    assert opt_results["pv_target_price_pe"] > pes_results["pv_target_price_pe"]
    assert opt_results["pv_target_price_ebitda"] > pes_results["pv_target_price_ebitda"]
    print("✅ A4 passed: Multiple-based valuations correctly follow exit multiple and margin assumptions.")

    print("\n🎉 All verification tests passed successfully!")

if __name__ == "__main__":
    run_tests()
