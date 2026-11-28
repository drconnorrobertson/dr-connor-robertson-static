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
TOPICS.extend([
    (
        "acquisition-backlog-due-diligence", "How to Verify Order Backlog When Buying a Business",
        "Reconcile the order backlog and distinguish customer commitments, expected work, and cash needed to fulfill it.",
        "An order backlog becomes useful evidence when a buyer can identify the underlying commitment and the work still required.",
        [
            ("Rebuild the backlog from orders", "Export signed orders and active change orders. Track promised dates, completion, remaining invoicing and cancellation rights. Reconcile backlog movement from opening balance to closing balance."),
            ("Test fulfillment before counting revenue", "A fictional backlog totals $600,000, including $100,000 of orders awaiting customer approval. Separate the uncertain amount. For a $150,000 signed job, estimate direct and mobilization cash requirements and when progress invoices can be collected."),
            ("Validate capacity and customer timing", "Sample overdue, large, and newly signed jobs. Ask operations whether crew, equipment, and materials can meet the promised dates. Have deal counsel review change and cancellation rights where material."),
        ],
        ["Tie backlog to commitments", "Separate expected orders", "Forecast cash and capacity", "Inspect late jobs"],
        ("Should backlog equal next year's revenue?", "Convert confirmed orders to a dated delivery schedule and adjust for cancellations, incomplete inputs, capacity, and revenue already recognized."),
        ["customer-concentration-risk", "deferred-revenue-business-acquisition"],
    ),
    (
        "employee-accruals-acquisition-diligence", "Employee Accruals in Acquisition Due Diligence",
        "Gather evidence on earned bonuses, commissions, paid leave, and payroll cutoffs before agreeing to closing balances.",
        "Employee-related balances can affect cash needs and closing mechanics. Begin with policy documents and anonymized reports.",
        [
            ("Create an accrual register", "Record each category, earning period, eligibility terms, payout timing, accounting balance, and policy reference. Use aggregate data or appropriately authorized records."),
            ("Reconcile one cutoff", "A fictional company has a $40,000 commission ledger balance. A sample shows $9,000 was paid in the following payroll and $6,000 depends on unresolved returns. Document the evidence and ask which cutoff and definitions the financial team uses."),
            ("Identify who bears the obligation", "Have deal counsel and the accountant review applicable obligations and deal definitions. Assign the owner of post-close payment or dispute handling and reconcile against the purchase agreement."),
        ],
        ["Obtain policies and reports", "Trace one payout cycle", "Flag unresolved eligibility", "Confirm responsibility"],
        ("Should I use payroll cash paid for the cutoff?", "Use the earning period and documented eligibility to identify the amount under review, then reconcile subsequent cash payments to it."),
        ["working-capital-business-acquisition", "day-one-acquisition-continuity-checklist"],
    ),
    (
        "acquisition-real-estate-lease-review", "Commercial Lease Review When Buying a Business",
        "Trace occupancy costs, renewal dates, assignment conditions, and site dependencies before a business acquisition.",
        "The site a business relies on can affect whether it can operate after closing. Collect signed leases, amendments, notices, and the most recent occupancy invoices.",
        [
            ("Reconcile occupancy expense", "Separate base rent, pass-through charges, utilities, scheduled increases, and one-time items. Ask who maintains essential equipment and estimate cash required when payments change."),
            ("Map deadlines against closing", "A fictional retailer pays $8,000 monthly rent and $1,200 in recurring pass-throughs. In three months base rent increases by $800. The buyer models the higher run rate and has counsel confirm the required consent and feasible timing."),
            ("Check location continuity", "Assess site-specific needs such as access, capacity, or permits with relevant advisers. Document the alternatives and decision deadline if the preferred location cannot transfer on time."),
        ],
        ["Collect signed amendments", "Build cash schedule", "Confirm consent path", "Document continuity options"],
        ("What if the seller owns the property?", "Model future occupancy under the proposed lease or property deal and verify responsibilities, renewal terms, and affordability with the deal team."),
        ["maintenance-capex-acquisition", "day-one-acquisition-continuity-checklist"],
    ),
    (
        "acquisition-software-license-transfer", "Software License Transfer Checklist for Acquisitions",
        "Map business-critical systems, data exports, license ownership, and approved access before a company handoff.",
        "Identify systems needed to place orders, collect cash, support customers, and run payroll. Confirm who can approve access and who holds the agreement for each system.",
        [
            ("Inventory access and contract owners", "Record provider, business owner, admin role, renewal date, legal entity, license count, integrations, and data export coverage. Confirm the permitted transfer process with the provider and deal team."),
            ("Rehearse continuity without live changes", "A fictional company uses a scheduling platform tied to a seller-owned workspace. The team uses sample data to test an authorized export and import, checks whether time zones and job notes survive, and confirms the intended production handoff with the provider."),
            ("Verify responsibilities at close", "Identify who authorizes the transfer, who checks service after close, and which approved fallback can keep essential work available. Record the evidence of a successful handoff without copying credentials into the checklist."),
        ],
        ["List essential systems", "Confirm provider transfer process", "Test an approved sample export", "Assign handoff owners"],
        ("Does admin access prove the license transferred?", "Admin access demonstrates one operational capability. Confirm the contract, billing owner, data responsibility, and ongoing support separately."),
        ["day-one-acquisition-continuity-checklist", "owner-dependence-due-diligence"],
    ),
    (
        "employee-transition-listening-plan", "Employee Listening Plan After a Business Acquisition",
        "Set up post-close employee listening sessions, follow-up commitments, and a practical issue log.",
        "Employee feedback is most useful when leaders can act on it and explain what happens next. Schedule predictable opportunities to raise operating concerns.",
        [
            ("Build a listening schedule", "Choose who attends, how separate shifts can participate, what information is recorded, and who follows up. Use a consistent set of operational questions and avoid collecting unnecessary personal information."),
            ("Turn feedback into an owned action", "In a fictional company, multiple shifts report that a new scheduling tool leaves no clear contact for absences. The operator confirms the issue, picks one contact and backup, and tests the revised instruction with a supervisor from each shift."),
            ("Close the loop", "Tell employees what changed, what is still under review, and when they should expect follow-up. Use aggregate themes for wider reporting and route individual concerns through the appropriate internal process."),
        ],
        ["Include each shift", "Record repeated operating issues", "Assign action owners", "Confirm changes with staff"],
        ("How often should the buyer meet employees?", "Match cadence to transition risk and existing communications. Establish a follow-up routine employees can count on before increasing meeting volume."),
        ["first-100-days-after-buying-a-business", "day-one-acquisition-continuity-checklist"],
    ),
    (
        "acquisition-customer-renewal-calendar", "Customer Renewal Calendar for Acquisition Diligence",
        "Map renewal and notice dates so a buyer can test revenue timing and plan account handoffs under the actual agreements.",
        "Build a contract-level calendar for material accounts. Key dates matter most when connected to revenue risk and the person who manages the relationship.",
        [
            ("Structure the renewal evidence", "Record account group, agreement version, renewal month, notice rules, recurring value, responsible employee, and recent customer signals. Keep renewal assumptions apart from signed commitments."),
            ("Prioritize accounts near closing", "A fictional buyer expects to close in October and finds three January renewals worth $240,000 combined. Two require notice in November. The buyer reviews who owns communications and models a downside case with one delayed renewal."),
            ("Use the calendar after close", "Work with counsel and the account lead to confirm permissible outreach and any consent needed. Give each priority account a dated action and capture the evidence of renewal when it arrives."),
        ],
        ["Validate agreement versions", "Map near-term renewals", "Stress-test delays", "Assign an account owner"],
        ("How is this different from customer concentration?", "Concentration measures dependence on a relationship. A renewal calendar adds deadlines and identifies when that risk needs an operating decision."),
        ["customer-concentration-risk", "seasonal-cash-flow-acquisition"],
    ),
])


