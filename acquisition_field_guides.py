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

TOPICS.extend([('acquisition-owner-expense-reconciliation',
  'Owner Expense Reconciliation in Acquisition Diligence',
  'Trace proposed owner expense adjustments to records and replacement costs.',
  'Start with the proposed adjustments and the reason each expense might change under new ownership.',
  [('Request line-level evidence',
    'Ask for ledger lines and supporting invoices. Record business purpose, covered period, category and who '
    'reviewed the proposed adjustment.'),
   ('Test replacement cost',
    'A seller adds back $30,000 for a vehicle. The buyer expects to retain a service vehicle costing $18,000 '
    'per year. Evaluate the proposed increase in earnings after allowing for the needed replacement cost.'),
   ('Reconcile the normalized model',
    'Ask the diligence accountant to review material adjustments and verify that an expense listed '
    'separately does not already appear in another adjustment.')],
  ['Trace to ledger', 'Document business purpose', 'Estimate replacement expense', 'Check for duplicates'],
  ('Can every owner-related expense be removed?',
   'Evaluate whether the buyer still needs the service or asset to operate and whether another cost replaces '
   'it.'),
  ['sde-add-backs-explained', 'acquisition-gross-margin-bridge']),
 ('acquisition-cash-disbursement-controls',
  'Cash Disbursement Controls Review Before Buying a Business',
  'Walk through vendor payments and confirm approval, recordkeeping and post-close responsibilities.',
  'Select routine and exceptional vendor payments that represent how money moves in the target business.',
  [('Trace the payment file',
    'Review invoice approval, supporting purchase records, authorized changes to remittance instructions, '
    'payment confirmation and reconciliation.'),
   ('Review a payment exception',
    'A fictional invoice from a familiar supplier includes new bank instructions. The buyer asks whether the '
    'team verified the change through its established supplier contact and documented approval before '
    'releasing payment.'),
   ('Identify the closing handoff',
    'Record which staff or providers initiate and approve payments and who reconciles the bank. Confirm '
    'approved coverage after closing without sharing credentials in the diligence log.')],
  ['Select a representative sample',
   'Check invoice and approval',
   'Review remittance changes',
   'Confirm handover coverage'],
  ('Why inspect an exception as well as a routine payment?',
   'An exception shows who can verify unusual requests and whether approval holds up when the usual process '
   'changes.'),
  ['acquisition-open-purchase-orders', 'day-one-acquisition-continuity-checklist']),
 ('acquisition-price-increase-exposure',
  'Supplier Price Increase Exposure in Acquisitions',
  'Check which upcoming supplier price changes may compress margins after closing.',
  'Map documented supplier price changes against order timing, inventory coverage, and customer pricing '
  'flexibility.',
  [('Build the effective-date view',
    'Collect approved rate notices, purchase commitments, quantities, and recent invoices. Identify whether '
    'prices change at order, shipment, or billing under the applicable documents.'),
   ('Measure the exposure',
    'A fictional buyer uses 800 units per month. A supplier increases cost from $15 to $17. With no offset, '
    'expected monthly direct cost increases by $1,600 once affected inventory flows through.'),
   ('Model offset and delay',
    'Compare alternatives, remaining stock and customer pricing terms. Document lead time and cost for any '
    'tested offset and keep it separate from the baseline until supported.')],
  ['Verify rates and dates', 'Estimate affected volume', 'Model margin and cash', 'Test offsets'],
  ('Do higher replacement prices affect all current inventory immediately?',
   'Model purchasing and inventory flow separately. Cash outflow and cost recognition can occur in different '
   'periods.'),
  ['acquisition-supplier-payment-terms', 'acquisition-gross-margin-bridge'])])

TOPICS.extend([('acquisition-supplier-rebate-reconciliation',
  'Supplier Rebate Reconciliation in Acquisition Diligence',
  'Connect supplier rebate income to documented terms, qualifying spend and cash receipts.',
  'Build the review around the vendor program and the purchases that support the reported amount.',
  [('Collect terms and source records',
    'Record program period, qualifying products, exclusions, tiers and payment timing. Match eligible '
    'purchases to vendor statements and identify amounts still pending.'),
   ('Calculate the amount at risk',
    'A fictional distributor receives a 3% rebate on qualifying purchases once $500,000 is reached. The '
    'seller qualified last year, but the buyer forecasts $450,000. The buyer tests margins with no rebate '
    'under those terms.'),
   ('Verify cash and continuation',
    'Reconcile credits or deposits to the amounts recorded and have the deal team verify which terms are '
    'available to the buyer. Keep disputed estimates separate from confirmed program amounts.')],
  ['Collect program terms',
   'Reconcile qualified purchases',
   'Recalculate threshold scenarios',
   'Trace credits or receipts'],
  ('Can the buyer assume last year’s rebate repeats?',
   'Check the expected purchasing mix, eligibility, program availability and settlement terms before '
   'including it.'),
  ['acquisition-supplier-payment-terms', 'acquisition-gross-margin-bridge']),
 ('acquisition-facility-utility-capacity',
  'Facility Utility Capacity Review Before Buying a Business',
  'Verify that electricity, water, compressed air and other critical utilities support the buyer’s operating '
  'plan.',
  'Identify utilities that constrain production or service availability and determine what supports the '
  'capacity estimate.',
  [('Collect capacity evidence',
    'Review utility bills, equipment specifications, site drawings and recorded operating constraints with '
    'qualified personnel. Identify maintenance and approval responsibilities.'),
   ('Test simultaneous load',
    'A fictional shop wants to run new finishing equipment during a shift when two existing loads are '
    'already near the documented limit. The buyer asks a qualified engineer to verify conditions and '
    'compares staggered operation with an upgrade.'),
   ('Budget a continuity plan',
    'Model ongoing usage, potential downtime, and any supported upgrade costs and lead time. Do not assume '
    'the added equipment can run until the responsible team confirms readiness.')],
  ['Gather site records', 'Identify peak loads', 'Obtain qualified review', 'Model timing and cost'],
  ('Can the utility bill prove spare capacity?',
   'Bills establish historical usage. Verify peak conditions and usable capacity separately with qualified '
   'specialists.'),
  ['acquisition-real-estate-lease-review', 'acquisition-equipment-downtime-review']),
 ('acquisition-customer-order-cancellation',
  'Customer Order Cancellation Exposure in Acquisition Diligence',
  'Estimate the impact of canceled orders and identify which backlog items can be relied on.',
  'Use actual cancellation behavior and signed commitments to understand which open orders may disappear '
  'before fulfillment.',
  [('Reconcile cancellations to original orders',
    'Collect event date, order value, reason, deposits, approved changes, and whether the order returned '
    'later. Use comparable order-stage cohorts.'),
   ('Measure exposure by stage',
    'A fictional seller enters $500,000 of new committed orders in one quarter and cancels $40,000 from that '
    'cohort before fulfillment. The buyer tracks 8% by value and checks whether a single project dominates '
    'the result.'),
   ('Translate the result into scenarios',
    'Have advisers review cancellation or refund rights. Model which materials or labor are already '
    'committed and estimate cash impact if the orders cancel.')],
  ['Track cohort and reason',
   'Check approval evidence',
   'Estimate sunk commitments',
   'Stress-test the largest items'],
  ('Should canceled and delayed orders be combined?',
   'Track cancellations and delays distinctly so lost demand and shifts in cash timing remain visible.'),
  ['acquisition-backlog-due-diligence', 'acquisition-customer-deposit-register'])])

