"""Editorial guides for owners choosing and rolling out AI tools."""
from html import escape

ROOT = "/ai/business-owners/"
CODEX = ("OpenAI Codex documentation", "https://openai.com/codex/")
CHATGPT = ("OpenAI guide to Projects in ChatGPT", "https://help.openai.com/en/articles/10169521-projects-in-chatgpt")
CLAUDE = ("Claude Help Center guide to Projects", "https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects")

GUIDES = [
    ("codex-for-business-owners", "OpenAI Codex for Business Owners",
     "Decide when to use Codex for business software, scope a first project, and prove your team can run it.",
     "Start with a decision someone makes by hand every week. An operations manager who combines two exports to identify late orders can start with one sanitized export, one report and one reviewer. Keep the existing spreadsheet available while the new report is tested.",
     ["Describe who runs the tool, which files it reads, and the output they need to make a decision.",
      "Give Codex a test fixture with five fictional orders, including a blank ship date and two rows with the same order ID.",
      "Ask for a local prototype and tests. Review the file changes with the person who will maintain the tool.",
      "Run the spreadsheet and prototype side by side. Move over only when the counts reconcile and the manager can handle errors without the original builder."],
     "The fixture has five rows but four distinct orders. Decide explicitly whether duplicates block the run or appear in a separate exceptions table. Make the reviewer confirm that rule before the prototype is used on real orders.",
     "Build a local prototype in this repository using the supplied fictional orders. Show late orders and list malformed or duplicate rows separately. Before editing, summarize the intended changes. Add tests for blanks and duplicates. Leave the existing workflow available.",
     CODEX),
    ("chatgpt-for-business-owners", "ChatGPT for Business Owners",
     "Choose a first ChatGPT workflow, test it on real business tasks, and measure whether it saves time after review.",
     "A useful first ChatGPT workflow takes a recurring set of inputs and turns it into a draft someone already knows how to review. Try a weekly owner brief before connecting systems or adding a new reporting obligation.",
     ["Collect the current KPI definitions, a blank brief and a sample with fictional values.",
      "If you use a ChatGPT Project, add the approved reference material and instructions about how to cite sources and mark missing figures.",
      "Use a fresh reporting packet each week. Ask for changes, possible explanations and decisions in separate sections.",
      "Have the meeting owner reconcile metrics and remove unsupported causal claims before circulation."],
     "A dashboard shows 18 open jobs last week and 24 this week. If the export date changed from Friday to Thursday, flag the comparison as provisional. Ask the source owner for matching snapshots before calling it a backlog increase.",
     "Draft a one-page owner brief from this packet. For each metric, show the value, comparison period and source. Separate observations from proposed explanations. List missing inputs and the decisions the meeting needs to make.",
     CHATGPT),
    ("claude-for-business-owners", "Claude for Business Owners",
     "Use Claude to turn approved business documents into evidence tables your team can review.",
     "A good first Claude workflow is a document review whose output can be checked against page or section references. Give it a question such as which support policy governs a service exception, along with only the documents approved for that review.",
     ["Select the current source documents and list their owners, effective dates and intended audience.",
      "If you use Claude Projects, put the reusable references in project knowledge and add instructions to flag conflicts and cite sections.",
      "Ask for a table with question, proposed answer, source and unresolved issue.",
      "Test one clear question, one ambiguous question and one question the documents cannot answer before sharing results with staff."],
     "A current policy allows a service credit with manager approval while an older FAQ promises a credit automatically. Surface both references and ask the policy owner to confirm which document staff should use.",
     "Use the approved policy packet to answer the listed staff questions. For each answer, identify the document and section. Flag conflicting or missing guidance and draft one clarification question for the policy owner.",
     CLAUDE),
    ("chatgpt-vs-claude-for-small-business", "ChatGPT vs. Claude for Small Business",
     "Compare ChatGPT and Claude on the same work before choosing one for your team.",
     "Test both tools on a recurring business task with a defined output. A vendor renewal brief is a useful trial because it combines structured facts, document references and judgment a reviewer can check.",
     ["Prepare one approved source packet and a reference answer with the fields the owner needs.",
      "Use the same task and constraints with both tools. Record which product surface and workspace settings you used.",
      "Count missing facts, unsupported statements and reviewer minutes for each output.",
      "Apply your requirements for data access and sharing before comparing the full cost per accepted brief."],
     "One draft takes six minutes to review but misses a renewal deadline. The other takes eight minutes and finds the date with a source. Treat the missed deadline as a failed requirement and rerun with a second document packet.",
     "Draft a renewal decision brief listing term, notice deadline, usage and outstanding questions. Cite the source for each. Where the packet is incomplete, state what someone needs to verify.",
     CHATGPT),
    ("codex-vs-claude-code-for-business", "Codex vs. Claude Code for Small Business Software",
     "Compare coding agents on the same repository task and measure what your team can maintain.",
     "Pick a change with visible acceptance criteria, such as adding a downloadable report to a small internal application. Use separate branches based on the same commit so each tool starts with the same code and tests.",
     ["Write requirements for column order, empty reports and which data is allowed in the export.",
      "Use the same brief, test fixture and repository instructions for each run.",
      "Review test results, unexpected file changes, setup effort and reviewer time.",
      "Have the future maintainer explain how to run the new tests and undo the change before choosing a default workflow."],
     "One branch includes hidden customer notes in the report. A passing test for column order cannot compensate for that. Add a test proving the allowed fields are the only ones exported, then rerun the trial.",
     "Add a local CSV export using the approved column list. Cover empty data, commas inside values and excluded fields with tests. Explain the changed files and how a maintainer can verify the result.",
     CODEX),
    ("chatgpt-projects-weekly-owner-review", "Build a Weekly Owner Review in ChatGPT Projects",
     "Create a repeatable workspace for preparing and reviewing the weekly business meeting.",
     "Keep stable business definitions and the changing weekly evidence distinct. Your project can hold the scorecard dictionary and meeting format. Give each weekly run a dated source packet so the reviewer can identify what was actually considered.",
     ["Add the scorecard dictionary and agenda format as reusable reference material.",
      "Supply the current and comparison period exports together.",
      "Ask for a brief organized by changed metrics, decisions, and unresolved questions.",
      "After the meeting, record approved decisions in your normal system and update project sources only when definitions change."],
     "The export calls estimates sent ‘proposals’ while the scorecard counts only signed quotes. Keep the two quantities separate and assign someone to fix the label before using the metric in a decision.",
     "Prepare this week's owner review. Use the dated packet for values and the scorecard dictionary for definitions. Identify definitions that do not match the export. Give every proposed action an owner or mark the owner undecided.",
     CHATGPT),
    ("claude-projects-company-knowledge", "Set Up Claude Projects for Company Knowledge",
     "Build a small, testable source collection for answering internal process questions.",
     "Pilot with one team and a narrow set of approved documents. A service team can start with dispatch, escalation and customer updates. Give those documents visible dates and owners so that weak answers can be traced to a source.",
     ["List the documents approved for the project and verify who can access them.",
      "Add the approved documents to project knowledge and set instructions for quoting section names and flagging missing answers.",
      "Prepare ten real questions with expected answers and two questions the packet cannot answer.",
      "When a policy changes, replace the outdated source and rerun the affected questions."],
     "A dispatcher asks whether a missed visit requires a phone call. The project has a rescheduling procedure but no rule about contact method. The expected output is to flag that missing rule and route it to the service lead.",
     "Answer using only the approved procedures. Cite the relevant section and effective date. If the packet does not establish an answer, write ‘policy owner review needed’ and summarize what is missing.",
     CLAUDE),
    ("codex-build-internal-tools", "Build Your First Internal Business Tool With Codex",
     "Turn a manual spreadsheet step into a tested internal tool your team can run.",
     "A first project can be a job CSV checker that catches blank IDs, invalid dates and repeated rows before a file reaches the reporting workbook. The checker produces a report and leaves the input file untouched.",
     ["Write a sample CSV and an expected exception report. Use fictional rows for development.",
      "Ask Codex to build the smallest local command that reads the file and produces that report.",
      "Ask for tests showing that valid rows pass and that malformed rows are surfaced with useful messages.",
      "Have a second person run it from the documented instructions. Use the existing workbook during the pilot and retain the prior process as a fallback."],
     "A file has a valid header and no records. Set the expected behavior before building. An explicit ‘no records received’ result gives an operator a reason to check the export before assuming there are no jobs.",
     "Build a local job-export checker from the fictional sample and expected exception report. Preserve the input file. Include tests for an empty export, duplicate IDs and malformed dates, and write the exact command an operator should run.",
     CODEX),
]