TOPICS.extend([('acquisition-warranty-claims-review',
  'Warranty Claims Review Before Buying a Business',
  'Estimate the work and cash tied to open and expected warranty claims.',
  'Review the commitment the customer received, the claim history, and cash required after close.',
  [('Collect warranty terms and active claims',
    'Match open claims to the originating sale, coverage period, status, and resolution owner. Review prior '
    'claims by product cohort and document unusual failure rates.'),
   ('Model an expected cost',
    'A fictional buyer finds 40 open claims. The initial planning model uses $180 average handling and '
    'repair cost, or $7,200, before unusual claims. Inspect the high-cost cases separately.'),
   ('Resolve responsibility',
    'Ask deal advisers to confirm who handles existing claims and future claims tied to prior sales. Assign '
    'an operating owner and a cash contingency.')],
  ['Map warranty terms',
   'Review active claims',
   'Model high-cost cases',
   'Confirm post-close responsibility'],
  ('What if claim rates changed recently?',
   'Review the affected cohorts separately and test the cost under the newer rate.'),
  ['maintenance-capex-acquisition', 'day-one-acquisition-continuity-checklist']),
 ('acquisition-customer-credit-memos',
  'Review Customer Credit Memos in Acquisition Diligence',
  'Trace customer credits to sales and distinguish routine discounts from disputes or recurring fulfillment '
  'problems.',
  'Credit memo history shows where billed revenue changed after invoicing.',
  [('Build a bridge from gross to net',
    'Group credits by origin and reason. Tie the original invoice and approval to each sampled credit and '
    'inspect unmatched credits around reporting cutoffs.'),
   ('Test recurring causes',
    'A fictional seller has $45,000 of credits in one quarter, including $25,000 from late delivery on one '
    'service line. The buyer checks subsequent jobs and distinguishes the recoverable operating issue from a '
    'persistent pricing assumption.'),
   ('Reflect the evidence in the deal model',
    'Update the projected net sales for persistent causes and document the estimate. Review unsettled '
    'disputes and upcoming service obligations with the transaction team.')],
  ['Reconcile adjustments', 'Inspect high-value credits', 'Classify repeat causes', 'Update net sales'],
  ('Why review credits rather than only net revenue?',
   'Credits can reveal recurring delivery problems or disputed terms hidden inside a stable aggregate '
   'amount.'),
  ['acquisition-revenue-reconciliation', 'accounts-receivable-aging-due-diligence']),
 ('acquisition-cash-conversion-cycle',
  'Cash Conversion Cycle When Buying a Business',
  'Translate inventory, billing and collection timing into a concrete funding requirement.',
  'A funding model needs the time between cash paid to suppliers and cash collected from customers.',
  [('Trace real trade cycles',
    'Collect time stamps from purchase orders, receipts, inventory issues, invoices and payments. Use '
    'representative orders by product line or season.'),
   ('Walk through a cash gap',
    'A fictional distributor pays on day 15, sells the inventory on day 35, and collects 35 days after sale. '
    'Cash is tied up for about 55 days. Apply that timing to planned purchases and test delays.'),
   ('Build the first-quarter funding schedule',
    'Map purchases, collections and debt payments week by week when cash is tight. Ask finance to reconcile '
    'the forecast with actual balances and update it at close.')],
  ['Collect source dates',
   'Measure time by cohort',
   'Model collection delays',
   'Monitor first-quarter balances'],
  ('How is this different from a working capital target?',
   'Cash timing helps estimate what must be funded during operations. The negotiated working capital target '
   'defines the purchase agreement mechanics.'),
  ['working-capital-business-acquisition', 'seasonal-cash-flow-acquisition']),
 ('key-manager-transition-plan',
  'Key Manager Transition Plan for Business Buyers',
  'Plan the transfer of decisions, relationships and operating responsibilities to key managers after an '
  'acquisition.',
  'A named manager needs clear authority, usable records and time to assume important duties.',
  [('Map the responsibilities',
    'List recurring decisions, unusual exceptions, internal and external relationships, approval limits and '
    'system access. Confirm which duties the manager already performs.'),
   ('Rehearse a high-impact decision',
    'A fictional manager can schedule staff but has never approved an expedited supplier order. The buyer '
    'runs an authorized exercise and records the budget limit, escalation path and systems needed for the '
    'change.'),
   ('Review workload after transfer',
    "Check which duties can move off the manager's plate. Schedule feedback and a backup owner for critical "
    'decisions. Use observable milestones to confirm the handoff.')],
  ['Map current duties', 'Set authority', 'Rehearse one exception', 'Review capacity'],
  ('What if the manager lacks capacity?',
   'Reassign work, add support or stage the transfer with an interim owner and explicit dates.'),
  ['owner-dependence-due-diligence', 'employee-transition-listening-plan']),
 ('acquisition-customer-deposit-register',
  'Customer Deposit Register for Business Buyers',
  'Build a register tying individual deposits to open orders, refund rules and delivery obligations.',
  'A deposit register helps prevent prepaid jobs from falling out of the closing handoff.',
  [('Connect every amount to a job',
    'Record deposit date, amount, remaining invoice, order status, expected completion, refund terms and '
    'account owner. Reconcile the register to accounting records.'),
   ('Quantify unresolved jobs',
    'A fictional company has 18 deposits totaling $90,000. Three pending jobs account for $15,000 and lack '
    'confirmed delivery dates. The buyer checks whether the orders can be filled or funds may need to be '
    'returned.'),
   ('Confirm handoff and reconciliation',
    'Have the deal team confirm treatment and appoint one owner for post-close customer communications. '
    'Sample the first week of completed jobs against the register.')],
  ['Build the job-level register', 'Reconcile to ledger', 'Review uncertain jobs', 'Assign follow-up'],
  ('How does this relate to deferred revenue?',
   'The register provides practical job-level evidence. The accountant determines how amounts belong in the '
   'financial statements and deal calculations.'),
  ['deferred-revenue-business-acquisition', 'acquisition-backlog-due-diligence']),
 ('acquisition-service-level-commitments',
  'Review Service-Level Commitments Before an Acquisition',
  'Map delivery, uptime, response and reporting commitments before deciding how the business will serve '
  'accounts after close.',
  'The buyer needs to understand which commitments create recurring staffing costs and which gaps already '
  'affect customer trust.',
  [('Read obligations with operations',
    'List commitments and measurement rules from signed contracts. Compare actual performance, recurring '
    'reports, credits and incident logs.'),
   ('Test the operating implications',
    'A fictional support contract requires a response within two hours during defined coverage hours. The '
    'buyer finds repeated late responses on one shift and tests the staffing and backup coverage required to '
    'support the promise.'),
   ('Assign ongoing ownership',
    'Give each commitment an operating owner and escalation route. Ask the deal team to review material '
    'obligations and open claims, then carry the most critical measures into the transition dashboard.')],
  ['Collect signed terms', 'Reconcile performance reports', 'Forecast staffing or capacity', 'Assign owners'],
  ('What if the seller reports performance differently from the contract?',
   'Recalculate a sample using the contractual definition and document the difference before relying on the '
   'reported figure.'),
  ['customer-concentration-risk', 'acquisition-customer-renewal-calendar'])])

