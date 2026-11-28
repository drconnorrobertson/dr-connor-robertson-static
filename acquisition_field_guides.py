"""Buyer field guides for reviewing specific evidence in an acquisition."""
PUBLISHED = "2026-11-27"

TOPICS = [
    (
        "customer-concentration-risk", "How to Check Customer Concentration Before Buying a Business",
        "Measure customer concentration, reconcile account groups, and stress-test the loss of a major account before buying a business.",
        "A customer concentration ratio only helps if the customer groups and revenue period reflect the deal. Identify related entities, then test the consequences of losing one buying relationship.",
        [
            ("Calculate share by buying relationship", "Pull invoice-level revenue and group accounts under the entity that actually controls purchasing. Reconcile totals to the seller's revenue report. Calculate top-one and top-five shares for comparable periods and investigate sharp changes."),
            ("Stress-test cash contribution", "A fictional company records $2 million of annual revenue. Three billing entities share one purchasing decision and account for $420,000, or 21%. Losing that work at a 40% contribution margin would remove $168,000 before fixed-cost changes. Test that scenario against debt service and reserves."),
            ("Check transfer and renewal", "Review renewals, assignment, notice, and price terms with deal counsel. Ask who owns the relationship after close and what evidence supports the transition plan. Update your downside case if a signed agreement expires shortly after close."),
        ],
        ["Group related accounts", "Reconcile invoice totals", "Model lost contribution", "Verify renewal and transfer"],
        ("Is there a safe concentration threshold?", "The judgment depends on replacement time, contract durability, contribution, and reserves. Run the loss scenario in dollars before comparing the deal to a rule of thumb."),
        ["business-acquisition-due-diligence-checklist", "how-much-cash-to-buy-a-business"],
    ),
    (
        "owner-dependence-due-diligence", "Owner Dependence Due Diligence Before an Acquisition",
        "Map a seller's real responsibilities, estimate replacement capacity, and test which decisions can move to the buyer's team.",
        "Owner dependence influences the workload you buy and the earnings you can keep. Trace real decisions to find out what the seller handles.",
        [
            ("Map recurring and exceptional work", "Review a representative calendar alongside recent approvals, customer escalations, and hiring or purchasing decisions. Record frequency, time, account access, and whether another employee already performs part of the work."),
            ("Turn duties into a staffing plan", "A fictional owner handles two hours of escalation a week and 15 hours of estimating. Estimate those duties separately. A manager may absorb the escalations while an estimator handles proposals. Put replacement pay and ramp time into the post-close cash model."),
            ("Demonstrate the handoff", "Choose a sample quote or account issue and ask the intended successor to walk through it. Record where information, authority, or relationships still depend on the seller. Convert the gaps to dated transition tasks."),
        ],
        ["Review a real workweek", "Price replacement capacity", "Test one workflow", "Name authority at close"],
        ("Should I rely on seller transition hours alone?", "Pair time commitments with named tasks and acceptance evidence. The buyer needs to know who is responsible after those hours end."),
        ["buying-business-from-retiring-owner", "first-100-days-after-buying-a-business"],
    ),
    (
        "acquisition-revenue-reconciliation", "Reconcile Revenue in a Small Business Acquisition",
        "Tie sales reports to accounting records, investigate differences, and document the revenue evidence available to a buyer.",
        "Sales exports and bank deposits represent different stages of a transaction. Agree which report and period you are reconciling before drawing conclusions.",
        [
            ("Trace from summary to source", "Choose a month. Compare the sales summary with the general ledger, then inspect invoices, credits, and payment settlement detail. Separate timing differences from unsupported entries and ask for evidence on remaining items."),
            ("Account for settlement timing", "A fictional company has $100,000 of recorded invoices in a month, with $5,000 in credit notes. If $8,000 of net billings remain open at month-end, expected collection on that invoice cohort is $87,000 before payment processing fees. Compare to collections assigned to the same cohort."),
            ("Document what you could verify", "Build a simple bridge showing conversion from invoices to ledger revenue and collections. Attach references for adjustments. Ask your diligence accountant to review differing recognition policies or material amounts that remain unexplained."),
        ],
        ["Choose a period and cohort", "Tie credits to invoices", "Track timing differences", "Escalate unresolved items"],
        ("Can bank deposits establish the revenue figure?", "Deposits can support collection evidence. Use invoice, ledger, and settlement records together to explain timing, fees, and deposits from other sources."),
        ["quality-of-earnings-small-business-acquisition", "business-acquisition-due-diligence-checklist"],
    ),
    (
        "accounts-receivable-aging-due-diligence", "Accounts Receivable Aging in Acquisition Due Diligence",
        "Review collectible receivables, disputed balances, and post-period collections before agreeing to a purchase adjustment.",
        "An aging report is a dated list of claims. Inspect how it was generated and check what happened after the reporting date.",
        [
            ("Rebuild the aging bands", "Request invoice date, due date, outstanding amount, customer, and dispute status. Recalculate aging using the documented due date. Reconcile the open balance to the ledger and examine negative or unapplied amounts."),
            ("Sample subsequent collections", "Suppose a fictional seller reports $300,000 open. Of $70,000 more than 90 days past due, $40,000 is collected before the diligence cutoff and $20,000 is disputed. The buyer records the collections, tests the dispute evidence, and discusses treatment of the remaining amount."),
            ("Decide who owns the follow-up", "Clarify which receivables transfer, who handles old disputes, and how collections are allocated after close. Bring the sample and classifications to the deal accountant and counsel before agreeing to the balance in closing documents."),
        ],
        ["Reconcile to ledger", "Inspect old balances", "Trace payments after cutoff", "Assign dispute follow-up"],
        ("Which invoices should I sample first?", "Start with large balances, disputed invoices, recently extended terms, and old accounts that materially affect the deal model."),
        ["working-capital-business-acquisition", "acquisition-revenue-reconciliation"],
    ),
    (
        "deferred-revenue-business-acquisition", "Deferred Revenue in a Small Business Acquisition",
        "Identify prepaid obligations and estimate the post-close cost of delivering work customers have already purchased.",
        "Customer prepayments may arrive before the related work. A buyer needs a delivery schedule and a clear understanding of the obligations that transfer.",
        [
            ("Build a contract-level register", "Collect prepaid amounts, delivery milestones, remaining work, credits, and estimated fulfillment cost. Reconcile balances to the seller's ledger and ask how renewals, refunds, and partial delivery are recorded."),
            ("Model service after closing", "A fictional service company has collected $120,000 for annual support. Six months of coverage remain. At $8,000 of expected delivery cost per month, the buyer models $48,000 of post-close service cost and tests higher utilization."),
            ("Align the model and closing terms", "Review whether customer contracts and prepaid obligations transfer, how working capital is defined, and whether another deal adjustment already captures the economics. Have the accountant and counsel align definitions with the signed agreement."),
        ],
        ["List customer obligations", "Reconcile prepaid balances", "Model fulfillment cash costs", "Review the closing definition"],
        ("Is the prepaid balance the same as delivery cost?", "The balance reflects how the seller recorded the obligation. Expected delivery cost depends on staffing, usage, vendor costs, and timing."),
        ["working-capital-business-acquisition", "accounts-receivable-aging-due-diligence"],
    ),
    (
        "inventory-due-diligence-small-business", "Inventory Due Diligence When Buying a Small Business",
        "Test whether inventory exists, can be sold, and belongs in the agreed closing inventory valuation.",
        "Start with the date of the inventory export and understand how counts, adjustments, damaged goods, and items owned by someone else are recorded.",
        [
            ("Tie records to physical stock", "Sample units from the listing to the warehouse floor and from the floor back to the listing. Record condition, lot, location, quantity, and ownership. Investigate movement around the count date."),
            ("Calculate an evidence-based adjustment", "A fictional stock line shows 1,000 units at $12 cost. During the count, 120 are damaged and 80 belong to a supplier. The buyer separates those units and reviews recovery evidence before modeling which portion of the $12,000 book balance fits the deal."),
            ("Specify closing mechanics", "Agree who counts, how items in transit are handled, and which valuation rules apply. Ask the deal team to align the count process with the closing agreement and record how disputes will be handled."),
        ],
        ["Obtain stock movement records", "Sample both directions", "Check ownership and condition", "Agree cutoff and valuation"],
        ("Why count from the floor back to the list?", "The reverse check can uncover stock missing from the report or identify items that belong to a supplier or customer."),
        ["working-capital-business-acquisition", "business-acquisition-due-diligence-checklist"],
    ),
    (
        "maintenance-capex-acquisition", "Estimate Maintenance Capital Spending Before Buying a Business",
        "Use the asset register, repair history, and replacement timing to estimate the cash required to keep the business operating.",
        "A buyer needs a forward view of what it costs to preserve operating capacity. Inspect the actual assets and forecast replacement by year.",
        [
            ("Build a condition and replacement schedule", "Request asset age, service records, hours, recent downtime, and replacement quotes. Mark the assets that would interrupt customer delivery if they failed. Confirm which are owned and which are leased."),
            ("Distinguish averages from cash timing", "A fictional company expects $240,000 of fleet replacement over four years. A $60,000 annual average helps compare ongoing economics, but two vehicles due next year could require $110,000 immediately. Model both the first-year cash need and long-run reserve."),
            ("Check for deferred maintenance", "Review whether recent spending was unusually low because maintenance or replacements were deferred. Ask operations and your advisers to identify safety, reliability, or permit issues requiring additional investigation."),
        ],
        ["Inspect essential assets", "Verify quotes and dates", "Model first-year cash", "Discuss deferred work"],
        ("Where should I put maintenance capital in the model?", "Show it as a separate expected cash use alongside operating costs, working capital, and financing payments so the buyer can inspect timing."),
        ["quality-of-earnings-small-business-acquisition", "how-much-cash-to-buy-a-business"],
    ),
    (
        "day-one-acquisition-continuity-checklist", "Day-One Business Acquisition Continuity Checklist",
        "Prepare payroll, customer service, order intake, suppliers, and decision authority before the handoff date.",
        "Map the essential work that must continue through the ownership transition and identify someone who can demonstrate each function.",
        [
            ("Walk through real transactions", "Have authorized owners trace a payroll cycle, customer order, scheduled delivery, refund, supplier purchase, and urgent request. Document the systems, approvals, information, and people needed."),
            ("Rehearse the highest-risk handoff", "A fictional buyer learns that the seller's account is the only one that can approve a supplier order. The team establishes approved buyer-side access before closing, verifies it through an authorized dry run, and names a backup approver."),
            ("Check the first week", "Give employees the escalation route and customer-facing contacts relevant to their role. Check that payments, dispatch, and customer questions can be handled. Keep a log of urgent issues, named owners, and resolution times."),
        ],
        ["Identify essential operating flows", "Confirm approvals and access", "Rehearse with responsible owners", "Review the first week"],
        ("How does this relate to the first 100 days?", "Day one is about continuity of essential work. The wider plan covers stabilization, assessment, and improvements once the team can operate reliably."),
        ["first-100-days-after-buying-a-business", "owner-dependence-due-diligence"],
    ),
    (
        "supplier-concentration-acquisition", "Supplier Concentration Risk When Buying a Business",
        "Identify single-source dependencies and test alternate supply, qualification time, and continuity before closing.",
        "Spending concentration is a starting point. A small vendor can still control a critical part, certification, or proprietary process.",
        [
            ("Map critical dependencies", "List essential inputs, approved suppliers, contractual restrictions, inventory coverage, actual lead times, and any required customer approval for a substitute. Identify the person who can verify each dependency."),
            ("Run a shortage scenario", "A fictional manufacturer holds three weeks of a critical part. Its only alternate supplier needs five weeks after qualification and two weeks for qualification. Even if the alternate works, normal inventory would leave a four-week gap without other action."),
            ("Verify the transition plan", "Check whether terms and credit limits transfer and confirm who manages supplier communication. Price a reasonable buffer or second-source trial and record how it changes the buyer's cash needs."),
        ],
        ["Map low-spend critical inputs", "Confirm qualification timing", "Calculate uncovered time", "Assign buyer-side ownership"],
        ("Should I focus on the top suppliers by spend?", "Review major spend, then inspect whether any low-spend input can stop delivery before an alternative becomes available."),
        ["business-acquisition-due-diligence-checklist", "inventory-due-diligence-small-business"],
    ),
    (
        "seasonal-cash-flow-acquisition", "Model Seasonal Cash Flow Before Buying a Business",
        "Translate annual earnings into monthly cash needs using collections, inventory, payroll, and expected financing payments.",
        "Businesses can report attractive annual earnings while needing a substantial reserve in their slowest month. Build a monthly cash model before deciding what you can afford.",
        [
            ("Use collections and payments by month", "Start with prior monthly collections, payroll, inventory purchases, vendor bills, and taxes. Adjust for deal changes you can support and model debt payments and one-time closing costs separately."),
            ("Stress-test the cash low point", "A fictional buyer starts a slow month with $130,000. Collections of $60,000 and cash uses of $155,000 leave $35,000. If another $25,000 of receipts slips into next month, cash falls to $10,000. Test whether that is enough to meet scheduled obligations."),
            ("Tie the result to timing", "Compare different closing months and inventory build dates. Document what cash the buyer supplies, what arrangements are confirmed, and what corrective action can trigger before the reserve is used."),
        ],
        ["Collect monthly history", "Model closing and debt separately", "Delay receipts in a downside case", "Choose a reserve trigger"],
        ("Why use monthly balances instead of annual profit?", "Monthly balances reveal whether cash arrives in time to cover obligations even when the full year appears profitable."),
        ["how-much-cash-to-buy-a-business", "accounts-receivable-aging-due-diligence"],
    ),
]


def field_guides():
    for slug, title, description, lead, sections, checklist, faq, related in TOPICS:
        yield {
            "slug": slug,
            "title": title,
            "description": description,
            "lead": lead,
            "eyebrow": "Acquisition Due Diligence",
            "published": PUBLISHED,
            "sections": [(heading, [paragraph]) for heading, paragraph in sections],
            "checklist": checklist,
            "faqs": [faq],
            "related": related,
        }
