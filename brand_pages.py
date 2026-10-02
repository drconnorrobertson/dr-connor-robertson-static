"""Evidence-linked author, project and podcast pages for the personal site."""
import html
import json

UPDATED = '2026-10-02'
STYLE = '''<style>
.profile-copy{max-width:880px;margin:auto}.profile-copy h2{font-size:clamp(24px,4vw,34px);line-height:1.2;margin:44px 0 18px}.profile-copy h3{font-size:21px;margin:24px 0 12px}.profile-copy p,.profile-copy li{font-size:17px;line-height:1.8;color:var(--text2)}.profile-copy p{margin:0 0 18px}.profile-copy a:not(.btn-p):not(.btn-s){color:var(--text);text-decoration:underline;text-underline-offset:4px}.profile-copy ul,.profile-copy ol{padding-left:24px;margin:16px 0 24px}.profile-copy li{margin-bottom:12px}.profile-links{display:flex;flex-wrap:wrap;gap:12px;margin:24px 0}.profile-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:24px}.profile-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:26px}.profile-card h2,.profile-card h3{margin:0 0 14px;font-size:23px}.profile-card p{font-size:16px}.profile-meta{font-size:14px!important;color:var(--muted)!important}.profile-copy audio{width:100%;margin:18px 0}.profile-nav{display:flex;flex-wrap:wrap;gap:18px;list-style:none!important;padding:0!important}.profile-copy .portrait{display:block;width:220px;max-width:100%;border-radius:14px;margin:0 auto 28px}.profile-copy details{border-top:1px solid var(--border);padding:20px 0}.profile-copy summary{cursor:pointer;font-size:18px;font-weight:600}.profile-copy details p{margin-top:14px}
</style>'''

def e(value):
    return html.escape(str(value), quote=True)

def link(url,label):
    attrs = ' target="_blank" rel="noopener"' if url.startswith('https://') else ''
    return f'<a href="{e(url)}"{attrs}>{e(label)}</a>'

def paragraph(text):
    return f'<p>{text}</p>'

def section(title,body):
    return f'<section><h2>{e(title)}</h2>{body}</section>'

def faq(items):
    return section('Questions and answers',''.join(f'<details><summary>{e(q)}</summary><p>{a}</p></details>' for q,a in items))