TOPICS.extend([('acquisition-gross-margin-bridge',
  'Gross Margin Bridge for Acquisition Due Diligence',
  'Separate price, mix, volume, and direct cost changes before relying on a seller’s margin trend.',
  'A gross margin bridge explains what changed between two periods and which changes the buyer can '
  'reasonably expect to persist.',
  [('Align the cost and product definitions',
    'Use comparable periods and document where freight, subcontractors, returns and discounts are booked. '
    'Map changed product codes and identify missing direct costs.'),
   ('Reconcile gross profit in dollars',
    'A seller reports the same $200,000 gross profit on revenue rising from $500,000 to $625,000. Margin '
    'declined from 40% to 32%. Break the change out by product or contract before deciding whether higher '
    'sales improved economic output.'),
   ('Test the assumptions that matter',
    'Carry forward recurring changes in price or cost only when there is documented support. If mix shifts '
    'materially, model a separate downside mix and ask the diligence accountant to review the bridge.')],
  ['Align periods', 'Reconcile gross profit', 'Review changes by product', 'Stress-test mix'],
  ('Should a buyer compare only margin percentages?',
   'Show gross profit dollars alongside percentages so growth and margin dilution stay visible.'),
  ['quality-of-earnings-small-business-acquisition', 'acquisition-customer-credit-memos']),
 ('debt-like-items-acquisition-review',
  'Debt-Like Items Review in a Small Business Acquisition',
  'Build a review list of possible debt-like obligations and avoid double counting them across deal '
  'adjustments.',
  'Begin with the definition being negotiated for the deal and a list of obligations requiring adviser '
  'review.',
  [('Collect potential obligations',
    'Ask for obligations with amounts, cutoff dates, due dates, responsible parties, and signed evidence. '
    'Mark items already included in working capital or another adjustment.'),
   ('Walk a duplicate through the model',
    'A fictional obligation of $35,000 for overdue equipment rent appears both in payable aging and in a '
    'draft debt-like schedule. The team reconciles the references and asks counsel and the deal accountant '
    'which negotiated calculation should capture it.'),
   ('Document closing treatment',
    'Update the schedule as balances change and ask the deal team to confirm classification. Record the '
    'reason for any exclusion and make the treatment visible in the bridge to closing proceeds.')],
  ['Get the deal definitions',
   'Collect supporting records',
   'Check for duplicates',
   'Confirm closing treatment'],
  ('Is every unpaid bill debt-like?',
   'Classification depends on the negotiated terms and the nature of the obligation. Review each materially '
   'disputed category with the deal team.'),
  ['working-capital-business-acquisition', 'employee-accruals-acquisition-diligence']),
 ('acquisition-contingent-liability-register',
  'Contingent Liability Register for Acquisition Diligence',
  'Document uncertain obligations, missing evidence, response deadlines, and operating owners before '
  'acquisition closing.',
  'A contingent liability register keeps uncertain potential obligations visible even when no reliable '
  'amount is available.',
  [('Record what is known',
    'Log the event, basis, possible counterparties, notice deadlines, supporting documents, and who has '
    'authority to investigate. Separate stated claims from estimates and confirmed costs.'),
   ('Model a range with clear boundaries',
    'A fictional business receives a $60,000 disputed customer claim. The buyer records the requested amount '
    'and separately has advisers evaluate possible outcomes, handling cost, and whether any insurance or '
    'contract provision applies.'),
   ('Follow the decisions through closing',
    'Set checkpoints for reviewing evidence and update the model when material facts change. Confirm who '
    'handles notices or records after close with qualified advisers.')],
  ['Log the event and dates',
   'Separate claims from estimates',
   'Name an investigation owner',
   'Review handover duties'],
  ('What if there is too little evidence to estimate an amount?',
   'State what is unknown, who can obtain evidence, and the deadline for deciding whether to proceed with '
   'the uncertainty.'),
  ['business-acquisition-due-diligence-checklist', 'acquisition-warranty-claims-review']),
 ('handover-readiness-evidence',
  'Acquisition Handover Readiness Evidence Checklist',
  'Turn acquisition handover tasks into observable proof of who can run essential workflows after close.',
  'Use a readiness checklist to demonstrate that the intended owners can execute the work and recognize '
  'exceptions.',
  [('Choose critical walkthroughs',
    'List a representative payment, order, employee schedule, customer issue, and supplier request. Identify '
    'required approvals and how the intended owner demonstrates work in an approved test.'),
   ('Record partial readiness',
    'A buyer-side operator can export a dispatch schedule but cannot see last-minute callouts in the new '
    'system. Record the gap, name the workaround owner, and schedule a second test before the first live '
    'shift.'),
   ('Keep a decision record',
    'Use accepted, conditional, and unresolved states with a dated reason. Escalate any issue that stops '
    'essential operations and agree an owner for first-week follow-through.')],
  ['Select critical workflows', 'Define observable proof', 'Record unresolved steps', 'Review on day one'],
  ('How is this different from a task checklist?',
   'A task checklist records activity. Readiness evidence shows that the intended person can run the work '
   'under expected operating conditions.'),
  ['day-one-acquisition-continuity-checklist', 'key-manager-transition-plan'])])