TOPICS.extend([('acquisition-customer-service-credit-exposure',
  'Service Credit Exposure Before Buying a Business',
  'Estimate credits caused by missed service commitments and trace unsettled amounts to specific contracts.',
  'Start with signed service terms, performance evidence and issued credits.',
  [('Map credit triggers',
    'Record measurement windows, definitions, limits and any notice requirements for material agreements.'),
   ('Reconcile actual records',
    'A fictional account has a monthly service fee of $30,000 and receives a 5% credit for a missed measure '
    'under its agreement. The buyer validates the $1,500 against the service log and credit memo.'),
   ('Review expected recurrence',
    'Ask the operating lead what would prevent a repeat. Confirm with advisers whether open credits already '
    'appear in receivables, net revenue or a closing adjustment.')],
  ['Collect signed terms', 'Recalculate a sample', 'Trace credit memos', 'Assess recurrence'],
  ('What if service logs disagree with the credit memo?',
   'Trace both to the reporting period and look for a documented exception before relying on either amount.'),
  ['acquisition-service-level-commitments', 'acquisition-customer-credit-memos']),
 ('acquisition-customer-implementation-cost',
  'Customer Implementation Costs in Acquisition Diligence',
  'Estimate how much labor, training and vendor support new customers require before recurring contribution '
  'begins.',
  'Cohort analysis can show the upfront cash cost of converting signed customers into active accounts.',
  [('Define implementation work',
    'Include setup, integration, training, repeated visits and third-party charges. Separate collected setup '
    'fees and recurring service costs.'),
   ('Measure a rollout cohort',
    'A fictional cohort of 12 accounts costs $1,500 each to activate and generates $500 per account in setup '
    'cash. Model the remaining $12,000 initial cash gap before recurring collections.'),
   ('Stress-test a slower rollout',
    'Inspect failed and delayed installations and test which costs repeat if go-live moves. Use the result '
    'in cash and staffing forecasts.')],
  ['List activation tasks', 'Allocate direct costs', 'Reconcile setup fees', 'Model delays'],
  ('Should buyer use average cost for every account?',
   'Compare equivalent scopes and evaluate unusually complex accounts separately.'),
  ['seasonal-cash-flow-acquisition', 'acquisition-work-in-progress-review']),
 ('acquisition-expedited-shipping-cost',
  'Expedited Shipping Cost Review Before an Acquisition',
  'Identify when freight premiums hide shortages, late orders or unsustainable service assumptions.',
  'Review expedited freight separately from standard shipments, using the reason and party bearing the cost.',
  [('Reconcile charges',
    'Match carrier invoices, order deadlines, supplier delays and customer reimbursements. Verify whether '
    'premiums are included in the reported direct costs.'),
   ('Test a concentrated issue',
    'A fictional distributor incurs $24,000 in expedite charges in one quarter, $15,000 tied to one '
    'supplier’s late deliveries. Assess whether a credible alternate source or earlier purchasing would '
    'change the cost.'),
   ('Carry evidence into the model',
    'Keep recorded costs in the baseline and describe any improvement case with the proposed change, '
    'evidence and timing.')],
  ['Match carrier invoices',
   'Identify recurring causes',
   'Check reimbursements',
   'Model supported alternatives'],
  ('Should unusual freight be added back?',
   'Review whether the underlying cause persists and how the buyer would meet the same commitments.'),
  ['supplier-concentration-acquisition', 'acquisition-gross-margin-bridge'])])

TOPICS.extend([('acquisition-customer-price-escalation',
  'Customer Price Escalation Clauses in Acquisition Diligence',
  'Map what customer agreements actually permit the business to charge as operating costs change.',
  'Separate proposed increases, permitted increases, and changes already reflected in actual customer bills.',
  [('Build an escalation calendar',
    'Record terms, calculation base, notice window, effective date and caps from the signed documents. '
    'Verify the contract version and invoice owner.'),
   ('Test offset timing',
    'A fictional operator expects supplier costs to rise by $30,000 annually. A potential customer increase '
    'offsets $18,000 at a full run rate, but takes effect six months later. Model the delay separately from '
    'the eventual contribution.'),
   ('Verify before forecasting',
    'Ask qualified advisers to review material clauses and confirm how notices are handled. Reconcile '
    'forecast amounts to invoices as increases take effect.')],
  ['Collect terms and amendments',
   'Verify dates and caps',
   'Model timing and margin',
   'Confirm notice ownership'],
  ('Can the buyer assume a full-year offset?',
   'Only model a full-year effect in periods when the higher rate applies to the relevant orders.'),
  ['acquisition-customer-contract-rate-review', 'acquisition-price-increase-exposure']),
 ('acquisition-warranty-supplier-recovery',
  'Supplier Warranty Recovery in Acquisition Diligence',
  'Reconcile supplier reimbursements against warranty costs and check whether claims remain collectible.',
  'Use the work order and supplier claim as separate records, then link them for analysis.',
  [('Trace eligible claims',
    'Gather supplier terms, approval records, affected parts, claim deadlines, and credits. Separate '
    'submitted claims from accepted or paid claims.'),
   ('Test net exposure',
    'A fictional seller records $38,000 of gross warranty costs and $12,000 in expected supplier recovery. '
    'The buyer finds evidence of $8,000 accepted by the supplier and models the remaining $4,000 as a '
    'separate outcome.'),
   ('Verify transition ownership',
    'Ask the deal team to confirm which balances and responsibilities transfer. Give an authorized team '
    'member the next action and deadline for unresolved claims.')],
  ['Gather claim terms', 'Tie claims to work orders', 'Reconcile credits', 'Assign follow-up'],
  ('Is expected supplier recovery the same as a settled credit?',
   'Track expected, approved, and settled amounts independently until the transaction is reconciled.'),
  ['acquisition-warranty-claims-review', 'acquisition-supplier-rebate-reconciliation']),
 ('acquisition-overtime-coverage-cost',
  'Overtime Coverage Cost Review Before Buying a Business',
  'Check whether overtime is driven by seasonal demand, staffing gaps or training requirements before '
  'forecasting labor costs.',
  'Review paid hours by shift and work type alongside jobs completed, schedules and planned headcount.',
  [('Reconcile the labor evidence',
    'Compare payroll summaries, scheduled shifts and job records for comparable periods. Identify seasonal '
    'peaks, vacant shifts and unusual customer commitments.'),
   ('Model a coverage alternative',
    'A fictional operation uses 160 overtime hours monthly at a loaded rate of $48. It expects to replace '
    '100 hours with regular coverage at $34. The direct modeled saving is $1,400 before considering hiring, '
    'training, scheduling and coverage costs.'),
   ('Check post-close feasibility',
    'Have operations test whether the intended staffing plan covers the same work and service windows. '
    'Retain a downside case until the additional coverage is demonstrated.')],
  ['Align records and periods',
   'Classify overtime causes',
   'Calculate alternative coverage',
   'Validate service capacity'],
  ('Should overtime be removed as a one-time cost?',
   'Assess whether the underlying work and staffing conditions persist before making any diligence '
   'adjustment.'),
  ['acquisition-service-staffing-coverage', 'acquisition-contractor-capacity-review'])])