BOOK_GUIDES = {
 'buying-wealth': {
  'short':'Buying Wealth','audience':'Entrepreneurs and professionals exploring ownership of businesses and income-producing assets.',
  'intro':'Buying Wealth introduces an ownership-centered approach to building wealth. Its central subject is the move from earning income through personal work toward owning assets that can produce cash flow. For a reader comparing entrepreneurship, business acquisition, and real estate, it provides a place to begin that conversation.',
  'context':'An asset purchase creates a new set of responsibilities. A buyer needs to understand how income is produced, which costs are unavoidable, and what remains after financing and ongoing maintenance. A large purchase price or attractive revenue figure alone does not answer those questions. Use the book alongside a written description of the asset you want to own and the resources you can commit to operating it.',
  'questions':['What asset am I considering, and what evidence supports its cash flow?','How much liquidity would remain after the purchase?','Who would manage the asset, and what happens if income falls?'],
  'next':[('/business-acquisitions/','Business acquisition guide'),('/books/creative-acquisitions/','Creative Acquisitions')],
 },
 'the-7-minute-phone-call': {
  'short':'The 7 Minute Phone Call','audience':'Founders, sales professionals, and business owners who want more purposeful prospecting conversations.',
  'intro':'The 7 Minute Phone Call focuses on human connection in prospecting. It addresses a familiar problem: it is easy to send another message while postponing the conversation that would clarify whether two people should work together. The book offers a practical entry point for readers who want to improve how they begin those conversations.',
  'context':'A useful call has a clear reason for happening and respects the other person\'s time. Before calling, identify why the conversation could matter to that person, what you need to learn, and what a sensible next step would be. Afterward, record the actual outcome. A requested introduction, a qualified follow-up, and a polite decline require different actions. Treat the book as a starting point for deliberate practice, then refine your approach through real conversations.',
  'questions':['Why is this conversation relevant to the person I am calling?','Which question would help me understand their situation?','What next step did we actually agree to?'],
  'next':[('/prospecting-sales/','Prospecting and sales guide'),('/podcast/','The Prospecting Show')],
 },
 'creative-acquisitions': {
  'short':'Creative Acquisitions','audience':'Aspiring business buyers, entrepreneurs, and operators evaluating flexible acquisition structures.',
  'intro':'Creative Acquisitions: The Playbook for Modern Dealmakers is an operator-focused book about buying existing businesses. The retailer description presents it as a guide to flexible and durable acquisition strategies. This page brings its official listings together with a practical reading guide for people evaluating their first or next purchase.',
  'context':'A deal structure should reflect the business being purchased and the obligations both sides can realistically meet. Before comparing structures, establish what the company earns, how much working capital it needs, and which responsibilities depend on the seller. A flexible structure does not remove those operating questions. Pair your reading with the acquisition resources below to organize diligence, seller conversations, and transition planning.',
  'questions':['What does the buyer need to verify before proposing terms?','Which risks should be addressed in the transition plan?','Can the company support the proposed obligations under a weaker operating scenario?'],
  'next':[('/business-acquisitions/','Business acquisition guide'),('/business-acquisitions/business-acquisition-due-diligence-checklist/','Due diligence checklist')],
 },
 'built-to-run': {
  'short':'Built to Run','audience':'Owner-operators and founders who want to reduce the business\'s dependence on their daily involvement.',
  'intro':'Built to Run concerns the systems and processes that allow a business to operate with less constant owner involvement. It is intended for readers who see a gap between owning a company and being required for every decision inside it. The book belongs alongside Connor\'s writing on leadership, operating systems, and the transition from operator to strategist.',
  'context':'Start by identifying a recurring activity that stops when the owner is unavailable. Write down its inputs, the person responsible, the standard for completion, and the decisions that need escalation. Delegating a task without those details can transfer work while leaving the owner responsible for resolving every exception. A practical reading exercise is to choose one workflow and document what another person needs to complete it reliably.',
  'questions':['Which recurring decisions still depend entirely on the owner?','What information would a team member need to make those decisions?','How will the business detect a problem before it becomes urgent?'],
  'next':[('/ai-business-strategy/','Practical AI business strategy'),('/blog/operational-drag-in-business/','Operational drag diagnostic')],
 },
 'padsplit-playbook': {
  'short':'PadSplit Playbook','audience':'Property owners and housing operators evaluating shared living and room-rental operations.',
  'intro':'PadSplit Playbook: Scaling Affordable Housing Through Shared Living addresses the operating model behind shared housing. The Google Play listing describes a guide to professionally managed room rentals and the use of underutilized single-family homes. This is a distinct subject from buying a conventional rental and leaving its management approach unchanged.',
  'context':'Shared housing requires attention to both the property and the experience of the people living there. Layout, local requirements, maintenance, common spaces, and clear operating responsibilities all affect whether a property can work as intended. Use the book to frame the questions you need to investigate for a specific property. A platform listing or optimistic room count does not establish that a proposed conversion is appropriate for that location.',
  'questions':['Which local occupancy and property requirements apply to this address?','How will common areas, repairs, and resident communication be managed?','What costs and vacancy assumptions belong in the operating budget?'],
  'next':[('/books/buying-wealth/','Buying Wealth'),('/projects/','Connor\'s projects and publishing work')],
 },
 'buy-the-building-keep-the-profits': {
  'short':'Buy the Building, Keep the Profits','audience':'Business owners comparing their existing lease with ownership of the property their company occupies.',
  'intro':'Buy the Building, Keep the Profits examines property ownership from the perspective of an operating business. The question is broader than whether rent feels expensive. It is whether owning the real estate that supports the company fits its capital needs, location plans, and ability to manage a second asset.',
  'context':'Compare the operating business and the property as two related decisions. The company needs suitable space and enough capital to keep operating. The property requires its own budget for financing, repairs, reserves, and potential changes in use. A purchase that benefits one side can still constrain the other. Before acting, write down the company\'s expected space needs, the costs of remaining a tenant, and the obligations that ownership would introduce.',
  'questions':['How long is this location likely to suit the company?','Which ownership costs would replace or supplement the existing rent?','Would the purchase leave enough capital for the operating business?'],
  'next':[('/books/buying-wealth/','Buying Wealth'),('/business-acquisitions/','Business acquisition resources')],
 },
}

