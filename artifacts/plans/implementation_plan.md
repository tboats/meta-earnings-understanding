# Financial Model and Valuation for Meta Platforms (META)

Build a first-principles financial model and interactive valuation tool for Meta Platforms (META) to assess its stock value under optimistic and pessimistic AI integration scenarios. The tool will react to the upcoming Q2 2026 earnings results and updated guidance to recalculate intrinsic value and target price ranges.

## User Review Required

> [!IMPORTANT]
> **First-Principles Modeling Parameters**
> 1. We model Meta's revenue by separating **Family of Apps (FoA)** and **Reality Labs (RL)**.
> 2. FoA revenue is driven by Family Daily Active People (DAP), Average Revenue Per Person (ARPP), and ad monetization efficiency (impressions growth vs. CPM).
> 3. Reality Labs is modeled as a capital sink with long-term option value or potential optimization.
> 4. The massive CapEx ramp ($125B - $145B guided for FY 2026) is modeled explicitly to see how depreciation impacts earnings and how capital cash outflow reduces free cash flow.
> Please review the details of the scenarios and valuation methodology.

## Open Questions

> [!NOTE]
> **Key Inputs & Settings**
> - **Valuation Horizon**: We propose a 5-year detailed forecast (2026-2030) followed by a terminal value calculation (DCF and Multiple-based).
> - **Discount Rate (WACC)**: We propose a WACC of 9.0% based on Meta's low-beta equity profile, balanced by high capital intensity.
> - **Terminal Growth Rate**: Proposed 2.5% in the baseline and optimistic scenarios, and 1.0% in the pessimistic scenario.

## Proposed Changes

### Project Configuration

#### [MODIFY] project.md
Update the project metadata, goal, and Definition of Done.

### Task Backlog

#### [MODIFY] backlog.md
Populate the backlog with tasks mapping to plan execution.

### Financial Model Implementation

#### [NEW] scenarios.py
Defines the parameters and financial projections for:
1. **Optimistic AI Scenario**:
   - High ARPP growth (Reels optimization, Advantage+ ad platform, AI agent monetization on WhatsApp/Messenger).
   - High margin retention despite CapEx.
   - Reality Labs losses peaking and declining.
   - Target terminal P/E multiple: 28x-32x.
2. **Pessimistic AI Scenario**:
   - Saturation of DAP, CPM declines due to competition.
   - Massive depreciation charge crushing operating margins.
   - Reality Labs continues to burn $18B-$20B/year.
   - Target terminal P/E multiple: 12x-15x.

#### [NEW] valuation_model.py
The core modeling engine that:
- Projects Income Statement, CapEx, D&A, and Free Cash Flow.
- Implements two valuation methodologies:
  - **Discounted Cash Flow (DCF)**.
  - **EV/EBITDA and P/E Multiple-based Valuation**.
- Integrates a baseline based on Q1 2026 actuals and current FY 2026 guidance.

#### [NEW] run_model.py
The interactive command-line interface. It will:
1. Explain the upsides and downsides of Meta's business.
2. Run baseline valuations for optimistic/pessimistic scenarios using current guidance.
3. Prompt the user to input the Q2 2026 actual earnings (Revenue, Operating Margin, updated CapEx guidance) once released at the end of July.
4. Dynamically compute the updated valuation ranges and implied stock prices.

## Verification Plan

### Automated Tests
- Implement validation checks inside `repo/src/valuation_model.py` to ensure balance sheet identity and cash flow reconciliation.
- Create a test script `repo/tests/test_model.py` to verify DCF calculations against known mathematical inputs.

### Manual Verification
- Run the interactive CLI to verify it outputs readable, detailed tables for both scenarios.
- Verify sensitivity analyses for WACC and terminal growth rates.