TOPICS.extend([('acquisition-equipment-lease-obligations',
  'Equipment Lease Obligations in Acquisition Diligence',
  'Reconcile leased equipment, scheduled payments and end-of-term responsibilities before closing.',
  'Start with executed agreements and confirm the assets the operating team expects to use.',
  [('Build the lease schedule',
    'Record asset, term, recurring cash payments, renewal or return dates, purchase options and maintenance '
    'obligations. Match the lease to serial numbers and recent bills.'),
   ('Test near-term cash needs',
    'A fictional business pays $1,200 monthly for equipment with eight months remaining and an optional '
    '$8,000 purchase at the end. Compare the payment schedule and option with replacement cost and operating '
    'downtime.'),
   ('Confirm continuity',
    'Ask advisers to check assignment and approval requirements. Give one operator responsibility for '
    'confirming equipment access and upcoming decision dates after closing.')],
  ['Collect signed agreements',
   'Match assets and invoices',
   'Model end-of-term choices',
   'Verify permitted transfer'],
  ('Does a remaining-payment total capture the obligation?',
   'Include any relevant return, maintenance and transition costs in the scenario, with options shown '
   'separately.'),
  ['acquisition-fixed-asset-ownership', 'acquisition-third-party-permissions']),
 ('acquisition-billing-cutover',
  'Billing Cutover Checklist for Business Acquisitions',
  'Prevent missed or duplicate invoices when billing moves to a buyer’s systems or team.',
  'Give each invoice population one responsible team and one set of cutoff rules.',
  [('Map the cutover by invoice type',
    'Identify recurring, milestone and usage-based bills. Record the system of record, required inputs, '
    'responsible owner and expected first run.'),
   ('Reconcile across the cutoff',
    'A fictional subscription company has 280 renewals scheduled for the first week. The legacy run '
    'processes 60 before cutoff. The buyer reconciles the remaining 220 against the authorized import and '
    'checks exceptions before sending bills.'),
   ('Validate first-week output',
    'Use sample runs to verify dates, rates and totals. Follow the deal team’s instructions on '
    'responsibilities and customer communications, then check the first settlement and credit activity.')],
  ['Map invoice populations',
   'Assign cutoff ownership',
   'Test sample invoices',
   'Reconcile first-run totals'],
  ('Should both teams issue invoices as a fallback?',
   'Give one team billing authority for each population and retain a reconciliation so a fallback does not '
   'issue duplicates.'),
  ['acquisition-order-to-cash-walkthrough', 'handover-readiness-evidence']),
 ('acquisition-order-fulfillment-lead-time',
  'Order Fulfillment Lead Time in Acquisition Diligence',
  'Test promised delivery dates using historical throughput, missing inputs and real capacity.',
  'Compare what customers were promised with when qualifying orders actually shipped or finished.',
  [('Measure from a consistent event',
    'Record order approval, release, shortages, fulfillment and delivery where available. Document which '
    'events start and stop the measurement.'),
   ('Identify the source of delay',
    'A fictional company promises five business days and takes nine for 14 sampled orders. Ten of those '
    'orders wait three or more days for one component. Inspect confirmed lead times and whether more buffer '
    'stock changes cash needs.'),
   ('Model the buyer’s operating plan',
    'Estimate realistic shipment and collection dates under the planned capacity. Give operations an '
    'escalation path for commitments at risk after close.')],
  ['Define the clock', 'Compare promises and actuals', 'Trace recurring blockers', 'Model cash timing'],
  ('Does average lead time show missed commitments?',
   'Check the share beyond promised dates and inspect long-tail delays alongside the average.'),
  ['acquisition-backlog-due-diligence', 'acquisition-supplier-payment-terms'])])