PRACTICE = {
    "chatgpt-vs-claude-for-small-business": """<h2>Run a side-by-side renewal test</h2>
<p>Copy the same fictional packet and prompt into separate fresh conversations. Give each tool the same inputs and access to sources. Have a colleague label the outputs A and B before the reviewer reads them.</p>
<pre>Signed agreement §4: Renews July 1, 2027 unless written notice is received by May 31, 2027.
Signed agreement §7: Renewal price is $600 per month for 30 seats.
Usage export, April 30: 18 of 30 seats used in the prior 30 days.
Vendor email, May 4: We can discuss a smaller seat package.
No signed amendment is included.</pre>
<p><strong>Expected answer:</strong> Notice is due May 31, 2027. The existing renewal price is $600 per month. Twelve seats had no recorded use. The email identifies a negotiation option, and the price or terms of a smaller package remain unconfirmed.</p>
<table><thead><tr><th scope="col">Check</th><th scope="col">What earns a pass</th></tr></thead><tbody>
<tr><td>Deadline</td><td>May 31, 2027 is identified as the notice deadline and cited to §4.</td></tr>
<tr><td>Price and usage</td><td>The draft cites §7 and the April export for $600 per month and 18 of 30 seats used.</td></tr>
<tr><td>Uncertainty</td><td>The draft treats a smaller package as an option and asks for written terms.</td></tr>
<tr><td>Review effort</td><td>Record minutes from opening the draft to approval, including corrections.</td></tr>
</tbody></table>
<h2>Test what happens when the evidence is incomplete</h2>
<p>Run a second round with the May 31 date removed from the packet. A usable draft should tell the contract owner to verify the notice deadline before deciding. Score each round separately. If both tools pass the required facts and uncertainty checks, compare review time and workspace cost per approved brief. If neither passes, revise the instructions and test again before using either in the renewal process.</p>""",
    "codex-for-business-owners": """<h2>Choose your first Codex project</h2>
<table><thead><tr><th scope="col">Candidate</th><th scope="col">First release</th><th scope="col">Evidence to review</th></tr></thead><tbody>
<tr><td>Operations reporting</td><td>Read a copy of a daily export and show late orders.</td><td>Reconcile the report against the existing spreadsheet and explain every unmatched order.</td></tr>
<tr><td>Internal request form</td><td>Build a preview with sample requests and validate required fields.</td><td>Show that a missing field is caught and that a failed submission displays a clear error.</td></tr>
<tr><td>Customer account updates</td><td>Produce a proposed change list for an operator to review.</td><td>Verify that each proposed change has source evidence and that the preview leaves accounts untouched.</td></tr>
</tbody></table>
<h2>Write a brief your team can accept</h2>
<p>Copy these fields into your first task. Agree on the expected result with the person who will own the work.</p>
<pre>Operator and owner:
Current manual process:
Approved input and example:
Output and destination:
Changes outside this task:
Routine and exception tests:
Release approver:
Fallback and support contact:</pre>
<p>For a fictional late-order report, agree that a row with a promised ship date before the report date and an empty actual ship date counts as late. A blank promised date belongs in the exceptions table. If the export contains two rows for the same order, flag both for review before counting the order. Ask the operations manager to predict the expected result before running the tool.</p>
<p>Before release, have a second operator run the report using its written instructions and reconcile one day’s output to the manual report. Keep the old report available during the trial. Use the <a href="/ai/business-owners/codex-build-internal-tools/">internal tool walkthrough and CSV fixture</a> to test a concrete implementation.</p>""",
    "chatgpt-for-business-owners": """<h2>Choose your first ChatGPT pilot</h2>
<p>Start where the team already has clear source material and someone who can approve the output. Choose a single workflow for the first two weeks.</p>
<table><thead><tr><th scope="col">Workflow</th><th scope="col">Inputs and reviewer</th><th scope="col">What the reviewer must verify</th></tr></thead><tbody>
<tr><td>Sales call follow-up</td><td>Approved call notes and a sample email. The salesperson reviews.</td><td>The draft matches the buyer’s request, next step, and agreed date. It introduces no new commitments.</td></tr>
<tr><td>Customer support draft</td><td>A redacted ticket and current service policy. The service lead reviews.</td><td>The draft uses the correct policy and routes refund or warranty exceptions to the person authorized to decide.</td></tr>
<tr><td>Weekly owner brief</td><td>Two dated metric exports and a scorecard dictionary. The meeting owner reviews.</td><td>Every figure reconciles, comparison periods match, and proposed explanations are labeled as hypotheses.</td></tr>
</tbody></table>
<h2>Measure time per approved output</h2>
<p>Use the same ten cases for your baseline and AI pilot. Include routine cases, one missing-input case, and one case that should be escalated. Record drafting, reviewing, and correction time. Count a draft as approved only after the assigned reviewer accepts it.</p>
<p>In a fictional sales pilot, ten manual follow-ups took 120 minutes. ChatGPT drafting and review took 65 minutes, but two drafts needed manual rewrites that added 24 minutes. That leaves 31 minutes saved across ten approved emails, or 3.1 minutes per email. If either draft introduced a false customer commitment, adjust the instructions and retest that failure before rollout.</p>
<p>Choose a threshold before the trial. For example, require all critical facts to pass and at least two minutes saved per approved draft. Record which cases failed and who will own the next revision.</p>
<p>For a recurring reporting workflow, use the <a href="/ai/business-owners/chatgpt-projects-weekly-owner-review/">weekly owner review template</a>. For task-specific drafts, see the <a href="/ai/chatgpt-business-workflows/">ChatGPT business workflow collection</a>.</p>""",
    "codex-build-internal-tools": """<h2>Test the checker with a fictional export</h2>
<p>Save this fixture as <code>jobs.csv</code>. The checker should report each exception with the row number and reason. Row numbers below count the header as row 1.</p>
<pre>job_id,due_date,status
J-101,2026-12-01,open
J-102,2026-12-02,complete
J-101,2026-12-03,open
J-103,2026-02-30,open
,2026-12-04,open</pre>
<table><thead><tr><th scope="col">Row</th><th scope="col">Expected result</th></tr></thead><tbody>
<tr><td>2–3</td><td>Accepted</td></tr><tr><td>4</td><td>Duplicate J-101</td></tr>
<tr><td>5</td><td>Invalid calendar date</td></tr><tr><td>6</td><td>Missing job ID</td></tr>
</tbody></table>
<p>Run a second fixture with just the header. Expect zero accepted rows and an explicit empty-export message. Check that both runs leave the source files unchanged.</p>""",
    "chatgpt-projects-weekly-owner-review": """<h2>Copy the weekly review template</h2>
<p>Fill in the inputs before asking for a draft. The reviewer can use the final column to record whether each figure reconciles.</p>
<pre>Week ending:
Meeting owner:
Current and comparison export dates:

Metric | Definition | Current | Prior | Source | Reviewer check
Open jobs | Jobs with no completion timestamp | 24 | 18 | Dispatch export | Check snapshot dates

Decision needed | Options | Owner | Due date
Investigate backlog change | Compare Friday snapshots | Dispatch lead | Next review

Missing evidence:
Approved actions:</pre>
<p>In this fictional example, the current export was taken on Thursday and the comparison on Friday. The accepted brief should ask for matching snapshots before treating the six-job difference as a trend.</p>""",
    "claude-projects-company-knowledge": """<h2>Run a three-question document review</h2>
<p>Use this fictional test packet. Give the reviewer the source text and expected answers before running the trial.</p>
<ol><li><strong>Dispatch Procedure §2, effective November 10.</strong> Dispatchers notify the scheduling lead within 15 minutes of a missed visit.</li>
<li><strong>Customer Updates §4, effective November 12.</strong> The service lead approves the revised arrival window before it is sent to the customer.</li></ol>
<table><thead><tr><th scope="col">Question</th><th scope="col">Expected answer and evidence</th></tr></thead><tbody>
<tr><td>Who needs to know immediately?</td><td>The scheduling lead within 15 minutes, Dispatch Procedure §2.</td></tr>
<tr><td>Who approves a revised arrival window?</td><td>The service lead, Customer Updates §4.</td></tr>
<tr><td>Must the customer be called?</td><td>The packet does not specify a contact method. Ask the policy owner.</td></tr>
</tbody></table>
<p>Mark the trial as failed if a response guesses a rule or cites a section that does not support the answer.</p>""",
}


