# run_model.py
"""
Interactive CLI for Meta Platforms (META) Financial Model and Valuation.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from scenarios import get_scenario_assumptions
from valuation_model import run_valuation

def print_banner():
    print("=" * 60)
    print("      META PLATFORMS (META) FIRST-PRINCIPLES FINANCIAL MODEL")
    print("=" * 60)
    print("Current Local Time: July 2026")
    print("Current META Stock Price: $670.27")
    print("Diluted Shares Outstanding: 2.55B")
    print("Net Cash Balance: $22.44B ($81.18B cash - $58.74B debt)")
    print("=" * 60)

def print_business_analysis():
    print("\n--- BUSINESS UPSIDES & RISK ANALYSIS ---")
    print("\n🚀 UPSIDES:")
    print("  * AI Monetization (FoA): Reels recommendations and Advantage+ drive higher CTR/CPM.")
    print("  * Llama Open-Source: Commoditizes competitor API stacks, avoiding third-party tolls.")
    print("  * WhatsApp Messaging: Agentic AI customer bots convert messaging network into a B2B goldmine.")
    print("  * Ambient Hardware: Smart glasses serve as consumer gateways to AR/VR and AI assistant lock-in.")
    print("\n⚠️ RISKS & DOWNSIDES:")
    print("  * Capital Spend Drag: $125B-$145B CapEx guidance for FY 2026 will drive massive depreciation.")
    print("  * FCF Compression: Negative or low FCF in 2026 due to intensive infrastructure investment.")
    print("  * Reality Labs Losses: Flat -$18B to -$20B operating loss per year.")
    print("  * Regulation: FTC antitrust actions and privacy compliance remain persistent headwind.")
    print("-" * 60)

def display_scenario_summary(opt, pes, base):
    print("\n" + "=" * 60)
    print("                 VALUATION RESULTS COMPARISON")
    print("=" * 60)
    print(f"{'Methodology':<35} | {'Pessimistic':<12} | {'Baseline':<12} | {'Optimistic':<12}")
    print("-" * 77)
    print(f"{'DCF Intrinsic Share Price':<35} | ${pes['dcf_price']:<11.2f} | ${base['dcf_price']:<11.2f} | ${opt['dcf_price']:<11.2f}")
    print(f"{'Exit P/E Share Price (PV)':<35} | ${pes['pv_target_price_pe']:<11.2f} | ${base['pv_target_price_pe']:<11.2f} | ${opt['pv_target_price_pe']:<11.2f}")
    print(f"{'Exit EV/EBITDA Share Price (PV)':<35} | ${pes['pv_target_price_ebitda']:<11.2f} | ${base['pv_target_price_ebitda']:<11.2f} | ${opt['pv_target_price_ebitda']:<11.2f}")
    print("-" * 77)
    print(f"{'Exit P/E Multiple Used':<35} | {pes['exit_pe']:<11} | {base['exit_pe']:<11} | {opt['exit_pe']:<11}")
    print(f"{'Exit EV/EBITDA Multiple Used':<35} | {pes['exit_ev_ebitda']:<11} | {base['exit_ev_ebitda']:<11} | {opt['exit_ev_ebitda']:<11}")
    print(f"{'Terminal Growth Rate':<35} | {pes['terminal_growth']*100:<10.1f}% | {base['terminal_growth']*100:<10.1f}% | {opt['terminal_growth']*100:<10.1f}%")
    print("=" * 60)

def run_interactive():
    print_banner()
    print_business_analysis()
    
    # 1. Run baseline models
    opt_base = get_scenario_assumptions("optimistic")
    pes_base = get_scenario_assumptions("pessimistic")
    base_base = get_scenario_assumptions("base")
    
    opt_res = run_valuation(opt_base)
    pes_res = run_valuation(pes_base)
    base_res = run_valuation(base_base)
    
    print("\n--- BASELINE MODEL VALUATIONS (Using current Q1/FY2026 guidance) ---")
    display_scenario_summary(opt_res, pes_res, base_res)
    
    from valuation_model import run_valuation_with_ranges
    ranges = run_valuation_with_ranges(opt_base, pes_base, wacc_center=0.090, weight_opt_center=0.50)
    print("\n--- INTRINSIC VALUE RANGE (WACC: 8.5% - 9.5% | Weight: 40% - 60% Optimistic) ---")
    print(f"  * Best Estimate: ${ranges['best_estimate']:.2f}")
    print(f"  * Range:         ${ranges['range_min']:.2f} - ${ranges['range_max']:.2f}")
    
    # 2. Ask if user wants to input Q2 actuals
    print("\n[Optional] Update model with Q2 2026 Earnings Results (Late July Release)")
    try:
        choice = input("Do you want to override inputs with Q2 actuals? (y/N): ").strip().lower()
        if choice == 'y':
            q2_rev = float(input("Enter actual Q2 2026 Revenue ($B) (e.g. 60.5): "))
            q2_margin = float(input("Enter actual Q2 Operating Margin (%) (e.g. 42.0): ")) / 100.0
            capex = float(input("Enter updated FY 2026 CapEx guidance ($B) (e.g. 130.0): "))
            wacc = float(input("Enter WACC/Discount Rate (%) (default 9.0): ") or "9.0") / 100.0
            
            # Recalculate
            opt_adj = get_scenario_assumptions("optimistic", q2_rev, q2_margin, capex)
            pes_adj = get_scenario_assumptions("pessimistic", q2_rev, q2_margin, capex)
            base_adj = get_scenario_assumptions("base", q2_rev, q2_margin, capex)
            
            opt_adj["wacc"] = wacc
            pes_adj["wacc"] = wacc
            base_adj["wacc"] = wacc
            
            opt_res_adj = run_valuation(opt_adj)
            pes_res_adj = run_valuation(pes_adj)
            base_res_adj = run_valuation(base_adj)
            
            print("\n--- UPDATED MODEL VALUATIONS (Based on Q2 Actuals) ---")
            display_scenario_summary(opt_res_adj, pes_res_adj, base_res_adj)
            
            ranges_adj = run_valuation_with_ranges(opt_adj, pes_adj, wacc_center=wacc, weight_opt_center=0.50)
            print("\n--- UPDATED VALUE RANGE (WACC +/- 0.5% | Weight: 40% - 60% Optimistic) ---")
            print(f"  * Best Estimate: ${ranges_adj['best_estimate']:.2f}")
            print(f"  * Range:         ${ranges_adj['range_min']:.2f} - ${ranges_adj['range_max']:.2f}")
        else:
            print("Using baseline assumptions.")
    except Exception as e:
        print(f"Error processing inputs: {e}. Reverting to baseline.")
    
    print("\n💡 Open Projects/meta-valuation/docs/interactive_model.html in your browser to interact with this model graphically.")

if __name__ == "__main__":
    run_interactive()