PROJECTS = [
 {'slug':'elixir-consulting-group','name':'Elixir Consulting Group','role':'Founder','url':'https://www.elixirconsultinggroup.com',
 'intro':'Elixir Consulting Group is Connor\'s business advisory venture, with published work on practical AI implementation, business automation, and operating systems for small and mid-sized businesses.',
 'body':'The work begins with understanding a business process. A team needs to know where information enters, which decisions require judgment, and what a usable result looks like before introducing automation. Connor\'s writing connects that operational discipline with the broader responsibilities of a business owner: finding customers, fulfilling commitments, and making room for growth.',
 'focus':['Documenting recurring work and assigning clear owners.','Evaluating where AI can assist with drafts, research, and internal workflows.','Connecting technology decisions to operating needs and review responsibilities.'],
 'sources':[('https://www.elixirconsultinggroup.com/blog/ai-implementation-small-business-step-by-step-guide/','AI implementation guide on Elixir\'s website')],
 'related':[('/ai-business-strategy/','AI business strategy'),('/business-acquisitions/','Business acquisitions')]},
 {'slug':'the-pittsburgh-wire','name':'The Pittsburgh Wire','role':'Founder and publisher','url':'https://www.thepittsburghwire.com',
 'intro':'The Pittsburgh Wire is a digital publication focused on Pittsburgh business, real estate, economic development, and the people shaping the city. Connor\'s founder profile on the publication identifies his role in establishing it.',
 'body':'A local publication gives business owners and residents a way to follow the changes happening around them. Its subjects include businesses, neighborhoods, development, and the people behind those projects. For readers exploring Connor\'s work, The Pittsburgh Wire represents the publishing side of his interests in entrepreneurship and the Pittsburgh community.',
 'focus':['Local business and entrepreneurship.','Real estate, development, and neighborhood activity.','Profiles and stories about the people building Pittsburgh.'],
 'sources':[('https://www.thepittsburghwire.com/authors/connor-robertson/','Connor\'s founder and publisher profile')],
 'related':[('/press-media/','Press and media directory'),('/about/','Connor\'s biography')]},
 {'slug':'the-prospecting-show','name':'The Prospecting Show','role':'Host','url':'https://www.prospectingshow.com',
 'intro':'The Prospecting Show is Connor\'s interview podcast about business owners and the companies they have built. Its published archive includes conversations about sales, entrepreneurship, software, real estate, and business operations.',
 'body':'The interviews create a record of how guests describe their work in their own words. An episode is useful when a listener can connect the guest\'s experience to a decision in their own business. The podcast pages on this site link to the original recording and identify the original publication date, so readers can distinguish an archived conversation from a current announcement.',
 'focus':['Founder interviews and accounts of business growth.','Sales, prospecting, and customer acquisition.','Operating lessons across different industries.'],
 'sources':[('https://podcasts.apple.com/us/podcast/the-prospecting-show-with-dr-connor-robertson/id1488353384','The published Apple Podcasts archive')],
 'related':[('/podcast/','Listen to verified episodes'),('/books/the-7-minute-phone-call/','The 7 Minute Phone Call')]},
]