TOPICS.extend([('acquisition-business-insurance-coverage',
  'Business Insurance Coverage Review Before an Acquisition',
  'Map operating coverage, policy periods, exclusions and transition questions before closing.',
  'Review the coverage evidence with an insurance professional and identify operations that need continuity '
  'from the closing date.',
  [('Assemble the coverage file',
    'Collect declarations, endorsements, claim histories where available, policy dates, deductibles and named '
    'insureds. Compare insured operations, vehicles and locations with what the buyer expects to receive.'),
   ('Walk a timing question through the file',
    'A fictional buyer inherits a service operation with an unresolved incident reported under the seller’s '
    'policy. Record incident and reporting dates and ask the broker and counsel to explain who reports new '
    'developments and which documents should be retained.'),
   ('Confirm the agreed plan',
    'Assign someone to verify that the intended coverage documentation is available by closing and that '
    'managers know how to report an incident afterward. Keep unresolved coverage and responsibility questions '
    'in the deal log.')],
  ['Collect endorsements',
   'Compare entities and operations',
   'Review open incidents',
   'Confirm reporting ownership'],
  ('Does an insurance certificate settle coverage?',
   'Use the certificate as a pointer to the policy. Ask qualified professionals to review terms, exclusions, '
   'and transition questions.'),
  ['acquisition-contingent-liability-register', 'day-one-acquisition-continuity-checklist']),
 ('acquisition-customer-cohort-retention',
  'Customer Cohort Retention in Acquisition Diligence',
  'Test repeat purchase patterns from dated customer cohorts rather than a blended revenue figure.',
  'Use matching customer identities and enough follow-up time to compare similar cohorts.',
  [('Define a meaningful repeat purchase',
    'Identify the first purchase date, customer grouping, repeat order rule, lookback and follow-up window. '
    'Document whether refunds, free replacements, or related entities qualify.'),
   ('Compare cohorts on the same clock',
    'A fictional January cohort includes 50 new accounts and 30 order again within 90 days. A February cohort '
    'has 40 accounts and 20 repeats within the same window. Compare 60% with 50%, then inspect differences in '
    'product mix and acquisition channel.'),
   ('Turn retention into a buyer assumption',
    'Flag cohorts that have not completed the measurement window. Reconcile customer totals to sales records '
    'and explain which assumptions support the downside cash forecast.')],
  ['Define a qualifying repeat',
   'Align follow-up windows',
   'Reconcile customer identities',
   'Model a weaker cohort'],
  ('How is cohort retention different from concentration?',
   'Retention measures repeat activity across comparable groups. Concentration measures reliance on specific '
   'relationships.'),
  ['customer-concentration-risk', 'acquisition-customer-renewal-calendar']),
 ('acquisition-third-party-permissions',
  'Third-Party Permissions Checklist for Business Acquisitions',
  'Identify contracts and dependencies that require third-party action before ownership can change.',
  'Create a contract-level list of the permissions, notices and approvals the deal team needs to evaluate.',
  [('Connect permission to an operating dependency',
    'Collect signed agreements and amendments. For each material relationship identify the counterparty, '
    'document reference, reason it matters, decision date and person who can verify the next step.'),
   ('Plan backward from the decision',
    'A fictional distribution business needs access to a customer portal for recurring orders. The buyer '
    'learns onboarding takes three weeks. The account owner confirms permissible contact with the deal team '
    'and creates a dated readiness check ahead of closing.'),
   ('Record evidence and fallback',
    'Document written responses and distinguish submitted requests from approvals. Have advisers confirm '
    'requirements for the particular deal and give each unresolved dependency an operating fallback with an '
    'owner.')],
  ['Gather agreement versions', 'Name the owner', 'Record the evidence', 'Test a fallback'],
  ('When should the buyer contact counterparties?',
   'Coordinate contact through the agreed deal process, with counsel and authorized deal team members '
   'reviewing timing and confidentiality.'),
  ['acquisition-real-estate-lease-review', 'acquisition-software-license-transfer']),
 ('acquisition-supplier-payment-terms',
  'Supplier Payment Terms in Acquisition Cash Flow',
  'Test whether supplier credit, deposits and settlement timing can change after closing.',
  'The same inventory and sales forecast can require more cash if supplier terms change.',
  [('Reconcile actual payment behavior',
    'Compare contract terms with invoice and payment history. Capture deposits, early-payment discounts, '
    'credit limits and exceptions by supplier. Verify whether terms depend on the selling entity or a separate '
    'guarantee.'),
   ('Model a shorter term',
    'A fictional buyer expects $80,000 a month of evenly spaced purchases under 30-day terms. If the supplier '
    'requires payment at order, the initial transition could accelerate roughly one month of outflows. Model '
    'actual dated orders and avoid counting the permanent run rate increase twice.'),
   ('Verify the post-close arrangement',
    'Assign someone to confirm terms with authorized contacts and identify any onboarding or deposits. Pair '
    'the base case with a cash forecast using the more restrictive terms until documented evidence supports '
    'the change.')],
  ['Collect invoices and payment dates',
   'Check credit conditions',
   'Model earlier cash outflows',
   'Confirm terms before close'],
  ('Do historical payment patterns establish future terms?',
   'Use historical timing for context and confirm the arrangement available to the buyer before relying on '
   'it.'),
  ['acquisition-cash-conversion-cycle', 'supplier-concentration-acquisition'])])

