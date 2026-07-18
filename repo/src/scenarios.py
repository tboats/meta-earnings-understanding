# src/scenarios.py
"""
Assumptions and parameters for Meta Platforms financial model scenarios.
"""

def get_scenario_assumptions(scenario_name, q2_revenue=None, q2_margin=None, capex_guidance=None):
    """
    Returns financial assumptions for 2026-2030 based on the scenario name and 
    optional Q2 2026 adjustments.
    """
    # Baseline actuals (Q1 2026)
    q1_revenue_actual = 56.31
    q1_operating_income_actual = 22.87
    q1_capex_actual = 18.997
    q1_da_actual = 5.999
    
    # Estimate Q2 2026 based on inputs or defaults
    q2_rev = q2_revenue if q2_revenue is not None else 59.5  # Midpoint of $58B - $61B
    q2_op_margin = q2_margin if q2_margin is not None else 0.41  # Q1 actual margin
    q2_op_inc = q2_rev * q2_op_margin
    
    # 2026 Full Year projection helper
    # We will build FY 2026 as Q1 (actual) + Q2 (projected/actual) + H2 (projected based on scenario)
    
    if scenario_name == "optimistic":
        # H2 growth rate (YoY relative to H2 2025)
        h2_growth_2026 = 0.28
        h2_margin_2026 = 0.43
        
        # 2026 Projections
        # H2 2025 revenue was roughly total 2025 revenue ($200.97B) - Q1 ($42.32B) - Q2 ($47.52B) = $111.13B
        h2_revenue_2026 = 111.13 * (1 + h2_growth_2026)
        revenue_2026 = q1_revenue_actual + q2_rev + h2_revenue_2026
        
        h2_op_income_2026 = h2_revenue_2026 * h2_margin_2026
        op_income_2026 = q1_operating_income_actual + q2_op_inc + h2_op_income_2026
        
        capex_2026 = capex_guidance if capex_guidance is not None else 130.0  # Midpoint of $125B - $145B
        
        # 2027-2030 growth and margin assumptions
        revenue_growth = [0.22, 0.20, 0.18, 0.15]  # 2027, 2028, 2029, 2030
        operating_margins = [0.38, 0.40, 0.42, 0.43]
        
        # CapEx ramp down as infrastructure stabilizes
        capex_projections = [120.0, 105.0, 90.0, 80.0]  # 2027, 2028, 2029, 2030
        
        # Reality Labs operating income (losses narrowing to profit)
        rl_losses = [-18.0, -15.0, -10.0, -4.0, 2.0]  # 2026, 2027, 2028, 2029, 2030
        
        # Valuation multiples in 2030
        exit_pe = 30.0
        exit_ev_ebitda = 20.0
        terminal_growth = 0.025
        
    elif scenario_name == "pessimistic":
        # H2 growth rate (YoY)
        h2_growth_2026 = 0.10
        h2_margin_2026 = 0.32
        
        # 2026 Projections
        h2_revenue_2026 = 111.13 * (1 + h2_growth_2026)
        revenue_2026 = q1_revenue_actual + q2_rev + h2_revenue_2026
        
        h2_op_income_2026 = h2_revenue_2026 * h2_margin_2026
        op_income_2026 = q1_operating_income_actual + q2_op_inc + h2_op_income_2026
        
        capex_2026 = capex_guidance if capex_guidance is not None else 140.0  # High end of guidance
        
        # 2027-2030 growth and margin assumptions
        revenue_growth = [0.05, 0.03, 0.02, 0.02]
        operating_margins = [0.28, 0.25, 0.22, 0.20]
        
        # CapEx stays high due to competitive pressure
        capex_projections = [135.0, 125.0, 115.0, 105.0]
        
        # Reality Labs losses stay elevated
        rl_losses = [-20.0, -20.0, -18.0, -18.0, -18.0]
        
        # Valuation multiples in 2030
        exit_pe = 14.0
        exit_ev_ebitda = 8.0
        terminal_growth = 0.010
        
    else:  # Baseline / Consensus
        h2_growth_2026 = 0.18
        h2_margin_2026 = 0.38
        
        h2_revenue_2026 = 111.13 * (1 + h2_growth_2026)
        revenue_2026 = q1_revenue_actual + q2_rev + h2_revenue_2026
        
        h2_op_income_2026 = h2_revenue_2026 * h2_margin_2026
        op_income_2026 = q1_operating_income_actual + q2_op_inc + h2_op_income_2026
        
        capex_2026 = capex_guidance if capex_guidance is not None else 135.0
        
        revenue_growth = [0.12, 0.10, 0.08, 0.08]
        operating_margins = [0.34, 0.35, 0.35, 0.36]
        capex_projections = [125.0, 110.0, 100.0, 90.0]
        rl_losses = [-19.0, -18.0, -16.0, -14.0, -12.0]
        
        exit_pe = 22.0
        exit_ev_ebitda = 14.0
        terminal_growth = 0.020

    # Build year-by-year projections list for 2026-2030
    years = [2026, 2027, 2028, 2029, 2030]
    
    rev_proj = [revenue_2026]
    for g in revenue_growth:
        rev_proj.append(rev_proj[-1] * (1 + g))
        
    op_inc_proj = [op_income_2026]
    for i, m in enumerate(operating_margins):
        op_inc_proj.append(rev_proj[i+1] * m)
        
    capex_proj = [capex_2026] + capex_projections
    
    # Depreciation and Amortization (D&A)
    # Model D&A growing as past CapEx is recognized
    da_proj = [25.0]  # Q1 actual was 6.0, so ~25B for FY2026 is reasonable
    for i in range(1, 5):
        # D&A is estimated as prior D&A + 20% of previous year's CapEx
        da_proj.append(da_proj[-1] + 0.20 * capex_proj[i-1])

    return {
        "years": years,
        "revenue": rev_proj,
        "operating_income": op_inc_proj,
        "capex": capex_proj,
        "da": da_proj,
        "rl_loss": rl_losses,
        "exit_pe": exit_pe,
        "exit_ev_ebitda": exit_ev_ebitda,
        "terminal_growth": terminal_growth,
        "tax_rate": 0.16,  # Meta's long-term tax rate range
        "wacc": 0.090,
        "shares_outstanding": 2.55,  # Billions
        "net_cash": 22.44  # $81.18B cash - $58.74B debt (billions)
    }
