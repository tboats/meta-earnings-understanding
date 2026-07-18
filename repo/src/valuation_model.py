# src/valuation_model.py
"""
Engine to calculate financial projections, DCF, and multiples-based valuation for Meta Platforms.
"""

def run_valuation(assumptions):
    """
    Computes detailed projections, DCF valuation, and Multiple-based valuations.
    """
    years = assumptions["years"]
    revenue = assumptions["revenue"]
    operating_income = assumptions["operating_income"]
    capex = assumptions["capex"]
    da = assumptions["da"]
    tax_rate = assumptions["tax_rate"]
    wacc = assumptions["wacc"]
    shares = assumptions["shares_outstanding"]
    net_cash = assumptions["net_cash"]
    
    # 1. Projections
    ebitda = []
    ebiat = []
    fcf = []
    pv_fcf = []
    
    for i in range(len(years)):
        yr = years[i]
        rev = revenue[i]
        op = operating_income[i]
        cap = capex[i]
        dep = da[i]
        
        # EBITDA = EBIT + D&A
        eb = op + dep
        ebitda.append(eb)
        
        # EBIAT = EBIT * (1 - tax)
        ebt = op * (1 - tax_rate)
        ebiat.append(ebt)
        
        # FCF = EBIAT + D&A - CapEx
        fc = ebt + dep - cap
        fcf.append(fc)
        
        # PV of FCF = FCF / (1 + WACC)^t
        t = i + 1  # 2026 is year 1
        discount_factor = (1 + wacc) ** t
        pv_fc = fc / discount_factor
        pv_fcf.append(pv_fc)
        
    sum_pv_fcf = sum(pv_fcf)
    
    # 2. DCF Terminal Value
    terminal_growth = assumptions["terminal_growth"]
    fcf_2030 = fcf[-1]
    terminal_value = fcf_2030 * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal_value = terminal_value / ((1 + wacc) ** 5)
    
    # DCF Enterprise Value
    dcf_ev = sum_pv_fcf + pv_terminal_value
    dcf_equity_val = dcf_ev + net_cash
    dcf_price = dcf_equity_val / shares
    
    # 3. Multiple-based valuations
    exit_pe = assumptions["exit_pe"]
    exit_ev_ebitda = assumptions["exit_ev_ebitda"]
    
    # PE Multiple-based target price (Net Income proxy = EBIAT)
    net_income_2030 = ebiat[-1]
    target_equity_val_pe_2030 = net_income_2030 * exit_pe + net_cash
    target_price_pe_2030 = target_equity_val_pe_2030 / shares
    pv_target_price_pe = target_price_pe_2030 / ((1 + wacc) ** 5)
    
    # EV/EBITDA Multiple-based target price
    ebitda_2030 = ebitda[-1]
    target_ev_ebitda_2030 = ebitda_2030 * exit_ev_ebitda
    target_equity_val_ebitda_2030 = target_ev_ebitda_2030 + net_cash
    target_price_ebitda_2030 = target_equity_val_ebitda_2030 / shares
    pv_target_price_ebitda = target_price_ebitda_2030 / ((1 + wacc) ** 5)
    
    return {
        "years": years,
        "revenue": revenue,
        "operating_income": operating_income,
        "capex": capex,
        "da": da,
        "ebitda": ebitda,
        "ebiat": ebiat,
        "fcf": fcf,
        "pv_fcf": pv_fcf,
        "sum_pv_fcf": sum_pv_fcf,
        "terminal_value": terminal_value,
        "pv_terminal_value": pv_terminal_value,
        "dcf_ev": dcf_ev,
        "dcf_equity_val": dcf_equity_val,
        "dcf_price": dcf_price,
        "exit_pe": exit_pe,
        "exit_ev_ebitda": exit_ev_ebitda,
        "target_price_pe_2030": target_price_pe_2030,
        "pv_target_price_pe": pv_target_price_pe,
        "target_price_ebitda_2030": target_price_ebitda_2030,
        "pv_target_price_ebitda": pv_target_price_ebitda,
        "shares": shares,
        "net_cash": net_cash,
        "wacc": wacc,
        "terminal_growth": terminal_growth
    }

def run_valuation_with_ranges(opt_assumptions, pes_assumptions, wacc_center, weight_opt_center):
    """
    Runs the model under near-term valuation sensitivity range conditions (order of $27/share delta):
    - Best Estimate: WACC = wacc_center, Terminal Growth = center
    - Min (Conservative): WACC = wacc_center + 0.05%, Terminal Growth = center - 0.1%
    - Max (Aggressive): WACC = wacc_center - 0.05%, Terminal Growth = center + 0.1%
    Weight remains constant to isolate operational and discount rate sensitivity.
    """
    # Best Estimate
    opt_base = opt_assumptions.copy()
    opt_base["wacc"] = wacc_center
    pes_base = pes_assumptions.copy()
    pes_base["wacc"] = wacc_center
    
    val_opt_base = run_valuation(opt_base)
    val_pes_base = run_valuation(pes_base)
    best_estimate = val_opt_base["dcf_price"] * weight_opt_center + val_pes_base["dcf_price"] * (1 - weight_opt_center)
    
    # Min (Conservative)
    opt_min = opt_assumptions.copy()
    opt_min["wacc"] = wacc_center + 0.0005
    opt_min["terminal_growth"] = opt_assumptions["terminal_growth"] - 0.001
    
    pes_min = pes_assumptions.copy()
    pes_min["wacc"] = wacc_center + 0.0005
    pes_min["terminal_growth"] = pes_assumptions["terminal_growth"] - 0.001
    
    val_opt_min = run_valuation(opt_min)
    val_pes_min = run_valuation(pes_min)
    range_min = val_opt_min["dcf_price"] * weight_opt_center + val_pes_min["dcf_price"] * (1 - weight_opt_center)
    
    # Max (Aggressive)
    opt_max = opt_assumptions.copy()
    opt_max["wacc"] = wacc_center - 0.0005
    opt_max["terminal_growth"] = opt_assumptions["terminal_growth"] + 0.001
    
    pes_max = pes_assumptions.copy()
    pes_max["wacc"] = wacc_center - 0.0005
    pes_max["terminal_growth"] = pes_assumptions["terminal_growth"] + 0.001
    
    val_opt_max = run_valuation(opt_max)
    val_pes_max = run_valuation(pes_max)
    range_max = val_opt_max["dcf_price"] * weight_opt_center + val_pes_max["dcf_price"] * (1 - weight_opt_center)
    
    return {
        "best_estimate": best_estimate,
        "range_min": range_min,
        "range_max": range_max,
        "val_opt_base": val_opt_base,
        "val_pes_base": val_pes_base
    }