TOPICS.extend([('acquisition-fixed-asset-ownership',
  'Verify Fixed Asset Ownership Before Buying a Business',
  'Reconcile the seller’s fixed asset list to physical equipment, ownership evidence, and obligations.',
  'An asset register identifies recorded equipment. Build transaction evidence for the items the buyer '
  'expects to use from day one.',
  [('Match physical assets to records',
    'Sample serial numbers, locations and operating condition. Request ownership or lease evidence and '
    'compare the intended asset list with the transfer schedule.'),
   ('Walk a discrepancy through diligence',
    'A fictional shop records three forklifts. Two serial numbers match purchase records and the third '
    'matches a rental agreement. Separate the rental from the owned list and model the ongoing cost or '
    'replacement requirement.'),
   ('Resolve material gaps',
    'Ask the transaction team to review financing, restrictions and transfer documents. Assign an operating '
    'owner to confirm equipment access and availability at handover.')],
  ['Match serial numbers',
   'Confirm ownership evidence',
   'Record unresolved items',
   'Check availability at close'],
  ('Does a depreciation schedule establish ownership?',
   'Use it to locate recorded assets and confirm ownership or permitted use against supporting documents.'),
  ['maintenance-capex-acquisition', 'acquisition-third-party-permissions']),
 ('acquisition-sales-pipeline-quality',
  'Sales Pipeline Quality Review for Business Acquisitions',
  'Test whether the seller’s reported sales pipeline has identifiable buyers, evidence of progression, and '
  'realistic timing.',
  'Pipeline figures can help forecast future orders when each material opportunity has evidence and a '
  'specific next milestone.',
  [('Reconstruct the stage criteria',
    'Record when opportunities entered their stage and the evidence required to advance. Inspect approved '
    'budgets, outreach history, proposals and known decision dates using authorized records.'),
   ('Test stale opportunities',
    'A fictional seller reports $900,000 in late-stage opportunities. Three deals totaling $300,000 have no '
    'buyer activity for 120 days. Forecast the remaining deals separately and require fresh evidence before '
    'relying on the stale group.'),
   ('Validate timing after close',
    'Compare stage-to-order outcomes from past cohorts and ask who owns the relationship after handover. Run '
    'a delay scenario for large deals where decisions fall near closing.')],
  ['Document stage rules', 'Sample past conversion', 'Flag stale opportunities', 'Assign account ownership'],
  ('How is pipeline different from backlog?',
   'Pipeline tracks potential orders. Backlog should trace to customer commitments and remaining fulfillment '
   'work.'),
  ['acquisition-backlog-due-diligence', 'customer-concentration-risk']),
 ('acquisition-data-room-request-tracker',
  'Data Room Request Tracker for Small Business Acquisitions',
  'Track diligence requests so owners can verify the evidence provided, identify gaps and follow material '
  'issues to a decision.',
  'A request tracker should tell the deal team which question a document answers and what remains to be '
  'verified.',
  [('Make requests specific',
    'Give requests a subject, relevant entity, dates, requested format, responsible person and reason. Use '
    'authorized access to records and avoid copying sensitive data into the tracker.'),
   ('Check completeness before accepting',
    'A fictional buyer receives 11 months of customer sales when requesting a full year. The reviewer '
    'records the missing month, checks the date range and leaves the request partially fulfilled until the '
    'seller supplies the remaining extract.'),
   ('Connect requests to findings',
    'Assign a reviewer to record which issue the evidence resolves. Flag unresolved items approaching a '
    'decision date and document how they affect models or closing conditions.')],
  ['Name the reviewer', 'Check dates and entities', 'Record partial delivery', 'Tie evidence to decisions'],
  ('When can a request be closed?',
   'Close it after the reviewer confirms the evidence addresses the original question or records an agreed '
   'disposition for what remains unresolved.'),
  ['business-acquisition-due-diligence-checklist', 'acquisition-decision-log'])])