TOPICS.extend([('acquisition-outsourced-payroll-handoff',
  'Outsourced Payroll Provider Handoff in an Acquisition',
  'Plan payroll provider responsibilities and first-cycle evidence without exchanging credentials or '
  'exposing employee files.',
  'Coordinate with authorized payroll owners and advisers to identify the first cycle each team owns.',
  [('Build the pay-cycle calendar',
    'Record pay-period and submission cutoffs, responsible employer or business entity, approved signers and '
    'vendor support. Confirm which qualified adviser handles jurisdiction-specific questions.'),
   ('Walk through the first cycle',
    'A buyer closes Thursday and the next payroll submission is due Monday. The payroll lead documents who '
    'validates hours, who authorizes the file, and what confirmation will show the provider accepted it.'),
   ('Establish continuity evidence',
    'Use authorized test procedures and retain only necessary summary evidence in the diligence log. Confirm '
    'responsible owners for failed items and employee inquiries.')],
  ['Map first pay dates',
   'Confirm provider ownership',
   'Test authorized workflow',
   'Verify exception contacts'],
  ('Should the buyer adopt the seller’s login?',
   'Obtain approved access through the provider and verify the intended roles through the deal process.'),
  ['day-one-acquisition-continuity-checklist', 'employee-accruals-acquisition-diligence']),
 ('acquisition-returns-authorization-cutover',
  'Returns Authorization Cutover When Buying a Business',
  'Transfer open returns and promised dispositions without losing refund or replacement commitments.',
  'Start with returns already promised and establish which authorized team can approve each next step.',
  [('Build the open returns register',
    'Record the original sale, authorization date, item condition, expected disposition, deadlines and '
    'settlement status. Match physical returns to customer and finance records.'),
   ('Walk a split case through closing',
    'A customer’s replacement was shipped before close but the original unit arrives after close. Identify '
    'who checks receipt and whether the agreement calls for a refund, a stock adjustment or closure only.'),
   ('Reconcile the first week',
    'Have advisers confirm which obligations transfer and give operating leads responsibility for unresolved '
    'cases. Verify credits and replacement records against the original order.')],
  ['List open returns',
   'Match customer promises',
   'Confirm settlement ownership',
   'Review first-week exceptions'],
  ('Why include replacements already shipped?',
   'The business may still need to inspect the original unit, update stock, or settle a charge when it '
   'arrives.'),
  ['acquisition-customer-refund-exposure', 'acquisition-billing-cutover']),
 ('acquisition-supplier-onboarding-timing',
  'Supplier Onboarding Timing in Acquisition Diligence',
  'Estimate when the buyer can place its first accepted order with essential suppliers.',
  'Map the administrative and operational steps suppliers require before they accept orders from the '
  'purchasing entity.',
  [('Identify required approvals',
    'Request the supplier’s authorized onboarding process, account lead time, credit requirements, ordering '
    'method and cutoff. Compare those dates with key material requirements.'),
   ('Run a dated supply scenario',
    'A buyer needs materials 18 days after closing. Account setup takes 10 days and delivery takes 12 after '
    'order. Identify a four-day gap and evaluate whether previously authorized orders or temporary stock can '
    'cover it.'),
   ('Assign continuity checks',
    'Have the deal team approve correspondence and responsibilities. Verify the first test order, delivery '
    'promise and approved payment setup before treating the dependency as resolved.')],
  ['List essential suppliers',
   'Confirm lead times',
   'Model the readiness gap',
   'Verify first-order ownership'],
  ('Is an approved application enough to show readiness?',
   'Confirm the supplier can accept the buyer’s order under the documented terms and provide a delivery '
   'date.'),
  ['acquisition-third-party-permissions', 'acquisition-open-purchase-orders'])])

TOPICS.extend([('acquisition-consignment-inventory-review',
  'Consignment Inventory Review Before Buying a Business',
  'Verify who owns consigned stock, what triggers settlement and how balances transfer.',
  'Compare the signed agreements with physical stock and inventory records before including consigned goods '
  'in a deal model.',
  [('Separate each ownership direction',
    'List supplier-owned stock on site and target-owned stock held elsewhere. Record location, lot, '
    'condition, reporting requirements and who bears losses.'),
   ('Reconcile transactions and settlement',
    'A buyer finds 400 units in a target warehouse, 90 supplied on consignment. Compare supplier statements '
    'and sales events to identify sold units awaiting settlement and stock still owned by the supplier.'),
   ('Assign post-close responsibility',
    'Ask the deal team to review contractual and accounting treatment. Have operations confirm who reports '
    'movement and who reconciles opening balances after close.')],
  ['Identify legal owners',
   'Reconcile stock by location',
   'Trace settlement events',
   'Confirm operating ownership'],
  ('Should consigned stock appear in the purchased inventory count?',
   'Count the physical stock, identify ownership separately, and apply the transaction’s agreed definitions '
   'with adviser review.'),
  ['inventory-due-diligence-small-business', 'acquisition-inventory-shrink-review']),
 ('acquisition-customer-support-cutover',
  'Customer Support Cutover Checklist for Acquisitions',
  'Transfer open issues, promised callbacks and escalation responsibilities into the buyer’s support '
  'workflow.',
  'Inventory the customer support channels and establish who owns each open item at the cutover.',
  [('Build the transfer register',
    'Capture case reference, customer impact, last contact, promised response, escalation and assigned '
    'owner. Keep supporting material within the approved system and scope.'),
   ('Walk one urgent case through close',
    'A priority case has a Friday repair promise and the technician changes employer Thursday. The buyer '
    'verifies authorization to dispatch the technician, confirms the case owner and checks who communicates '
    'schedule changes.'),
   ('Verify the first support cycle',
    'Test agreed phone and email routing, trace one new request to its destination and review the backlog '
    'for commitments that no team owns.')],
  ['List inbound channels',
   'Assign open commitments',
   'Verify authorized access',
   'Check first-week routing'],
  ('What should be included in the cutover test?',
   'Confirm a new request reaches the assigned team and a transferred case retains its promised response '
   'time and history.'),
  ['day-one-acquisition-continuity-checklist', 'acquisition-returns-authorization-cutover']),
 ('acquisition-customer-prepayment-seasonality',
  'Customer Prepayment Seasonality in Acquisition Cash Flow',
  'Model how seasonal prepayments affect cash availability and fulfillment costs across closing.',
  'Map expected service obligations against the months when customers typically pay in advance.',
  [('Build a dated collection and delivery schedule',
    'Record amount, payment date, coverage period, associated costs and refund terms. Reconcile a sample to '
    'invoices and cash receipts.'),
   ('Stress-test closing timing',
    'A fictional business collects $180,000 in spring for annual service and expects $90,000 in direct cost '
    'across the following nine months. A midsummer buyer models remaining work and asks which cash and '
    'obligations the transaction transfers.'),
   ('Compare cash and accounting views',
    'Have the deal team assess the agreed closing economics. Test late collections and higher fulfillment '
    'spending without assuming prepayment cash will be available after close.')],
  ['Map receipt dates',
   'Match obligations to costs',
   'Model alternate closing dates',
   'Verify deal definitions'],
  ('Does annual profitability show the full cash risk?',
   'Use monthly cash flows to show when customers pay, when the team performs the work and what funding '
   'remains available.'),
  ['deferred-revenue-business-acquisition', 'seasonal-cash-flow-acquisition'])])