def render_pages(header, breadcrumbs, footer):
    def wrap(path, title, description, body, kind):
        trail = [("Home", "/"), ("AI for Business Owners", ROOT)]
        trail = trail[:-1] + [("AI for Business Owners", None)] if path == ROOT else trail + [(title, None)]
        return (header(title, description, path, page_type=kind)
                + breadcrumbs(trail)
                + f'<section class="sec"><div class="ctn owner-guide"><h1>{escape(title)}</h1>{body}</div></section>'
                + footer())

    def link(guide):
        return f'<a href="{ROOT}{guide[0]}/">{escape(guide[1])}</a>'

    title = "Codex, ChatGPT, and Claude for Business Owners"
    description = "Practical guides for using OpenAI Codex, ChatGPT, and Claude to run a small business, with worked examples and prompts."
    cards = "".join(f'<article class="pill"><h3>{link(guide)}</h3><p>{escape(guide[2])}</p></article>' for guide in GUIDES)
    intro = """<p>Use ChatGPT or Claude when the deliverable is a draft, decision brief, or review of approved documents. Start with Codex or Claude Code when the deliverable is a change to software someone on your team can test and maintain.</p>
    <p>Choose one recurring job and record how long it takes today. Give the tool the same inputs and check how long it takes a person to approve the result. An output that saves writing time but adds review time may need a narrower brief.</p>"""
    more = """<h2>More business workflows</h2><ul>
    <li><a href="/ai/chatgpt-business-workflows/">ChatGPT workflows for operations and sales</a></li>
    <li><a href="/ai/claude-business-documents/">Claude workflows for business documents</a></li>
    <li><a href="/ai/implementation/">AI implementation library</a></li></ul>"""
    pages = {ROOT: wrap(ROOT, title, description, intro + f'<div class="pills">{cards}</div>' + more, "CollectionPage")}
    for index, guide in enumerate(GUIDES):
        slug, name, summary, intro, steps, example, prompt, source = guide
        path = f"{ROOT}{slug}/"
        items = "".join(f"<li>{escape(step)}</li>" for step in steps)
        related = "".join(f"<li>{link(GUIDES[(index + offset) % len(GUIDES)])}</li>" for offset in (1, 2))
        sources = [source]
        if slug == "codex-vs-claude-code-for-business":
            sources.append(("Claude Code documentation", "https://code.claude.com/docs/en/overview"))
        if slug == "chatgpt-vs-claude-for-small-business":
            sources.append(CLAUDE)
        references = "".join(f'<li><a href="{escape(url, quote=True)}">{escape(label)}</a></li>' for label, url in sources)
        body = f"""<p>{escape(summary)}</p><p>{escape(intro)}</p>
        <h2>How to run the workflow</h2><ol>{items}</ol>
        <h2>Worked example</h2><p>{escape(example)}</p>
        <h2>Prompt to adapt</h2><blockquote>{escape(prompt)}</blockquote>
        {PRACTICE.get(slug, "")}<h2>Product documentation</h2><ul>{references}</ul>
        <h2>Related business guides</h2><ul>{related}<li><a href="{ROOT}">All Codex, ChatGPT, and Claude guides</a></li></ul>"""
        pages[path] = wrap(path, name, summary, body, "WebPage")
    return pages