TOPICS.extend([('acquisition-customer-contract-rate-review',
  'Customer Contract Rate Review Before an Acquisition',
  'Check actual billing against signed rate schedules and model upcoming price changes.',
  'Start with the contract versions and invoices that support the largest or most complex customer '
  'relationships.',
  [('Build a rate schedule',
    'Record service codes, agreed prices, effective dates, permitted surcharges, discounts, approvals and '
    'billing frequency.'),
   ('Test a real invoice pattern',
    'A fictional contract lists $120 per service call, but invoices have billed $105 for six months. Inspect '
    'amendments and account correspondence to determine whether the lower amount was approved or a '
    'configuration error.'),
   ('Reconcile the forecast',
    'Use actual collected pricing for the starting model, investigate future changes, and have the advisers '
    'assess material unresolved differences.')],
  ['Collect amendments', 'Tie invoices to rates', 'Flag recurring concessions', 'Update the forecast'],
  ('Which accounts should I review first?',
   'Start with accounts whose approved rates differ materially from the forecast or whose next price change '
   'falls near closing.'),
  ['acquisition-customer-renewal-calendar', 'acquisition-gross-margin-bridge']),
 ('acquisition-open-purchase-orders',
  'Open Purchase Order Review for Business Buyers',
  'Identify procurement commitments, cancellation terms and expected cash outflows before closing.',
  'An open purchase order can represent a required input, an avoidable duplicate, or a payment the buyer '
  'needs to fund.',
  [('Reconcile order status',
    'Compare orders against partial receipts, supplier acknowledgements and deposits. Identify open work by '
    'delivery date, responsible team, and related customer order.'),
   ('Model remaining commitments',
    'A fictional seller shows $200,000 of open orders. The review finds $35,000 already received but '
    'unclosed and $20,000 of orders awaiting supplier confirmation. Treat confirmed remaining commitments '
    'and unresolved orders as distinct cash scenarios.'),
   ('Assign follow-up',
    'Have the deal team review which commitments transfer. Give purchasing responsibility for confirming '
    'important deliveries and update the cash schedule as evidence changes.')],
  ['Reconcile receipts', 'Identify deposits', 'Record expected cash dates', 'Confirm post-close ownership'],
  ('Should every open order go into the baseline forecast?',
   'Include evidence-supported commitments in the baseline and describe how uncertain orders affect a '
   'separate scenario.'),
  ['acquisition-supplier-payment-terms', 'inventory-due-diligence-small-business']),
 ('acquisition-equipment-downtime-review',
  'Equipment Downtime Review for Business Acquisitions',
  'Use downtime records to test throughput assumptions, repair exposure and backup capacity.',
  'Identify the equipment failures that interrupt customer delivery and compare recorded downtime with the '
  'forecast.',
  [('Trace downtime events',
    'Collect maintenance tickets, shift notes, throughput history, duration and repair costs. Separate '
    'planned maintenance from failures and record when another line absorbed the work.'),
   ('Test a capacity assumption',
    'A fictional packaging line loses six hours per month unexpectedly. At 140 units per hour, that exposes '
    'up to 840 units of nominal production. Check whether overtime or spare capacity actually recovers those '
    'units.'),
   ('Model operating response',
    'Price backup capacity and upcoming repair work, then test how a longer outage would change delivery and '
    'cash. Assign post-close monitoring to an operating owner.')],
  ['Identify the constrained asset',
   'Reconcile event records',
   'Check recoverable volume',
   'Estimate backup capacity'],
  ('Is lost production the same as lost sales?',
   'Check how much demand was deferred, recovered, or canceled before valuing the financial effect.'),
  ['maintenance-capex-acquisition', 'acquisition-fixed-asset-ownership']),
 ('acquisition-inventory-shrink-review',
  'Inventory Shrink Review in Acquisition Diligence',
  'Measure recurring inventory loss and separate counting errors from supported shrink.',
  'Compare inventory movements and physical counts over matching periods before carrying the seller’s loss '
  'assumption into the deal model.',
  [('Build a movement bridge',
    'Reconcile opening quantity, receipts, issues, transfers and adjustments to closing quantity. Check '
    'consistent units and verify the count cutoff.'),
   ('Evaluate the adjustment pattern',
    'A fictional warehouse expects 2,000 units and counts 1,960. Ten were transferred before cutoff and '
    'recorded afterward. Investigate the remaining 30 using prior reconciliations and related transaction '
    'evidence.'),
   ('Carry findings into diligence',
    'Separate errors corrected once from unexplained recurring differences. Document any estimated ongoing '
    'cost and have the financial team review how it affects inventory and projected margins.')],
  ['Align the cutoff', 'Reconcile movement', 'Inspect recurring differences', 'Review deal effects'],
  ('Can a single count establish a shrink rate?',
   'A count can verify one date. Compare multiple reconciled periods before estimating a recurring rate.'),
  ['inventory-due-diligence-small-business', 'acquisition-gross-margin-bridge'])])