TOPICS.extend([('acquisition-merchant-settlement-cutover',
  'Merchant Settlement Cutover for Acquisitions',
  'Reconcile payment processor settlements across closing and assign owners for delayed deposits and '
  'disputes.',
  'Identify the authorized merchant accounts, settlement windows and who owns exceptions around the closing '
  'date.',
  [('Reconcile transactions to batches',
    'Capture transaction date, gross amount, fees, reversals, payout date and responsible entity. Confirm '
    'authorized access with the payment provider.'),
   ('Trace a cross-close batch',
    'A fictional Friday batch contains $18,000 in sales and settles Tuesday with $550 in fees. The team ties '
    'the $17,450 payout to the batch and confirms treatment with the deal accountant.'),
   ('Validate the first buyer payout',
    'Verify a properly authorized transaction, settlement notice and reconciliation. Assign an owner for '
    'chargebacks and follow-up without putting credentials into the deal record.')],
  ['Match batch and payout dates',
   'Reconcile net deposits',
   'Confirm exception owners',
   'Verify the first payout'],
  ('Why check settlement dates alongside sales dates?',
   'A transaction can occur before closing and settle afterward, so each event needs its own date and '
   'disposition.'),
  ['acquisition-billing-cutover', 'acquisition-cash-conversion-cycle']),
 ('acquisition-inventory-in-transit',
  'Inventory in Transit Review Before Buying a Business',
  'Reconcile goods between suppliers and receiving locations and assign unresolved deliveries at closing.',
  'Create a shipment-level list for material items that may move across the closing cutoff.',
  [('Match shipments to purchase records',
    'Collect supplier confirmations, packing lists, carrier events and expected receipts. Trace deposits or '
    'invoices and record the destination and receiving owner.'),
   ('Check partial orders',
    'A buyer samples an order for 900 units. Six hundred have arrived and 300 remain in transit. Reconcile '
    'what the count includes and determine whether a previously paid deposit applies to one shipment or the '
    'full order.'),
   ('Review ownership and continuity',
    'Have advisers interpret agreed cutoff, ownership and closing treatment. Give operations an authorized '
    'route for tracing delayed shipments and confirming the first receipt.')],
  ['Trace orders to shipment events',
   'Separate received and in-transit stock',
   'Reconcile payments',
   'Confirm receiving ownership'],
  ('Does carrier tracking resolve ownership?',
   'Tracking establishes movement and delivery events. Review ownership and transaction treatment with '
   'supporting contracts and advisers.'),
  ['inventory-due-diligence-small-business', 'acquisition-open-purchase-orders']),
 ('acquisition-customer-reporting-obligations',
  'Customer Reporting Obligations in Acquisition Diligence',
  'Identify recurring reports the buyer must deliver and verify that operating data and review ownership '
  'transfer.',
  'List material customer reports and test how each one is assembled, approved and sent.',
  [('Build the reporting register',
    'Capture frequency, due dates, contract reference, approved recipients, source systems and reviewer. '
    'Identify restricted inputs and approved access.'),
   ('Run a representative report',
    'A fictional buyer can reproduce totals in a monthly service report but has no source for the prior '
    'month’s exceptions. Assign an owner to verify those records and document how reporting proceeds if the '
    'missing data persists.'),
   ('Verify operating readiness',
    'Have the intended owner reproduce one complete report in the approved environment and confirm '
    'recipients through the agreed process. Track any unresolved reporting commitment around closing.')],
  ['Map required reports', 'Verify source access', 'Reproduce a sample', 'Assign delivery owner'],
  ('Why verify a report before the handoff?',
   'The test shows whether the buyer can reconstruct the numbers, review the output and deliver it by the '
   'required date.'),
  ['acquisition-service-level-commitments', 'handover-readiness-evidence'])])

TOPICS.extend([('acquisition-accounts-payable-cutover',
  'Accounts Payable Cutover for Small Business Acquisitions',
  'Reconcile unpaid supplier invoices, pending payments and first-week approvals around closing.',
  'Build a dated cutoff schedule jointly with the authorized finance and deal teams.',
  [('Build a supplier invoice register',
    'Take a snapshot of open invoices, credits, receipt references, due dates and payments already '
    'scheduled. Capture the proposed responsible entity for review.'),
   ('Trace payment in flight',
    'A fictional company initiates an $8,000 payment Thursday and closes Friday before the bank settles it. '
    'The team marks the invoice pending, tracks the settlement, and agrees who handles it if the payment '
    'fails.'),
   ('Validate the first approval cycle',
    'Confirm approved roles and bank or payment provider access through normal channels. Reconcile the '
    'opening and first-week balances and give every difference an owner.')],
  ['Capture open invoices',
   'Flag payments in flight',
   'Confirm entity responsibility',
   'Reconcile first-week balances'],
  ('Why include invoices already entered for payment?',
   'Payment initiation and settlement happen at different times. Track both events to prevent a duplicate '
   'payment or missed obligation.'),
  ['acquisition-cash-disbursement-controls', 'acquisition-merchant-settlement-cutover']),
 ('acquisition-service-dispatch-system-test',
  'Dispatch System Readiness Test After an Acquisition',
  'Verify the buyer can assign, change and close representative service jobs in the approved environment.',
  'Select the jobs that most clearly show whether dispatch can serve customers from the first operating day.',
  [('Design representative tests',
    'Choose a routine appointment, an urgent reschedule and a job requiring a specific skill or part. Define '
    'observable results and use authorized test data.'),
   ('Exercise a reroute',
    'A fictional test moves a technician across two routes after a customer cancels. Verify the revised '
    'window, crew notice, visibility of unaffected jobs and how the system records a rollback.'),
   ('Record release conditions',
    'Assign an owner for each defect. Decide with operating leaders which problems must be addressed before '
    'release and verify the approved fallback before the first live shift.')],
  ['Choose a representative job', 'Exercise a schedule change', 'Validate notices', 'Reconcile the fallback'],
  ('Does successful sign-in establish readiness?',
   'Require the intended users to complete the dispatch actions and demonstrate exception handling with '
   'approved records.'),
  ['handover-readiness-evidence', 'acquisition-customer-support-cutover']),
 ('acquisition-recurring-invoice-rate-sampling',
  'Recurring Invoice Rate Sampling in Acquisition Diligence',
  'Check upcoming recurring bills against approved customer rates and renewal dates before operating '
  'handoff.',
  'Focus the sample on recurring charges whose timing or pricing changed near closing.',
  [('Define a risk-based sample',
    'Take accounts with recent renewals, open price disputes, volume tiers and planned increases. Use '
    'approved agreements, changes and prior invoices.'),
   ('Recalculate a sample invoice',
    'A fictional contract bills $500 for the first five units and $80 for each additional unit. Seven units '
    'should bill $660 before other agreed charges. Check for a stale flat rate or a volume tier applied to '
    'all units.'),
   ('Resolve mismatches before cutover',
    'Document whether the rate or the supporting data is wrong. Have authorized staff confirm fixes, run a '
    'sample bill and retain sign-off before the first recurring batch.')],
  ['Sample recent amendments',
   'Recalculate a tiered bill',
   'Resolve unsupported rates',
   'Verify the next run'],
  ('Is a clean live balance enough?',
   'Recompute upcoming invoices from written terms and the applicable usage. A reconciled prior balance can '
   'coexist with a future billing error.'),
  ['acquisition-customer-contract-rate-review', 'acquisition-billing-cutover'])])

