"""Editorial guides for owners choosing and rolling out AI tools."""
from html import escape

ROOT = "/ai/business-owners/"
CODEX = ("OpenAI Codex documentation", "https://openai.com/codex/")
CHATGPT = ("OpenAI guide to Projects in ChatGPT", "https://help.openai.com/en/articles/10169521-projects-in-chatgpt")
CLAUDE = ("Claude Help Center guide to Projects", "https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects")

GUIDES = [
    ("codex-for-business-owners", "OpenAI Codex for Business Owners",
     "Use Codex to build a small internal tool with a brief your team can test and maintain.",
     "Start with a decision someone makes by hand every week. An operations manager who combines two exports to identify late orders can start with one sanitized export, one report and one reviewer. Keep the existing spreadsheet available while the new report is tested.",
     ["Describe who runs the tool, which files it reads, and the output they need to make a decision.",
      "Give Codex a test fixture with five fictional orders, including a blank ship date and two rows with the same order ID.",
      "Ask for a local prototype and tests. Review the file changes with the person who will maintain the tool.",
      "Run the spreadsheet and prototype side by side. Move over only when the counts reconcile and the manager can handle errors without the original builder."],
     "The fixture has five rows but four distinct orders. Decide explicitly whether duplicates block the run or appear in a separate exceptions table. Make the reviewer confirm that rule before the prototype is used on real orders.",
     "Build a local prototype in this repository using the supplied fictional orders. Show late orders and list malformed or duplicate rows separately. Before editing, summarize the intended changes. Add tests for blanks and duplicates. Leave the existing workflow available.",
     CODEX),
    ("chatgpt-for-business-owners", "ChatGPT for Business Owners",
     "Set up a reusable ChatGPT workflow for the decisions and drafts your team prepares every week.",
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


def render_pages(header, breadcrumbs, footer):
    def wrap(path, title, description, body, kind):
        trail = [("Home", "/"), ("AI for Business Owners", ROOT)]
        trail = trail[:-1] + [("AI for Business Owners", None)] if path == ROOT else trail + [(title, None)]
        return (header(title, description, path, page_type=kind)
                + breadcrumbs(trail)
                + f'<section class="sec"><div class="ctn" style="max-width:900px"><h1>{escape(title)}</h1>{body}</div></section>'
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
        <h2>Product documentation</h2><ul>{references}</ul>
        <h2>Related business guides</h2><ul>{related}<li><a href="{ROOT}">All Codex, ChatGPT, and Claude guides</a></li></ul>"""
        pages[path] = wrap(path, name, summary, body, "WebPage")
    return pages