TOPICS.extend([('acquisition-channel-revenue-dependence',
  'Revenue Channel Dependence in Acquisition Diligence',
  'Review dependence on marketplaces, referral sources or resellers before forecasting customer acquisition.',
  'Identify which channels produce collected sales and which relationships the buyer can reasonably expect '
  'to continue.',
  [('Reconcile channel attribution',
    'Compare channel exports, customer records and payment settlements. Separate direct invoices, '
    'billed-through partners, referral charges and refunds.'),
   ('Test a concentrated channel',
    'A fictional business receives $600,000 of net sales through a single reseller and $900,000 directly. '
    'The reseller accounts for 40% of net sales. Model a six-month decline using contribution after reseller '
    'fees and the time to replace demand.'),
   ('Verify continuity',
    'Review contracts and operational dependencies with deal advisers. Assign a buyer-side owner and update '
    'the model if portal access, pricing or referral terms change.')],
  ['Reconcile channel sales',
   'Calculate channel share',
   'Model lost contribution',
   'Verify continued access'],
  ('How does this differ from customer concentration?',
   'Channel risk can affect many customers at once even when individual accounts are small.'),
  ['customer-concentration-risk', 'acquisition-customer-cohort-retention']),
 ('acquisition-work-in-progress-review',
  'Work in Progress Review When Buying a Business',
  'Reconcile project progress, unbilled amounts and cost to complete for open work.',
  'Begin with open projects and the estimates and customer approvals that support remaining work.',
  [('Build a project-level view',
    'Capture contract amount, approved changes, billed and collected amounts, actual cost and estimated cost '
    'to finish. Note disputed scope and missing acceptance evidence.'),
   ('Test the remaining margin',
    'A fictional job has a $200,000 contract and $150,000 billed. A review identifies $65,000 in remaining '
    'cost and $45,000 previously spent. The job may have positive overall margin, while its remaining '
    '$50,000 billable amount trails the $65,000 future cost.'),
   ('Align financial and operating views',
    'Have the diligence accountant review reporting treatment. Ask the project owner to verify staffing, '
    'materials and remaining approval dates before relying on the cash forecast.')],
  ['Collect approved scope',
   'Reconcile billings and costs',
   'Test cost to complete',
   'Confirm operating ownership'],
  ('Is billed percentage a substitute for work completed?',
   'Billing follows the agreement. Verify progress and remaining work separately.'),
  ['acquisition-backlog-due-diligence', 'deferred-revenue-business-acquisition']),
 ('acquisition-customer-refund-exposure',
  'Customer Refund Exposure in Acquisition Diligence',
  'Estimate unresolved and recurring refund exposure using transaction records and contract or policy '
  'evidence.',
  'Review refund claims and settlement history alongside customer balances and service problems.',
  [('Classify the exposure',
    'Collect dated refund requests, payment references, reason codes, approvals and settlement data. '
    'Separate open requests, approved refunds and payments already issued.'),
   ('Reconcile one reporting period',
    'A fictional report lists $18,000 approved for refund. Settlements show $11,000 issued and $2,000 '
    'attempted but failed. The buyer reviews the $7,000 still unresolved and keeps the failed payments '
    'visible until successfully retried.'),
   ('Carry findings into the model',
    'Ask advisers which obligations transfer and avoid double counting amounts already deducted in net sales '
    'or closing balances. Give the post-close owner a record of unresolved commitments.')],
  ['Match approvals to payments',
   'Identify failed settlements',
   'Check reporting treatment',
   'Assign post-close follow-up'],
  ('How should the buyer use historic refund rates?',
   'Compare comparable cohorts and review changes in products, policies and recurring causes before adopting '
   'a forecast rate.'),
  ['acquisition-customer-credit-memos', 'acquisition-customer-deposit-register']),
 ('acquisition-service-staffing-coverage',
  'Service Staffing Coverage Review Before Buying a Business',
  'Test whether scheduled staff and backup coverage can meet contracted service windows after closing.',
  'Start with customer hours and service commitments, then map which shifts and skills actually provide the '
  'coverage.',
  [('Build the staffing coverage grid',
    'Record contracted windows, required skills, scheduled people and backups. Verify what contractors, '
    'temporary staff and seller coverage contribute.'),
   ('Test an absence scenario',
    'A fictional service company needs two qualified technicians on Saturdays and normally schedules exactly '
    'two. Losing either technician leaves no covered slot. Price a backup rotation and assess which promises '
    'need escalation if coverage slips.'),
   ('Confirm the handover plan',
    'Check availability using authorized discussions. Estimate onboarding and training time and put any '
    'recurring staffing costs into the post-close forecast.')],
  ['Map service windows', 'Verify qualified coverage', 'Test absences', 'Budget for backups'],
  ('Can total headcount prove coverage?',
   'Use availability by time and skill. Total headcount can hide a gap on a critical shift.'),
  ['acquisition-service-level-commitments', 'handover-readiness-evidence'])])