TOPICS.extend([('acquisition-contract-auto-renewal-exposure',
  'Auto-Renewal Exposure in Acquisition Due Diligence',
  'Identify vendor contracts near automatic renewal and estimate the cost of missing notice dates.',
  'Begin with signed recurring agreements and put notice deadlines on the deal timeline.',
  [('Build a notice calendar',
    'Record renewal term, notice period, required delivery method, dates and authorized sender. Ask counsel '
    'to verify material timing and obligations.'),
   ('Model a missed decision',
    'A fictional supplier agreement renews for 12 months at $2,000 monthly. Its notice deadline falls one '
    'week before close. Compare using the contract, negotiating a change, or budgeting the $24,000 '
    'commitment if the seller takes no approved action.'),
   ('Assign a decision before close',
    'Have the deal team agree who can act and what evidence confirms delivery. Transfer unresolved '
    'commitments into the operating calendar.')],
  ['Collect signed amendments', 'Verify notice dates', 'Price renewal scenarios', 'Confirm action ownership'],
  ('Should notices be sent automatically?',
   'Have authorized personnel review whether renewal is desirable and confirm who may send any notice under '
   'the agreement.'),
  ['acquisition-supplier-payment-terms', 'acquisition-third-party-permissions']),
 ('acquisition-customer-installation-backlog',
  'Customer Installation Backlog Review Before Buying a Business',
  'Validate the resource needs and deadlines for installations already promised to customers.',
  'Connect pending installations to customer commitments, site readiness and actual field capacity.',
  [('Build an installation register',
    'Record site, approved work, required crew skills, equipment, access date, and next customer milestone. '
    'Flag jobs whose prerequisites are incomplete.'),
   ('Calculate a capacity gap',
    'A fictional buyer inherits 18 installs averaging four crew hours. Two crews each have 28 install hours '
    'available before the commitments fall due, leaving 16 uncovered hours before travel. Confirm which '
    'promised slots can move with customer approval.'),
   ('Verify first-week readiness',
    'Have scheduling confirm each customer window and the backlog owner. Put subcontractor or overtime costs '
    'into the transition budget only when coverage is feasible.')],
  ['Verify promised dates',
   'Confirm job prerequisites',
   'Calculate crew capacity',
   'Assign customer communication'],
  ('Should all pending jobs receive an installation slot?',
   'Distinguish confirmed commitments from jobs awaiting site readiness or approval before reserving scarce '
   'crew time.'),
  ['acquisition-backlog-due-diligence', 'acquisition-service-staffing-coverage']),
 ('acquisition-vendor-master-handoff',
  'Vendor Master Handoff for Business Acquisitions',
  'Transfer approved supplier records and preserve verification for new payment or contact details.',
  'Agree which vendor records the buyer needs and which team can approve them before the first payable run.',
  [('Define the authorized record set',
    'Map supplier identifiers, open items, approved contacts, status and reference documentation. Use '
    'restricted procedures for sensitive data and preserve required history.'),
   ('Test a possible duplicate',
    'A fictional export lists two vendors with the same trading name and distinct approved legal entities. '
    'Accounts payable keeps them separate and verifies which record owns each open balance.'),
   ('Verify the first payment cycle',
    'Match a sample invoice to the intended supplier and apply current verification procedures for '
    'remittance changes. Reconcile rejected records and assign an owner to resolve them.')],
  ['Define authorized data scope',
   'Identify possible duplicates',
   'Verify supplier mappings',
   'Test the first cycle'],
  ('Can the buyer trust all imported payment instructions?',
   'Follow established verification and approval procedures before relying on any instructions, especially '
   'changes received near the cutover.'),
  ['acquisition-accounts-payable-cutover', 'acquisition-cash-disbursement-controls'])])

