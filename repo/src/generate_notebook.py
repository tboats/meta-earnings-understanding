# src/generate_notebook.py
"""
Script to generate the Jupyter Notebook meta_valuation.ipynb programmatically.
"""
import json
import os

def create_notebook():
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Meta Platforms (META) Financial Model & Valuation\n",
                    "This notebook builds a first-principles financial model of Meta Platforms, Inc. (META) as of July 2026. \n",
                    "We analyze Meta's valuation under two primary AI scenarios:\n",
                    "1. **Optimistic AI Scenario**: Meta and Google dominate the AI frontier; Llama becomes the open-source standard; AI-driven personalization and WhatsApp messaging explode.\n",
                    "2. **Pessimistic AI Scenario**: Heavy CapEx buildout fails to monetize efficiently; depreciation charges crush operating margins; Reality Labs remains a persistent cash drain.\n",
                    "\n",
                    "We model projections for 2026-2030 and perform a Discounted Cash Flow (DCF) and Multiples-based valuation."
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 📊 1. Business Upsides & Downsides (First Principles)\n",
                    "\n",
                    "### 🚀 Upsides:\n",
                    "- **Unmatched Network Effects**: 3.56 billion Daily Active People (DAP) across Facebook, Instagram, Messenger, and WhatsApp.\n",
                    "- **AI Monetization Engine**: AI recommendations (Reels) and ad personalization (Advantage+) drive click-through-rates (CTR) and pricing power.\n",
                    "- **Commoditizing the AI Stack**: By open-sourcing Llama, Meta forces competitor API prices to zero, avoiding third-party tolls and making its own ad platform the primary beneficiary of cheaper compute.\n",
                    "- **WhatsApp Business Messaging**: Automated AI agents on WhatsApp unlock B2B customer service revenue.\n",
                    "- **Ambient AI Hardware**: Ray-Ban Meta smart glasses serve as a stealth gateway to consumer AR/VR, driving ecosystem lock-in.\n",
                    "\n",
                    "### ⚠️ Downsides:\n",
                    "- **Historic CapEx Ramps**: Guiding $125B - $145B in 2026 CapEx. If monetization stalls, massive depreciation charges will crush operating margins.\n",
                    "- **Reality Labs Cash Burn**: Reality Labs lost $19.2 billion in FY 2025, showing zero near-term operating profitability.\n",
                    "- **Ad Cyclicality & Competition**: Total dependence on advertising makes Meta vulnerable to macro downturns and competition from TikTok/Amazon.\n",
                    "- **Regulatory & Privacy Drag**: Ongoing FTC antitrust lawsuits and EU regulatory compliance restrict data usage."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Import core libraries and path adjustments\n",
                    "import sys\n",
                    "import os\n",
                    "sys.path.append(os.path.abspath('src'))\n",
                    "\n",
                    "import pandas as pd\n",
                    "from scenarios import get_scenario_assumptions\n",
                    "from valuation_model import run_valuation\n",
                    "print(\"Libraries successfully imported!\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 📈 2. Scenario Projections (2026-2030)\n",
                    "Let's load the assumptions and compute projections for both **Optimistic** and **Pessimistic** AI scenarios."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Run calculations for both scenarios\n",
                    "opt_assumptions = get_scenario_assumptions(\"optimistic\")\n",
                    "pes_assumptions = get_scenario_assumptions(\"pessimistic\")\n",
                    "base_assumptions = get_scenario_assumptions(\"base\")\n",
                    "\n",
                    "opt_results = run_valuation(opt_assumptions)\n",
                    "pes_results = run_valuation(pes_assumptions)\n",
                    "base_results = run_valuation(base_assumptions)\n",
                    "\n",
                    "def build_summary_df(results):\n",
                    "    df = pd.DataFrame({\n",
                    "        \"Revenue ($B)\": results[\"revenue\"],\n",
                    "        \"Operating Income ($B)\": results[\"operating_income\"],\n",
                    "        \"EBITDA ($B)\": results[\"ebitda\"],\n",
                    "        \"CapEx ($B)\": results[\"capex\"],\n",
                    "        \"D&A ($B)\": results[\"da\"],\n",
                    "        \"Free Cash Flow ($B)\": results[\"fcf\"],\n",
                    "        \"PV of FCF ($B)\": results[\"pv_fcf\"]\n",
                    "    }, index=results[\"years\"])\n",
                    "    return df.round(2)\n",
                    "\n",
                    "print(\"--- OPTIMISTIC SCENARIO PROJECTIONS ---\")\n",
                    "display(build_summary_df(opt_results))\n",
                    "\n",
                    "print(\"\\n--- PESSIMISTIC SCENARIO PROJECTIONS ---\")\n",
                    "display(build_summary_df(pes_results))"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 🔍 3. Valuation Results Comparison\n",
                    "Let's compare the implied stock price under DCF and Multiples (P/E, EV/EBITDA) methodologies. \n",
                    "Current stock price is **$670.27**."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "valuation_comparison = pd.DataFrame({\n",
                    "    \"Metric\": [\n",
                    "        \"DCF Share Price (Intrinsic Value)\",\n",
                    "        \"Exit P/E Share Price (PV of Target)\",\n",
                    "        \"Exit EV/EBITDA Share Price (PV of Target)\",\n",
                    "        \"Exit P/E Multiple Used\",\n",
                    "        \"Exit EV/EBITDA Multiple Used\",\n",
                    "        \"Terminal Growth Rate (%)\"\n",
                    "    ],\n",
                    "    \"Pessimistic Scenario\": [\n",
                    "        f\"${pes_results['dcf_price']:.2f}\",\n",
                    "        f\"${pes_results['pv_target_price_pe']:.2f}\",\n",
                    "        f\"${pes_results['pv_target_price_ebitda']:.2f}\",\n",
                    "        f\"{pes_results['exit_pe']}x\",\n",
                    "        f\"{pes_results['exit_ev_ebitda']}x\",\n",
                    "        f\"{pes_results['terminal_growth'] * 100:.1f}%\"\n",
                    "    ],\n",
                    "    \"Baseline (Consensus) \": [\n",
                    "        f\"${base_results['dcf_price']:.2f}\",\n",
                    "        f\"${base_results['pv_target_price_pe']:.2f}\",\n",
                    "        f\"${base_results['pv_target_price_ebitda']:.2f}\",\n",
                    "        f\"{base_results['exit_pe']}x\",\n",
                    "        f\"{base_results['exit_ev_ebitda']}x\",\n",
                    "        f\"{base_results['terminal_growth'] * 100:.1f}%\"\n",
                    "    ],\n",
                    "    \"Optimistic Scenario\": [\n",
                    "        f\"${opt_results['dcf_price']:.2f}\",\n",
                    "        f\"${opt_results['pv_target_price_pe']:.2f}\",\n",
                    "        f\"${opt_results['pv_target_price_ebitda']:.2f}\",\n",
                    "        f\"{opt_results['exit_pe']}x\",\n",
                    "        f\"{opt_results['exit_ev_ebitda']}x\",\n",
                    "        f\"{opt_results['terminal_growth'] * 100:.1f}%\"\n",
                    "    ]\n",
                    "})\n",
                    "\n",
                    "display(valuation_comparison.set_index(\"Metric\"))\n",
                    "\n",
                    "from valuation_model import run_valuation_with_ranges\n",
                    "ranges = run_valuation_with_ranges(opt_assumptions, pes_assumptions, wacc_center=0.090, weight_opt_center=0.50)\n",
                    "print(f\"Weighted Intrinsic Price (Best Estimate): ${ranges['best_estimate']:.2f}\")\n",
                    "print(f\"Valuation Range (WACC 8.5%-9.5%, Weight 40%-60%): ${ranges['range_min']:.2f} - ${ranges['range_max']:.2f}\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 📈 4. Charting the Scenarios\n",
                    "Let's visualize the projected revenue and Free Cash Flows."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import matplotlib.pyplot as plt\n",
                    "\n",
                    "plt.figure(figsize=(12, 5))\n",
                    "\n",
                    "# Plot Revenue\n",
                    "plt.subplot(1, 2, 1)\n",
                    "plt.plot(opt_results[\"years\"], opt_results[\"revenue\"], 'g-o', label=\"Optimistic\")\n",
                    "plt.plot(base_results[\"years\"], base_results[\"revenue\"], 'b-o', label=\"Baseline\")\n",
                    "plt.plot(pes_results[\"years\"], pes_results[\"revenue\"], 'r-o', label=\"Pessimistic\")\n",
                    "plt.title(\"Projected Revenue ($B)\")\n",
                    "plt.xlabel(\"Year\")\n",
                    "plt.ylabel(\"Revenue ($B)\")\n",
                    "plt.grid(True, linestyle=\"--\", alpha=0.5)\n",
                    "plt.legend()\n",
                    "\n",
                    "# Plot Free Cash Flow\n",
                    "plt.subplot(1, 2, 2)\n",
                    "plt.plot(opt_results[\"years\"], opt_results[\"fcf\"], 'g-o', label=\"Optimistic\")\n",
                    "plt.plot(base_results[\"years\"], base_results[\"fcf\"], 'b-o', label=\"Baseline\")\n",
                    "plt.plot(pes_results[\"years\"], pes_results[\"fcf\"], 'r-o', label=\"Pessimistic\")\n",
                    "plt.title(\"Projected Free Cash Flow ($B)\")\n",
                    "plt.xlabel(\"Year\")\n",
                    "plt.ylabel(\"FCF ($B)\")\n",
                    "plt.grid(True, linestyle=\"--\", alpha=0.5)\n",
                    "plt.legend()\n",
                    "\n",
                    "plt.tight_layout()\n",
                    "plt.show()"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

    # Save to workspace root or repo/
    notebook_path = "Projects/meta-valuation/repo/meta_valuation.ipynb"
    with open(notebook_path, "w") as f:
        json.dump(notebook, f, indent=2)
    print(f"✅ Successfully wrote notebook to {notebook_path}")

if __name__ == "__main__":
    create_notebook()