TOPICS.extend([('acquisition-sales-commission-plan-review',
  'Sales Commission Plan Review Before Buying a Business',
  'Test how sales incentives, repayment triggers and payout timing affect margins and transition cash.',
  'Use the written plans and actual payout history to understand the economics of the sales engine being '
  'acquired.',
  [('Map the earning triggers',
    'Record commission bases, tiers, payout dates, treatment of returns, splits and exceptions. Compare the '
    'plan approved for each period with historical payments.'),
   ('Test the cost on one deal',
    'A fictional seller pays 5% on collected revenue. A $100,000 order is initially billed but only $80,000 '
    'has been collected. Under that example the result is $4,000 on current collections, with the remaining '
    'amount conditional on later payment.'),
   ('Review changes and closing responsibility',
    'Have qualified advisers assess obligations and the intended treatment across closing. Budget for any '
    'planned changes and estimate what happens if core producers leave.')],
  ['Collect signed plans',
   'Trace actual payouts',
   'Model returns and delays',
   'Discuss transition treatment'],
  ('Why check prior payouts alongside written terms?',
   'Actual payouts can reveal exceptions or practices that are absent from the documents and relevant to '
   'transition planning.'),
  ['employee-accruals-acquisition-diligence', 'acquisition-sales-pipeline-quality']),
 ('acquisition-data-migration-reconciliation',
  'Customer Data Migration Reconciliation for Acquisitions',
  'Verify that customer and order records survive an approved system migration with their relationships '
  'intact.',
  'Use authorized export and import procedures, then verify coverage with agreed record counts and test '
  'cases.',
  [('Define the data baseline',
    'Record exported and excluded fields, entity counts, creation and update cutoffs, and relationship keys. '
    'Obtain authorized access through the intended process and avoid replicating unnecessary personal data.'),
   ('Test duplicates and attachments',
    'A fictional buyer imports 11,000 source contacts and sees 10,850 in the target. Check whether '
    'documented merges explain 150 fewer contacts, then sample the links to orders and attachments.'),
   ('Sign off the operating handoff',
    'Require the account owner to find a test customer, open its most recent order, and verify the fields '
    'used for service and billing. Document unresolved gaps and who decides whether they delay cutover.')],
  ['Document allowed scope', 'Reconcile record counts', 'Check relationships', 'Get operating sign-off'],
  ('Can exact counts prove a sound migration?',
   'Counts should reconcile, and field accuracy, relationships, permissions and workflow usability need '
   'separate checks.'),
  ['acquisition-software-license-transfer', 'handover-readiness-evidence']),
 ('acquisition-customer-contract-exception-log',
  'Customer Contract Exception Log for Acquisition Diligence',
  'Find customer-specific promises that may change renewal risk, delivery cost or responsibility after '
  'closing.',
  'Identify deviations from standard sales terms and record the evidence for each material exception.',
  [('Compare contracts and actual practices',
    'Review signed schedules, amendments, invoicing and account notes. Document which source establishes an '
    'exception and who can explain unresolved differences.'),
   ('Estimate operating impact',
    'A fictional customer gets no-charge emergency visits under an amendment. The account records show 12 '
    'visits at $220 estimated direct cost each. The buyer places a $2,640 annual assumption in the model and '
    'tests a higher-usage case.'),
   ('Transfer decisions with the account',
    'Ask counsel and the diligence team to review binding terms. Give the account and delivery owners a '
    'dated record of applicable promises and exceptions to standard procedures.')],
  ['Collect approved amendments',
   'Compare service history',
   'Estimate direct costs',
   'Assign an account owner'],
  ('What if a promise only appears in account notes?',
   'Preserve the evidence, verify the history, and get advice on whether and how it affects the deal and '
   'operating plan.'),
  ['acquisition-service-level-commitments', 'acquisition-customer-contract-rate-review'])])

TOPICS.extend([('acquisition-key-person-interview-plan',
  'Key Person Interview Plan for Business Buyers',
  'Prepare authorized diligence interviews around real decisions, controls and customer relationships.',
  'Agree who can be contacted through the deal process and give each interview a concrete operating '
  'question.',
  [('Map questions to evidence',
    'Ask about representative shifts, recurring decisions and unusual escalations. Compare statements with '
    'approved workflow records where available.'),
   ('Trace a specific handoff',
    'A manager says their team approves routine quotes, but three sample quotes all show a seller signature. '
    'Ask what triggered the escalations and whether the written approval boundary reflects practice.'),
   ('Document evidence and uncertainty',
    'Summarize what the interview supports, record conflicting accounts without speculation, and assign a '
    'follow-up owner before relying on the result.')],
  ['Confirm authorized contact', 'Choose a sample workflow', 'Compare evidence', 'Record unresolved claims'],
  ('Should every employee be interviewed?',
   'Work through the authorized deal process and prioritize roles whose decisions or knowledge materially '
   'affect continuity.'),
  ['owner-dependence-due-diligence', 'key-manager-transition-plan']),
 ('acquisition-contractor-capacity-review',
  'Contractor Capacity Review Before Buying a Business',
  'Test continuity, costs and scheduling risk for contractors who perform essential work.',
  'Map which contract teams support customer commitments and whether the buyer has documented access to that '
  'capacity.',
  [('Build a dependency list',
    'Collect agreements, availability windows, recent invoices, skills and backup alternatives. Identify '
    'where the seller personally manages bookings.'),
   ('Stress-test a coverage gap',
    'A field service buyer expects 32 weekly installation hours from one crew. The crew can commit to only '
    '20 after close. Estimate the cost and lead time to cover the missing 12 hours before promising the '
    'existing volume.'),
   ('Verify the operating response',
    'Ask qualified advisers to review contracts and obligations. Give scheduling an approved backup and '
    'update service forecasts when availability changes.')],
  ['Collect agreements', 'Measure committed hours', 'Model a shortfall', 'Identify backup capacity'],
  ('How should verbal availability be modeled?',
   'Use a separate scenario until the buyer can verify timing and applicable terms through an authorized '
   'source.'),
  ['acquisition-service-staffing-coverage', 'supplier-concentration-acquisition']),
 ('acquisition-order-to-cash-walkthrough',
  'Order-to-Cash Walkthrough for Acquisition Diligence',
  'Follow a completed transaction from order approval to fulfillment, invoicing and collection.',
  'Choose transactions that reflect the way the target earns and collects revenue, including one that '
  'required an exception.',
  [('Collect each handoff record',
    'Trace the signed order, release, delivery proof, invoice, adjustments and settlement. Note each control '
    'owner and any manual re-entry.'),
   ('Find the delay',
    'A customer accepts a job on Monday, it finishes Friday, and billing waits 10 days for emailed evidence. '
    'Distinguish the invoice creation delay from the agreed payment period when modeling cash.'),
   ('Design the transition check',
    'Assign an owner to perform each handoff after close. Re-run the walkthrough using a sample transaction '
    'in any approved replacement system before relying on its output.')],
  ['Select routine and exceptional orders',
   'Trace approval through cash',
   'Separate processing delays',
   'Confirm post-close owners'],
  ('Why inspect an exceptional order?',
   'Exceptions expose approvals and manual steps that can remain invisible in a clean routine transaction.'),
  ['acquisition-revenue-reconciliation', 'acquisition-cash-conversion-cycle'])])


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