TOPICS.extend([('acquisition-supplier-minimum-purchase',
  'Supplier Minimum Purchase Commitments in Acquisition Diligence',
  'Identify minimum purchase clauses, shortfall exposure and timing before finalizing a buyer’s forecast.',
  'Start with current executed supplier agreements and the purchases counted under each commitment.',
  [('Build a commitment schedule',
    'Record the measurement period, eligible purchases, true-up calculation, expiration, and counterparty. '
    'Match each obligation to a forecast line and actual purchase history.'),
   ('Estimate potential shortfall',
    'A fictional contract requires 10,000 qualifying units for the year and charges $4 for each unit below '
    'the minimum. A buyer forecasts 8,600 units. Under the stated assumptions, the shortfall charge would be '
    '$5,600.'),
   ('Compare documented options',
    'Consider planned demand, carrying costs, and any permitted renegotiation. Ask the deal team to review '
    'contractual treatment and record who owns the next threshold decision.')],
  ['Verify minimum terms',
   'Reconcile eligible purchases',
   'Calculate the shortfall',
   'Assign the next decision'],
  ('Can purchase forecasts substitute for eligible units?',
   'Use the contract’s eligibility terms and compare with dated actual purchases before determining the '
   'gap.'),
  ['acquisition-supplier-payment-terms', 'acquisition-supplier-rebate-reconciliation']),
 ('acquisition-customer-acceptance-backlog',
  'Customer Acceptance Backlog in Acquisition Diligence',
  'Identify delivered work still waiting for acceptance and test the effect on invoicing and cash.',
  'Separate orders awaiting delivery from work already delivered that still needs customer sign-off.',
  [('Build the acceptance queue',
    'Track delivery evidence, required approval, responsible account owner, billing trigger, and unresolved '
    'objections. Reconcile to open projects and invoice records.'),
   ('Trace delayed cash',
    'A fictional project earns a $22,000 final billing when the customer approves documentation. Work is '
    'finished, but a missing inspection report delays acceptance two weeks. Reflect the delay in the cash '
    'forecast and assign the missing input.'),
   ('Carry commitments through closing',
    'Have advisers review material acceptance and billing terms. Give the buyer a dated queue with a '
    'specified person to complete evidence and contact authorized customer representatives.')],
  ['Separate delivery and acceptance',
   'Confirm billing triggers',
   'Model collection timing',
   'Transfer follow-up ownership'],
  ('Can delivered work be treated as unconditional cash?',
   'Check whether acceptance or another contractual step must occur before invoicing or collection.'),
  ['acquisition-work-in-progress-review', 'acquisition-billing-cutover']),
 ('acquisition-open-service-escalations',
  'Open Customer Escalations Review Before an Acquisition',
  'Review the most material customer issues and assign responsibility for remedies, communications, and '
  'follow-up.',
  'Start with escalations that could disrupt a renewal, produce a remedy cost, or strain service capacity '
  'after closing.',
  [('Build an evidence-based issue register',
    'Capture account, problem, impacted service, promised response, known cost, responsible owner and '
    'relevant agreement. Distinguish requested remedies from approved ones.'),
   ('Walk a major account issue',
    'A fictional buyer finds an account awaiting a replacement visit and requesting a $6,000 credit. Verify '
    'whether the credit was approved, confirm who owns the visit, and model the documented remedy separately '
    'from the open request.'),
   ('Verify transition actions',
    'Align responsibility with the deal team and transfer only authorized records. Give the first operating '
    'week a due-date review for unresolved escalations.')],
  ['List material issues', 'Verify prior promises', 'Identify cost scenarios', 'Assign follow-through'],
  ('Should every open ticket enter the diligence log?',
   'Include issues material to continuity or economics and put ordinary cases in the approved support '
   'handoff.'),
  ['acquisition-customer-support-cutover', 'acquisition-customer-service-credit-exposure'])])

TOPICS.extend([('acquisition-seller-training-milestones',
  'Seller Training Milestones After an Acquisition',
  'Translate seller transition hours into specific training outcomes the buyer can verify.',
  'Start with tasks the team cannot yet perform independently and specify who must demonstrate each one.',
  [('Prioritize tasks by operational exposure',
    'Map recurring workflows, approval exceptions, customer introductions and undocumented records. Tie each '
    'session to the job the new owner needs to perform.'),
   ('Define a completion test',
    'A fictional buyer schedules two walkthroughs for a monthly supplier order. The buyer demonstrates a '
    'sample order using approved access, explains who approves a variance, and verifies where the record '
    'will be stored.'),
   ('Review unresolved tasks before hours expire',
    'Record evidence and outstanding dependencies at each milestone. Arrange interim coverage for critical '
    'tasks and discuss any agreement changes through the authorized deal team.')],
  ['List critical tasks',
   'Name a learner and verifier',
   'Record completion evidence',
   'Plan interim coverage'],
  ('Should hours alone count as completion?',
   'Use hours for scheduling and verify separately that the responsible person can perform the task under '
   'expected conditions.'),
  ['owner-dependence-due-diligence', 'handover-readiness-evidence']),
 ('acquisition-return-freight-cost',
  'Return Freight Cost Exposure in Acquisition Diligence',
  'Reconcile return shipping to credits and test which channels or product lines bear the cost.',
  'Start with orders returned in a completed cohort, including no-charge replacements and partial returns.',
  [('Collect charge and policy records',
    'Compare carrier bills, return authorizations, customer credits and supplier recoveries. Record who paid '
    'under the policy and who paid in practice.'),
   ('Test unit economics by channel',
    'A fictional channel has 150 returns, each averaging $18 of buyer-paid inbound freight. The baseline is '
    '$2,700 before handling. Separate $450 in verified reimbursements to estimate $2,250 in net freight.'),
   ('Check future policy assumptions',
    'Review material commitments with advisers and compare the cost under retained or altered sales '
    'channels. Ask operations to verify which return causes they can address.')],
  ['Match freight to returns', 'Verify reimbursements', 'Compute net cost', 'Model channel differences'],
  ('Is the refund total enough to estimate exposure?',
   'Trace freight, handling and recoveries separately to understand the operational cost of a return.'),
  ['acquisition-returns-authorization-cutover', 'acquisition-expedited-shipping-cost']),
 ('acquisition-inventory-obsolescence-review',
  'Inventory Obsolescence Review Before Buying a Business',
  'Evaluate whether slow or superseded stock can sell and how that affects expected recovery.',
  'Review inventory by item history, usable condition and realistic customer demand.',
  [('Build the aging and movement view',
    'Identify last receipts and sales, substitutions, current demand, restrictions, and how each item was '
    'valued by the seller.'),
   ('Estimate recovery under distinct scenarios',
    'A fictional business holds 300 units at $20 each. Regular demand supports 100 units and a buyer has a '
    'supported clearance offer of $8 for the remaining 200, before handling. Model both outcomes rather than '
    'relying on the $6,000 booked total.'),
   ('Confirm disposition and forecasts',
    'Have qualified advisers assess deal treatment. Assign an operating owner to verify demand and determine '
    'timing and costs for approved disposal or clearance.')],
  ['Compare movement and age',
   'Verify usable condition',
   'Model supported recovery',
   'Confirm deal treatment'],
  ('Should all slow stock be valued at zero?',
   'Tie estimated recovery to condition, documented demand, approved uses, and relevant disposal or selling '
   'costs.'),
  ['inventory-due-diligence-small-business', 'acquisition-inventory-shrink-review'])])