def render_pages(b):
    pages = {}
    site, person = b['SITE_URL'], b['PERSON_ID']
    books = b['BOOKS']
    episodes = json.loads((b['BASE_DIR']/'podcast_episodes.json').read_text())
    def page(path,title,desc,h1,subtitle,body,kind='WebPage',nodes=None,image='/images/connor-hero.jpg',parents=None):
        trail = [('Home','/')] + (parents or []) + [(h1,None)]
        result = b['header'](title,desc,path,extra=STYLE,og_image=image,page_type=kind,
            crumbs=trail,schema_nodes=nodes or [],page_extra={'dateModified':UPDATED, **({'mainEntity':{'@id':person}} if kind == 'ProfilePage' else {})})
        result += b['breadcrumbs'](trail)
        result += f'<section class="pg-hero"><div class="ctn"><h1>{e(h1)}</h1><p>{e(subtitle)}</p></div></section><section class="sec"><div class="ctn profile-copy">{body}</div></section>'
        result += b['footer']()
        pages[path] = result
    def resources(items):
        return '<ul>'+''.join('<li>'+link(u,l)+'</li>' for u,l in items)+'</ul>'
    def contact(label='Discuss a project'):
        return f'<div class="profile-links"><a class="btn-p" href="/contact/">{e(label)}</a><a class="btn-s" href="/about/">About Connor</a></div>'

    bio = '<img class="portrait" src="/images/connor-about.jpg" alt="Dr. Connor Robertson, Pittsburgh entrepreneur and author" width="220" height="220">'
    bio += paragraph('Dr. Connor Robertson is a Canadian-born entrepreneur, author, podcast host, and business strategist based in Pittsburgh, Pennsylvania. His work spans business acquisitions, real estate, publishing, and practical business automation. This is his official personal website, with links to his books, interviews, and ventures.')
    bio += '<ul class="profile-nav"><li><a href="#background">Background</a></li><li><a href="#work">Current work</a></li><li><a href="#books">Books</a></li><li><a href="#interviews">Interviews</a></li></ul>'
    bio += '<section id="background"><h2>From healthcare to business ownership</h2>'+paragraph('Connor began his professional career in chiropractic care after studying at the University of Western Ontario and New York Chiropractic College. His later work moved into business ownership, acquisitions, and consulting. The transition connected an interest in helping people with the practical responsibilities of building and operating a company.')
    bio += paragraph('His career has developed through several stages: professional education and healthcare, business operations and acquisitions, and then a broader mix of advisory, real estate, and publishing work. The common thread is an interest in how a business attracts customers, delivers its work, and becomes less dependent on one person.')+'</section>'
    bio += '<section id="work"><h2>Business, real estate, and publishing</h2>'+paragraph('Through '+link('/projects/elixir-consulting-group/','Elixir Consulting Group')+', Connor works on business strategy and practical automation. He also publishes '+link('/projects/the-pittsburgh-wire/','The Pittsburgh Wire')+', a publication about Pittsburgh business and development, and hosts '+link('/podcast/','The Prospecting Show')+'. Each venture has its own purpose and public website.')
    bio += paragraph('His real estate interests appear throughout his books, including shared housing and the relationship between an operating company and the property it occupies. His acquisition writing addresses buying an existing business and preparing to operate it after the purchase.')+'</section>'
    bio += '<section id="books"><h2>Books by Dr. Connor Robertson</h2>'+paragraph('Connor\'s six listed books address ownership, acquisitions, prospecting, shared housing, commercial property, and operating systems. Each book has its own page with an overview, reading questions, and links to its official website or retailer listings.')+resources([(f'/books/{x["slug"]}/',x['title']) for x in books])+'</section>'
    bio += '<section id="interviews"><h2>The Prospecting Show and public profiles</h2>'+paragraph('The Prospecting Show features conversations with business owners about their experience building and growing companies. The published feed contained 179 entries when checked on October 2, 2026. The '+link('/podcast/','podcast directory')+' includes selected original recordings with their publication dates.')+resources([('https://www.linkedin.com/in/dr-connor-robertson','LinkedIn profile'),('/press-media/','Press and media coverage'),('/media/','Media kit and photographs')])+'</section>'
    bio += faq([('What does the title Dr. refer to?','It refers to Connor\'s chiropractic education. His work presented on this website concerns business, publishing, and entrepreneurship.'),('Where is Connor Robertson based?','Connor is based in Pittsburgh, Pennsylvania.'),('How can I contact Connor?','Use the '+link('/contact/','contact page')+' for business inquiries, speaking requests, or media questions.')])+contact('Contact Connor')
    page('/about/','Dr. Connor Robertson | Biography, Books & Career','Official biography of Dr. Connor Robertson: healthcare background, business ventures, six books, podcast interviews, and Pittsburgh publishing work.','About Dr. Connor Robertson','Entrepreneur, author, podcast host, and business strategist.',bio,'ProfilePage',image='/images/connor-about.jpg',nodes=[])

    book_cards=[]; book_nodes=[]
    for book in books:
        slug=book['slug']; guide=BOOK_GUIDES[slug]; path=f'/books/{slug}/'
        body=paragraph(e(guide['intro']))+paragraph('<strong>Author:</strong> '+link('/about/','Dr. Connor Robertson'))
        body+=section('Who this book is for',paragraph(e(guide['audience'])))
        body+=section('A practical reading guide',paragraph(e(guide['context']))+paragraph('Use these questions to connect the topic to your own situation. They are companion reading prompts, rather than quotations from the book.')+'<ul>'+''.join(f'<li>{e(q)}</li>' for q in guide['questions'])+'</ul>')
        body+=section('Read the book and explore available previews',paragraph('Visit the official listing below to check the current edition, available formats, and any sample offered by the seller.'))
        body+=resources(book['retailers'])
        body+=section('About the author',paragraph('Dr. Connor Robertson is a Pittsburgh-based entrepreneur, author, and host of The Prospecting Show. His writing connects business ownership with the operating responsibilities that follow it. Explore his '+link('/about/','biography')+' and '+link('/books/','other books')+' for related work.'))
        body+=section('Continue exploring',resources(guide['next']))+contact('Ask about this book')
        node={'@type':'Book','@id':site+path+'#book','name':book['title'],'author':{'@id':person},'url':site+path,'description':book['desc'],'inLanguage':'en','sameAs':[u for label,u in book['retailers']]}
        page(path,guide['short']+' | Dr. Connor Robertson',book['desc'],book['title'],'A book by Dr. Connor Robertson.',body,nodes=[node],image='/images/connor-book.jpg',parents=[('Books','/books/')])
        book_nodes.append({'@type':'ListItem','position':len(book_nodes)+1,'item':node})
        book_cards.append(f'<article class="profile-card" id="{e(slug)}"><h2>{link(path,book["title"])}</h2><p>{e(book["desc"])}</p><p>{link(path,"Overview and reading guide")}</p></article>')
    body=paragraph('Explore six books by Dr. Connor Robertson. Choose a title based on the decision you are working through: buying an asset, acquiring a company, improving sales conversations, organizing operations, or evaluating real estate ownership.')
    body+='<div class="profile-grid">'+''.join(book_cards)+'</div>'
    body+=section('Where to begin',paragraph('For a broad introduction to ownership, start with '+link('/books/buying-wealth/','Buying Wealth')+'. For a business purchase, explore '+link('/books/creative-acquisitions/','Creative Acquisitions')+'. If your company already exists and needs stronger operations, consider '+link('/books/built-to-run/','Built to Run')+'.'))+contact('Invite Connor to discuss his work')
    page('/books/','Books by Dr. Connor Robertson | Official Reading Guides','Explore six books by Dr. Connor Robertson, with individual reading guides and official listings on acquisitions, prospecting, operations, and real estate.','Books by Dr. Connor Robertson','Find the book that fits your next business decision.',body,'CollectionPage',[{'@type':'ItemList','@id':site+'/books/#booklist','itemListElement':book_nodes}],image='/images/connor-book.jpg')

    cards=[]
    for project in PROJECTS:
        path='/projects/'+project['slug']+'/'
        body=paragraph(e(project['intro']))+paragraph('<strong>Connor\'s role:</strong> '+e(project['role']))
        body+=section('What this project does',paragraph(e(project['body'])))
        body+=section('Areas of focus','<ul>'+''.join('<li>'+e(x)+'</li>' for x in project['focus'])+'</ul>')
        body+=section('Explore the original project',resources([(project['url'],project['name']+' official website')]+project['sources']))
        body+=section('Related work',resources(project['related']))+contact()
        page(path,project['name']+' | Dr. Connor Robertson',project['intro'],project['name'],'A project in Connor Robertson\'s business and publishing work.',body,parents=[('Projects','/projects/')])
        cards.append(f'<article class="profile-card"><h2>{link(path,project["name"])}</h2><p>{e(project["intro"])}</p><p>{link(path,"Explore the project")}</p></article>')
    body=paragraph('These project profiles explain Connor\'s role and link to the original venture. They cover advisory work, local publishing, and business interviews.')+'<div class="profile-grid">'+''.join(cards)+'</div>'
    body+=section('Books and real estate',paragraph('Connor\'s '+link('/books/','books')+' explore the acquisition and operation of businesses and property. His real estate titles include '+link('/books/padsplit-playbook/','PadSplit Playbook')+' and '+link('/books/buy-the-building-keep-the-profits/','Buy the Building, Keep the Profits')+'.'))+contact()
    page('/projects/','Dr. Connor Robertson | Companies & Projects','Explore Dr. Connor Robertson\'s work through Elixir Consulting Group, The Pittsburgh Wire, The Prospecting Show, and his books.','Projects and companies','Advisory work, publishing, and conversations with business owners.',body,'CollectionPage')

    episode_cards=[]
    series={'@type':'PodcastSeries','@id':site+'/podcast/#series','name':'The Prospecting Show with Dr. Connor Robertson','url':site+'/podcast/','creator':{'@id':person},'webFeed':episodes['source_feed'],'sameAs':['https://podcasts.apple.com/us/podcast/the-prospecting-show-with-dr-connor-robertson/id1488353384']}
    for episode in episodes['episodes']:
        path='/podcast/'+episode['slug']+'/'
        date=episode['date'][:10]
        body=f'<p class="profile-meta">Episode {episode["number"]} · Published {e(date)} · Hosted by Dr. Connor Robertson</p>'
        body+=section('Listen to the original recording',f'<audio controls preload="none" aria-label="Listen to episode {episode["number"]}"><source src="{e(episode["audio_url"])}" type="audio/mpeg">{link(episode["audio_url"],"Open the audio recording")}</audio>'+resources([(episode['source_url'],'Episode on Spotify for Podcasters')]))
        body+=section('Original episode notes',paragraph(e(episode['description'])))
        body+=paragraph('<span class="profile-meta">This is an archived episode. The description reflects the original publication, and guest roles and contact details may have changed since recording.</span>')
        body+=section('About the series',paragraph('The Prospecting Show is hosted by Dr. Connor Robertson and features business owners discussing their work and experience. Browse the '+link('/podcast/','episode directory')+' to explore other conversations.'))
        body+=section('More from Connor',resources([('/books/','Books by Dr. Connor Robertson'),('/about/','Biography and background'),('/prospecting-sales/','Prospecting and sales resources')]))
        node={'@type':'PodcastEpisode','@id':site+path+'#episode','name':episode['title'],'url':site+path,'episodeNumber':episode['number'],'datePublished':episode['date'],'description':episode['description'],'partOfSeries':{'@id':series['@id']},'associatedMedia':{'@type':'AudioObject','contentUrl':episode['audio_url']},'creator':{'@id':person},'sameAs':episode['source_url']}
        page(path,f'Episode {episode["number"]} | The Prospecting Show',episode['description'],episode['title'],'The Prospecting Show with Dr. Connor Robertson.',body,nodes=[series,node],parents=[('Podcast','/podcast/')])
        episode_cards.append(f'<article class="profile-card"><p class="profile-meta">Episode {episode["number"]} · {e(date)}</p><h2>{link(path,episode["title"])}</h2><p>{e(episode["description"][:160])}{"..." if len(episode["description"])>160 else ""}</p><p>{link(path,"Listen and read the episode notes")}</p></article>')
    body=paragraph('The Prospecting Show with Dr. Connor Robertson is an interview podcast about entrepreneurship, sales, and building businesses. Explore selected conversations from the published archive below. Each episode page includes the original audio, publication date, and episode notes.')
    body+=paragraph('The published feed contained 179 entries when verified on October 2, 2026. These are archive recordings, rather than a claim of newly released episodes.')
    body+='<div class="profile-links"><a class="btn-p" href="https://podcasts.apple.com/us/podcast/the-prospecting-show-with-dr-connor-robertson/id1488353384" target="_blank" rel="noopener">Full archive on Apple Podcasts</a><a class="btn-s" href="https://open.spotify.com/show/4VDPOlbe2RSSqukaSuYniX" target="_blank" rel="noopener">Listen on Spotify</a></div>'
    body+=section('Selected interviews','<div class="profile-grid">'+''.join(episode_cards)+'</div>')
    body+=section('For guests and listeners',paragraph('For an interview inquiry or a question about the show, use the '+link('/contact/','contact page')+'. Include your background, the subject you would like to discuss, and any relevant links. For more on the host, read '+link('/about/','Connor\'s biography')+'.'))
    page('/podcast/','Dr. Connor Robertson Podcast | The Prospecting Show','Listen to verified episodes of The Prospecting Show with Dr. Connor Robertson, including original audio, publication dates, and guest episode notes.','The Prospecting Show','Business interviews hosted by Dr. Connor Robertson.',body,'CollectionPage',[series])

    body=paragraph('Dr. Connor Robertson speaks on business ownership, acquisitions, prospecting, and practical business automation. His books and podcast archive give organizers a way to explore his subject matter before discussing an event.')
    body+=section('Speaking topics','<div class="profile-grid">'+''.join(f'<article class="profile-card"><h3>{e(t)}</h3><p>{e(d)}</p><p>{link(u,"Explore the related work")}</p></article>' for t,d,u in [
     ('Buying and operating an existing business','A discussion of acquisition preparation, diligence, and the responsibilities that begin after closing.','/books/creative-acquisitions/'),
     ('Prospecting through better conversations','Making outbound conversations more purposeful and building a clear follow-up process.','/books/the-7-minute-phone-call/'),
     ('Building a business that can run without its owner','Documenting recurring work, assigning responsibility, and reducing dependence on one person.','/books/built-to-run/'),
     ('Practical AI for business owners','Choosing a workflow, defining review responsibilities, and evaluating whether automation improves the process.','/ai-business-strategy/'),
     ('Business ownership and real estate','Exploring the relationship between an operating company and the property it occupies.','/books/buy-the-building-keep-the-profits/')])+'</div>')
    body+=section('Explore Connor\'s work before booking',resources([('/podcast/','Recorded podcast conversations'),('/books/','Books and reading guides'),('/press-media/','Press and media coverage'),('/media/','Photographs and media kit')]))
    body+=section('Tell us about your event',paragraph('Send the event date, location or virtual format, audience, expected attendance, requested topic, and session length. Include your budget and any recording or travel requirements so the request can be evaluated. Availability and arrangements are confirmed through the inquiry process.'))
    body+='<div id="book-me">'+contact('Send a speaking inquiry')+'</div>'
    page('/speaker/','Dr. Connor Robertson Speaker | Business & Acquisitions','Invite Dr. Connor Robertson to discuss business acquisitions, prospecting, operations, real estate ownership, and practical AI. Explore topics and send an inquiry.','Dr. Connor Robertson: speaking and workshops','Practical topics for business owners, founders, and operating teams.',body,image='/images/connor-blazer.jpg')
    return pages