TOPICS.extend([('acquisition-open-freight-claims',
  'Open Freight Claims Review Before Buying a Business',
  'Reconcile unresolved carrier claims, customer commitments and replacement costs around closing.',
  'Start with shipments whose loss or damage created a material expected recovery or service obligation.',
  [('Build a claims register',
    'Record shipment, documented loss, claim date, replacement obligations, settlement status and next '
    'deadline. Verify expected recovery against actual correspondence.'),
   ('Trace a split obligation',
    'A fictional seller has replaced $9,000 of damaged goods but the carrier has acknowledged only $6,000. '
    'Model the replacement expense and possible recovery separately until settlement.'),
   ('Assign post-close follow-up',
    'Ask deal advisers to confirm who owns each claim and related customer commitment. Transfer approved '
    'evidence and give each unresolved item a dated action.')],
  ['Match claims to shipments',
   'Verify replacement commitments',
   'Separate possible recovery',
   'Name an owner'],
  ('Does filing a claim establish recovery?',
   'Use filing as evidence of a request. Verify acceptance, settlement terms and receipt separately.'),
  ['acquisition-inventory-in-transit', 'acquisition-expedited-shipping-cost']),
 ('acquisition-production-tooling-dependence',
  'Production Tooling Dependence in Acquisition Diligence',
  'Identify whether molds, fixtures and specialized tooling will remain available to the buyer.',
  'Map tooling that supports important customer orders or constrained operations.',
  [('Verify tooling records',
    'List the asset reference, location, owner, condition, supported products and access restrictions. Ask '
    'operating staff for evidence of actual use.'),
   ('Model a replacement delay',
    'A fictional target relies on a customer-owned fixture for one recurring product. A replacement would '
    'take six weeks. Verify permitted access and model delivery impact if the current fixture becomes '
    'unavailable.'),
   ('Check continuity at close',
    'Have advisers review rights and obligations. Assign a buyer-side owner to verify possession or '
    'authorized access, inspect the tooling and test a representative job.')],
  ['Map customer and supplier tooling',
   'Check condition and access',
   'Model replacement timing',
   'Verify day-one use'],
  ('Can ownership be inferred from storage location?',
   'Check documentation for ownership and permitted use. Tooling may be stored at the business while '
   'belonging to a customer or supplier.'),
  ['acquisition-fixed-asset-ownership', 'supplier-concentration-acquisition']),
 ('acquisition-order-entry-cutover',
  'Order Entry Cutover Checklist for Acquisitions',
  'Keep customer order channels and unentered commitments traceable across the closing date.',
  'Identify how orders arrive and give every inbound channel an owner for each side of the cutover.',
  [('Define the transfer population',
    'List email, portal, phone and recurring feeds. Reconcile approved orders waiting for entry and confirm '
    'which party owns open acknowledgments.'),
   ('Run an approved duplicate test',
    'A fictional buyer receives one order through both a portal and a customer email. Use the customer order '
    'number to match them, retain one accepted record and confirm only one shipment is scheduled.'),
   ('Verify the first operating cycle',
    'Trace a representative new order from receipt to scheduling and acknowledgment. Reconcile exceptions '
    'and document who can approve a manual fallback.')],
  ['Assign channel owners', 'List unentered orders', 'Test a duplicate', 'Verify the first acknowledgment'],
  ('What if some orders have no customer reference?',
   'Use authorized records to confirm the account, requested items and dates before deciding whether the '
   'requests match.'),
  ['acquisition-order-to-cash-walkthrough', 'acquisition-service-dispatch-system-test'])])

TOPICS.extend([('acquisition-supplier-payables-aging',
  'Supplier Payables Aging Review Before an Acquisition',
  'Reconcile aged supplier invoices and identify credit holds, disputes and near-term cash pressure.',
  'Review supplier balances with the actual due dates and supporting invoice records.',
  [('Build a risk-based sample',
    'Choose major suppliers, balances past due, recent term changes and disputed invoices. Compare '
    'statements with approved records and subsequent payments.'),
   ('Translate an aged balance into cash exposure',
    'A fictional target has $90,000 older than 60 days. Statements confirm $20,000 is disputed, $15,000 '
    'settled after cutoff and $55,000 remains outstanding without a documented dispute. Forecast the $55,000 '
    'with its expected timing, plus a separate dispute scenario.'),
   ('Verify the operating consequence',
    'Ask which suppliers can place orders on hold and review the agreed treatment of closing balances with '
    'advisers. Assign one post-close owner for the largest unresolved items.')],
  ['Sample high-risk suppliers', 'Trace later settlements', 'Separate disputes', 'Plan order continuity'],
  ('Does payable aging establish the total due at closing?',
   'Reconcile timing, credits and disputed items with source records and have the deal team apply the agreed '
   'closing definitions.'),
  ['acquisition-accounts-payable-cutover', 'acquisition-supplier-payment-terms']),
 ('acquisition-customer-renewal-cohort-forecast',
  'Customer Renewal Cohort Forecast for Business Buyers',
  'Forecast renewal cash by matching contracts, dates, historical cohorts and documented assumptions.',
  'Group eligible renewals by the month and type in which customers make the decision.',
  [('Prepare comparable cohorts',
    'Collect renewal eligibility, actual decision, effective date, value and whether agreements had price or '
    'scope changes. Separate customers outside the measurement window.'),
   ('Compare account and value measures',
    'In a fictional cohort, 18 of 20 accounts renew, or 90%. Renewed value is $140,000 of $200,000 eligible, '
    'or 70%. Model both measures to avoid hiding risk from larger accounts.'),
   ('Prepare buyer-side scenarios',
    'Map renewals near closing to account owners, check documented pricing and service issues, and use a '
    'separate delay case for material uncertain decisions.')],
  ['Confirm eligibility',
   'Compare counts and value',
   'Map dates near closing',
   'Stress-test larger accounts'],
  ('Should a signed renewal be grouped with forecasts?',
   'Keep signed and still-open renewals visible separately so forecasts can be reconciled as outcomes '
   'arrive.'),
  ['acquisition-customer-renewal-calendar', 'acquisition-customer-cohort-retention']),
 ('acquisition-replacement-inventory-cost',
  'Replacement Inventory Cost in Acquisition Diligence',
  'Test whether current vendor prices, pack sizes and freight change the cash needed to restock.',
  'Separate historic book cost from the cost to buy the next usable quantity.',
  [('Collect a restocking quote',
    'Confirm unit conversion, minimum purchase, effective price, freight and delivery lead time. Compare '
    'with current demand and authorized supply alternatives.'),
   ('Model the first order',
    'A fictional buyer needs 300 units. A supplier quotes $12 each with a 500-unit minimum and $300 freight. '
    'Budget $6,300 for the order and account for the 200 excess units separately.'),
   ('Link the cost to cash and margin',
    'Schedule payment on the terms actually available. Review how the change affects expected consumption '
    'and operating reserves, and discuss valuation effects with advisers.')],
  ['Verify buy and use units', 'Check minimum quantities', 'Include landed costs', 'Model payment dates'],
  ('Should book cost be used to forecast replenishment?',
   'Use current supported purchase assumptions for replenishment and keep book values in the appropriate '
   'historical or deal analysis.'),
  ['inventory-due-diligence-small-business', 'acquisition-price-increase-exposure'])])


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
