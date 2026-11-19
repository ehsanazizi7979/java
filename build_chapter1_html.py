#!/usr/bin/env python3
"""Generate a self-contained HTML summary of Chapter 1 of 'Clean Code'
(from The Robert C. Martin Clean Code Collection), embedding all images
from the chapter as base64 data URIs."""
import base64
import os

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chapter1_assets")


def data_uri(filename):
    path = os.path.join(ASSETS, filename)
    with open(path, "rb") as f:
        raw = f.read()
    ext = os.path.splitext(filename)[1].lstrip(".").lower()
    mime = "jpeg" if ext == "jpg" else ext
    return f"data:image/{mime};base64," + base64.b64encode(raw).decode("ascii")


def data_uri_ch4(filename):
    path = os.path.join(os.path.dirname(ASSETS), "chapter2_assets", filename)
    with open(path, "rb") as f:
        raw = f.read()
    ext = os.path.splitext(filename)[1].lstrip(".").lower()
    mime = "jpeg" if ext == "jpg" else ext
    return f"data:image/{mime};base64," + base64.b64encode(raw).decode("ascii")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Clean Code Collection — Chapter Summaries (Ch. 1 &amp; Coding)</title>
<style>
  :root {
    --paper: #f4f1ea;
    --card: #ffffff;
    --ink: #2b2620;
    --muted: #6f675c;
    --accent: #b5541c;
    --accent-soft: #f7e8dd;
    --line: #e4ddd1;
    --code-bg: #1e1b16;
    --code-ink: #f3ede2;
  }
  * { box-sizing: border-box; }
  html { scroll-behavior: smooth; }
  body {
    margin: 0;
    background: var(--paper);
    color: var(--ink);
    font-family: Georgia, 'Times New Roman', serif;
    line-height: 1.65;
  }
  .wrap { max-width: 860px; margin: 0 auto; padding: 0 20px 80px; }

  /* ---------- hero ---------- */
  .hero {
    text-align: center;
    padding: 48px 20px 24px;
  }
  .hero .kicker {
    letter-spacing: .25em;
    text-transform: uppercase;
    font-size: 12px;
    color: var(--accent);
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-weight: 700;
  }
  .hero h1 {
    font-size: clamp(34px, 6vw, 56px);
    margin: 10px 0 6px;
    line-height: 1.1;
  }
  .hero .sub {
    color: var(--muted);
    font-style: italic;
    font-size: 17px;
  }
  /* ---------- part divider (book 2) ---------- */
  .part-divider {
    text-align: center;
    padding: 40px 20px 8px;
    margin-top: 30px;
    border-top: 3px double var(--line);
  }
  .part-divider .kicker {
    letter-spacing: .25em;
    text-transform: uppercase;
    font-size: 12px;
    color: var(--accent);
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-weight: 700;
  }
  .part-divider h2.part-title {
    font-size: clamp(28px, 5vw, 42px);
    margin: 8px 0 6px;
    border: none;
    padding: 0;
  }
  .part-divider .sub { color: var(--muted); font-style: italic; font-size: 16px; }
  .part-divider img.chapter-art {
    max-width: 420px;
    width: 100%;
    margin: 22px auto 0;
    display: block;
    border-radius: 8px;
    box-shadow: 0 10px 30px rgba(43, 38, 32, .18);
  }
  nav.toc .sep { color: var(--line); align-self: center; }
  .hero img.chapter-art {
    max-width: 340px;
    width: 100%;
    margin: 26px auto 0;
    display: block;
    border-radius: 8px;
    box-shadow: 0 10px 30px rgba(43, 38, 32, .18);
  }

  /* ---------- nav ---------- */
  nav.toc {
    position: sticky;
    top: 0;
    z-index: 50;
    background: rgba(244, 241, 234, .92);
    backdrop-filter: blur(6px);
    border-top: 1px solid var(--line);
    border-bottom: 1px solid var(--line);
    padding: 10px 0;
    margin-bottom: 34px;
  }
  nav.toc ol {
    display: flex;
    flex-wrap: wrap;
    gap: 4px 14px;
    justify-content: center;
    list-style: none;
    margin: 0;
    padding: 0;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 12.5px;
  }
  nav.toc a {
    color: var(--muted);
    text-decoration: none;
    padding: 3px 6px;
    border-radius: 4px;
  }
  nav.toc a:hover, nav.toc a.active { color: var(--accent); background: var(--accent-soft); }

  /* ---------- sections ---------- */
  section.card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 26px 30px;
    margin: 0 0 22px;
    box-shadow: 0 2px 8px rgba(43, 38, 32, .05);
  }
  h2 {
    font-size: 24px;
    margin: 0 0 12px;
    padding-bottom: 8px;
    border-bottom: 2px solid var(--accent-soft);
  }
  h2 .num {
    color: var(--accent);
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 13px;
    display: block;
    letter-spacing: .15em;
    text-transform: uppercase;
    margin-bottom: 4px;
  }
  h3 { font-size: 18px; margin: 18px 0 6px; }
  p { margin: 0 0 12px; }
  .lead { font-size: 18px; color: var(--ink); }
  .pull {
    border-left: 4px solid var(--accent);
    background: var(--accent-soft);
    padding: 12px 16px;
    font-style: italic;
    margin: 14px 0;
    border-radius: 0 8px 8px 0;
  }
  .figure { text-align: center; margin: 18px 0; }
  .figure img { max-width: 100%; border: 1px solid var(--line); border-radius: 8px; }
  .figure figcaption {
    font-size: 13px;
    color: var(--muted);
    margin-top: 8px;
    font-family: 'Helvetica Neue', Arial, sans-serif;
  }

  /* ---------- quote cards ---------- */
  .quote {
    display: flex;
    gap: 18px;
    align-items: flex-start;
    background: #fbf9f4;
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 18px;
    margin: 16px 0;
  }
  .quote img {
    width: 92px;
    height: 112px;
    object-fit: cover;
    border-radius: 6px;
    flex-shrink: 0;
    filter: grayscale(15%);
    box-shadow: 0 3px 10px rgba(43,38,32,.15);
  }
  .quote .who {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 4px;
  }
  .quote .role { font-size: 12.5px; color: var(--muted); margin-bottom: 8px; font-family: 'Helvetica Neue', Arial, sans-serif; }
  .quote blockquote {
    margin: 0;
    font-style: italic;
    font-size: 16.5px;
  }
  .quote .note { font-size: 14.5px; color: var(--muted); margin-top: 10px; font-style: normal; }
  @media (max-width: 560px) {
    .quote { flex-direction: column; }
    .quote img { width: 120px; height: 140px; }
  }

  /* ---------- code ---------- */
  pre {
    background: var(--code-bg);
    color: var(--code-ink);
    border-radius: 8px;
    padding: 16px 18px;
    overflow-x: auto;
    font-size: 13.5px;
    line-height: 1.55;
    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  }
  pre .cm { color: #a89f8d; }
  pre .kw { color: #e0a458; }
  pre .st { color: #b5c98a; }
  .code-label {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .1em;
    text-transform: uppercase;
    margin: 14px 0 6px;
  }
  .code-label.bad { color: #c0392b; }
  .code-label.good { color: #2e8b57; }

  /* ---------- takeaways ---------- */
  .takeaways li { margin-bottom: 8px; }
  .badge {
    display: inline-block;
    background: var(--accent-soft);
    color: var(--accent);
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 13px;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    margin: 2px 4px 2px 0;
  }

  footer {
    text-align: center;
    color: var(--muted);
    font-size: 13px;
    margin-top: 40px;
    font-family: 'Helvetica Neue', Arial, sans-serif;
  }
  #top {
    position: fixed;
    right: 22px;
    bottom: 22px;
    width: 42px;
    height: 42px;
    border-radius: 50%;
    border: none;
    background: var(--accent);
    color: #fff;
    font-size: 18px;
    cursor: pointer;
    opacity: 0;
    transition: opacity .25s;
    box-shadow: 0 4px 12px rgba(0,0,0,.2);
  }
  #top.show { opacity: 1; }
</style>
</head>
<body>

<header class="hero">
  <div class="kicker">The Robert C. Martin Clean Code Collection · Chapter Summaries</div>
  <h1>Book 1 · Clean Code — Chapter 1</h1>
  <div class="sub">Summary with the chapter's original artwork, figures &amp; author portraits</div>
  <img class="chapter-art" src="__CHAPTER_ART__" alt="Chapter 1 opener artwork from the book">
</header>

<nav class="toc">
  <ol>
    <li><a href="#there-will-be-code">There Will Be Code</a></li>
    <li><a href="#bad-code">Bad Code</a></li>
    <li><a href="#total-cost">The Total Cost of Owning a Mess</a></li>
    <li><a href="#grand-redesign">The Grand Redesign in the Sky</a></li>
    <li><a href="#attitude">Attitude</a></li>
    <li><a href="#primal-conundrum">The Primal Conundrum</a></li>
    <li><a href="#art">The Art of Clean Code?</a></li>
    <li><a href="#what-is">What Is Clean Code?</a></li>
    <li><a href="#schools">Schools of Thought</a></li>
    <li><a href="#authors">We Are Authors</a></li>
    <li><a href="#scout">The Boy Scout Rule</a></li>
    <li><a href="#conclusion">Conclusion</a></li>
    <li class="sep">|</li>
    <li><a href="#c-intro">Coding · Intro</a></li>
    <li><a href="#c-preparedness">Preparedness</a></li>
    <li><a href="#c-3am">3 AM Code</a></li>
    <li><a href="#c-zone">The Flow Zone</a></li>
    <li><a href="#c-debugging">Debugging</a></li>
    <li><a href="#c-late">Being Late</a></li>
    <li><a href="#c-help">Help</a></li>
    <li><a href="#c-takeaways">Takeaways</a></li>
  </ol>
</nav>

<div class="wrap">

<section class="card" id="intro">
  <p class="lead">"You are reading this book for two reasons. First, you are a programmer. Second, you want to be a better programmer. Good. We need better programmers."</p>
  <p>This opening chapter is the philosophical foundation of the whole book. It is prose-only — no code listings — and it answers one question: <em>why does clean code matter?</em> Below is a section-by-section summary, followed by the masters' definitions of clean code, the chapter's key takeaways, and a short illustration of the chapter's lesson.</p>
  <img src="__KENT_BECK__" alt="Portrait of Kent Beck" style="display:none">
</section>

<section class="card" id="there-will-be-code">
  <h2><span class="num">Section 1</span>There Will Be Code</h2>
  <p>Some argue that a book about code is behind the times — that we should worry about models and requirements, or that business people will soon generate programs straight from specifications. Nonsense, says Uncle Bob: <strong>we will never be rid of code</strong>, because code represents the <em>details</em> of the requirements.</p>
  <p>At some level those details cannot be ignored or abstracted — they have to be specified. And a specification detailed enough for a machine to execute it <em>is</em> programming. Languages will keep rising to higher levels of abstraction, and domain-specific languages will multiply, but every one of those specifications will still be code: rigorous, accurate, formal.</p>
  <div class="pull">The dream of machines that turn our vague feelings into perfect programs will never come true. Well-specified requirements are as formal as code — and can act as executable tests of that code.</div>
</section>

<section class="card" id="bad-code">
  <h2><span class="num">Section 2</span>Bad Code</h2>
  <div class="quote">
    <img src="__KENT_BECK__" alt="Portrait of Kent Beck">
    <div>
      <div class="who">Kent Beck</div>
      <div class="role">Implementation Patterns — quoted in the chapter's opening</div>
      <blockquote>"...this book is based on a rather fragile premise: that good code matters..."</blockquote>
      <div class="note">Uncle Bob disagrees: it is one of the most robust premises in our craft — we know good code matters because we have dealt for so long with its lack.</div>
    </div>
  </div>
  <p>He tells of a company that, in the late 80s, wrote a killer app. It was very popular — until release cycles stretched, bugs went unfixed, load times grew and crashes increased. The author shut it down in frustration and never used it again; the company went out of business shortly after. Rushed to market, they made a huge mess in the code; every new feature made it worse until it was unmanageable. <strong>It was the bad code that brought the company down.</strong></p>
  <p>Every experienced programmer knows the impediment: we call it <em>wading</em> — slogging through a morass of tangled brambles and hidden pitfalls, hoping for some clue of what is going on.</p>
  <p>So why did we write it? Probably in a rush, under pressure, tired, eyeing the backlog. We have all looked at a fresh mess, felt relief that it works, and chosen to leave it for another day. But in those days we didn't know <strong>LeBlanc's law</strong>:</p>
  <div class="pull">Later equals never.</div>
</section>

<section class="card" id="total-cost">
  <h2><span class="num">Section 3</span>The Total Cost of Owning a Mess</h2>
  <p>Messy code slows every change. Each modification breaks two or three other parts; no change is trivial. Every addition requires "understanding" the tangles, twists and knots so that more tangles, twists and knots can be added. Eventually the mess is so big, so deep and so tall that it cannot be cleaned up at all.</p>
  <p>As the mess builds, team productivity decreases, asymptotically approaching zero. Management then does the only thing it can think of — <strong>add more staff</strong> — but the newcomers don't know the design, don't know a change that matches its intent from one that thwarts it, and — under the same horrific pressure — they make more messes, driving productivity ever further toward zero.</p>
  <figure class="figure">
    <img src="__FIGURE_1_1__" alt="Figure 1-1: Productivity vs. time — a graph showing productivity falling asymptotically toward zero as the mess grows">
    <figcaption>Figure 1-1 — Productivity vs. time (original figure from the book)</figcaption>
  </figure>
</section>

<section class="card" id="grand-redesign">
  <h2><span class="num">Section 4</span>The Grand Redesign in the Sky</h2>
  <p>Eventually the team rebels and demands a redesign. Management, unable to deny the terrible productivity, authorizes the grand redesign in the sky. A <em>tiger team</em> of the best and brightest gets a green-field project to build something beautiful — while everyone else maintains the old system.</p>
  <p>Now the two teams race: the tiger team must reproduce everything the old system does, <em>and</em> keep up with the continuous changes made to it. Management won't replace the old system until the new one can do everything it does.</p>
  <div class="pull">The race can go on for ten years. By the time it is done, the original tiger team is long gone — and the current members are demanding that the new system be redesigned, because it is such a mess.</div>
  <p>Spending time keeping your code clean is therefore not just cost effective; <strong>it is a matter of professional survival.</strong></p>
</section>

<section class="card" id="attitude">
  <h2><span class="num">Section 5</span>Attitude</h2>
  <p>Why does good code rot so quickly? We complain about changing requirements, impossible schedules, stupid managers, useless marketing. But the fault, dear Dilbert, is not in our stars, but in ourselves: <strong>we are unprofessional</strong>.</p>
  <p>Programmers are deeply complicit in the planning of the project and share a great deal of the responsibility for failures that have to do with bad code. Managers and marketers look to us for the information they need to make promises; users look to us to validate how requirements will fit the system; project managers look to us to help work out the schedule.</p>
  <p>"But if I don't do what my manager says, I'll be fired." Probably not — most managers want the truth, even when they don't act like it. It is their job to defend the schedule; it is your job to defend the code with equal passion.</p>
  <div class="pull">Uncle Bob's doctor analogy: if a patient demanded you skip the hand-washing before surgery because it takes too long, you would absolutely refuse — you know the risks of infection better than the patient. It would be unprofessional to comply. So too it is unprofessional for programmers to bend to managers who don't understand the risks of making messes.</div>
</section>

<section class="card" id="primal-conundrum">
  <h2><span class="num">Section 6</span>The Primal Conundrum</h2>
  <p>Programmers face a conundrum of basic values. Every experienced developer knows that previous messes slow them down — and yet every developer feels pressure to make messes in order to meet deadlines. In short: <em>they don't take the time to go fast!</em></p>
  <div class="pull">True professionals know the second half of the conundrum is wrong. You will not make the deadline by making the mess — the mess slows you down instantly and forces you to miss the deadline. The only way to make the deadline, the only way to go fast, is to keep the code as clean as possible at all times.</div>
</section>

<section class="card" id="art">
  <h2><span class="num">Section 7</span>The Art of Clean Code?</h2>
  <p>Believing that messy code impedes you and that only clean code lets you go fast still leaves the question: <em>how do I write clean code?</em> Writing clean code is a lot like painting a picture — most of us can tell a well-painted picture from a bad one, but recognizing good art does not mean knowing how to paint.</p>
  <p>Writing clean code requires the disciplined use of a myriad little techniques, applied through a painstakingly acquired sense of "cleanliness" — the <strong>code-sense</strong>. Some of us are born with it; some of us have to fight to acquire it. It lets us see whether code is good or bad, and shows us the strategy for transforming bad code into good code:</p>
  <ul>
    <li>A programmer <em>without</em> code-sense sees the mess but has no idea what to do about it.</li>
    <li>A programmer <em>with</em> code-sense sees options and variations, chooses the best one, and plots a sequence of <em>behavior-preserving transformations</em> to get from here to there.</li>
  </ul>
  <div class="pull">In short: a programmer who writes clean code is an artist who can take a blank screen through a series of transformations until it is an elegantly coded system.</div>
</section>

<section class="card" id="what-is">
  <h2><span class="num">Section 8</span>What Is Clean Code?</h2>
  <p>There are probably as many definitions as there are programmers, so Uncle Bob asked some very well-known and deeply experienced ones. Here are their answers, with the portraits that appear beside them in the book.</p>

  <div class="quote">
    <img src="__BJARNE__" alt="Portrait of Bjarne Stroustrup">
    <div>
      <div class="who">Bjarne Stroustrup</div>
      <div class="role">Inventor of C++ and author of The C++ Programming Language</div>
      <blockquote>"I like my code to be elegant and efficient. The logic should be straightforward to make it hard for bugs to hide, the dependencies minimal to ease maintenance, error handling complete according to an articulated strategy, and performance close to optimal so as not to tempt people to make the code messy with unprincipled optimizations. Clean code does one thing well."</blockquote>
      <div class="note"><strong>Uncle Bob's reading:</strong> clean code should be <em>pleasing</em> to read; wasted cycles are inelegant; and bad code <em>tempts</em> the mess to grow (the "broken windows" metaphor of Dave Thomas and Andy Hunt — one broken window starts the process toward decay). Complete error handling and consistent naming show close attention to detail. Clean code is focused: each function, class and module exposes a single-minded attitude.</div>
    </div>
  </div>

  <div class="quote">
    <img src="__GRADY__" alt="Portrait of Grady Booch">
    <div>
      <div class="who">Grady Booch</div>
      <div class="role">Author of Object Oriented Analysis and Design with Applications</div>
      <blockquote>"Clean code is simple and direct. Clean code reads like well-written prose. Clean code never obscures the designer's intent but rather is full of crisp abstractions and straightforward lines of control."</blockquote>
      <div class="note"><strong>Uncle Bob's reading:</strong> like a good novel, clean code exposes the tensions of the problem, builds them to a climax, and gives the reader an "Aha! Of course!" as they resolve. "Crisp abstractions" is a fascinating oxymoron: our code should be matter-of-fact, containing only what is necessary — readers should perceive us to have been decisive.</div>
    </div>
  </div>

  <div class="quote">
    <img src="__DAVE__" alt="Portrait of Dave Thomas">
    <div>
      <div class="who">"Big" Dave Thomas</div>
      <div class="role">Founder of OTI, godfather of the Eclipse strategy</div>
      <blockquote>"Clean code can be read, and enhanced by a developer other than its original author. It has unit and acceptance tests. It has meaningful names. It provides one way rather than many ways for doing one thing. It has minimal dependencies, which are explicitly defined, and provides a clear and minimal API. Code should be literate since depending on the language, not all necessary information can be expressed clearly in code alone."</blockquote>
      <div class="note"><strong>Uncle Bob's reading:</strong> there is a difference between code that is easy to <em>read</em> and code that is easy to <em>change</em> — clean code makes enhancement by others easy. Cleanliness is tied to tests: "Code, without tests, is not clean. No matter how elegant it is... if it hath not tests, it be unclean." Minimal is better, and code should be literate — composed to be readable by humans.</div>
    </div>
  </div>

  <div class="quote">
    <img src="__FEATHERS__" alt="Portrait of Michael Feathers">
    <div>
      <div class="who">Michael Feathers</div>
      <div class="role">Author of Working Effectively with Legacy Code</div>
      <blockquote>"I could list all of the qualities that I notice in clean code, but there is one overarching quality that leads to all of them. Clean code always looks like it was written by someone who cares... code left by someone who cares deeply about the craft."</blockquote>
      <div class="note"><strong>Uncle Bob's reading:</strong> one word — <em>care</em>. That is really the topic of the book; an appropriate subtitle would be <em>How to Care for Code</em>. Someone took the time to keep it simple and orderly and paid attention to the details.</div>
    </div>
  </div>

  <div class="quote">
    <img src="__JEFFRIES__" alt="Portrait of Ron Jeffries">
    <div>
      <div class="who">Ron Jeffries</div>
      <div class="role">Author of Extreme Programming Installed and Extreme Programming Adventures in C#</div>
      <blockquote>"In recent years I begin, and nearly end, with Beck's rules of simple code. In priority order, simple code: runs all the tests; contains no duplication; expresses all the design ideas that are in the system; minimizes the number of entities such as classes, methods, functions, and the like."</blockquote>
      <div class="note"><strong>Uncle Bob's reading:</strong> Ron focuses on <em>duplication</em> — repeated code is an idea not well represented in the code — and on <em>expressiveness</em>: meaningful names (rename freely; modern tools make it cheap), one thing per object/method (Extract Method), and early, simple abstractions over recurring operations such as "find things in a collection". Reduced duplication, high expressiveness, early tiny abstractions — that is clean code for Ron.</div>
    </div>
  </div>

  <div class="quote">
    <img src="__WARD__" alt="Portrait of Ward Cunningham">
    <div>
      <div class="who">Ward Cunningham</div>
      <div class="role">Inventor of Wiki, inventor of Fit, coinventor of eXtreme Programming, Smalltalk and OO thought leader</div>
      <blockquote>"You know you are working on clean code when each routine you read turns out to be pretty much what you expected. You can call it beautiful code when the code also makes it look like the language was made for the problem."</blockquote>
      <div class="note"><strong>Uncle Bob's reading:</strong> clean code never surprises you — it is obvious, simple and compelling; each module sets the stage for the next, and the designer makes it look ridiculously simple, as all exceptional designs do. And beautiful code <em>makes the language look like it was made for the problem</em> — it is the programmer who makes the language appear simple, not the other way around.</div>
    </div>
  </div>
</section>

<section class="card" id="schools">
  <h2><span class="num">Section 9</span>Schools of Thought</h2>
  <div class="quote">
    <img src="__UNCLE_BOB__" alt="Portrait of Robert C. Martin (Uncle Bob)">
    <div>
      <div class="who">Robert C. "Uncle Bob" Martin</div>
      <div class="role">The author himself — portrait from the chapter's sidebar</div>
      <blockquote>"What about me (Uncle Bob)? What do I think clean code is? This book will tell you, in hideous detail..."</blockquote>
    </div>
  </div>
  <p>Martial artists do not all agree about the best martial art, or the best technique within one; masters found their own schools and gather students — Gracie Jiu Jitsu, Hakkoryu Jiu Jitsu, Jeet Kune Do. Students immerse themselves in one master's teaching, later may study under another, and some eventually found schools of their own.</p>
  <div class="pull">Consider this book a description of the <strong>Object Mentor School of Clean Code</strong>. None of these schools is absolutely right — yet within a particular school we act as though the teachings are right. Many recommendations here are controversial; you may violently disagree with some — that's fine. But they were learned through decades of experience and repeated trial and error, so whether you agree or not, respect the point of view — and learn from the other schools as well.</div>
</section>

<section class="card" id="authors">
  <h2><span class="num">Section 10</span>We Are Authors</h2>
  <p>The <code>@author</code> field of a Javadoc tells us who we are: <strong>authors</strong>. And authors have readers — so authors are responsible for communicating well with them. The next time you write a line of code, remember you are writing for readers who will judge your effort.</p>
  <p>How much is code really read? Have you ever played back an edit session (Emacs could replay a whole hour of keystrokes like a high-speed movie)? The vast majority of the playback was <em>scrolling and navigating to other modules</em>: Bob enters the module, scrolls to the function needing change, pauses, scrolls up to check a variable's initialization, types, erases, types again, erases again, scrolls to a caller, pops up a subclass to check for overrides...</p>
  <div class="pull">The ratio of time spent reading vs. writing is well over 10:1. Because this ratio is so high, we want the reading of code to be easy, even if it makes the writing harder. There is no escape from this logic: if you want to go fast, if you want to get done quickly, make it easy to read.</div>
</section>

<section class="card" id="scout">
  <h2><span class="num">Section 11</span>The Boy Scout Rule</h2>
  <p>It is not enough to write the code well — the code has to be <em>kept</em> clean over time. We have all seen code rot and degrade as time passes, so we must take an active role in preventing that degradation. The Boy Scouts of America have a simple rule we can apply to our profession:</p>
  <div class="pull">"Leave the campground cleaner than you found it."<br><small>— adapted from Robert Stephenson Smyth Baden-Powell's farewell message to the Scouts: "Try and leave this world a little better than you found it..."</small></div>
  <p>If we all checked in our code a little cleaner than when we checked it out, the code simply could not rot. The cleanup doesn't have to be big:</p>
  <ul>
    <li>change one variable name for the better,</li>
    <li>break up one function that's a little too large,</li>
    <li>eliminate one small bit of duplication,</li>
    <li>clean up one composite <code>if</code> statement.</li>
  </ul>
  <p>Can you imagine working on a project where the code simply got <em>better</em> as time passed? Continuous improvement is an intrinsic part of professionalism.</p>
</section>

<section class="card" id="prequel">
  <h2><span class="num">Section 12</span>Prequel and Principles</h2>
  <p>In many ways this book is a prequel to Uncle Bob's 2002 book <em>Agile Software Development: Principles, Patterns, and Practices</em> (PPP), which concerns the principles of object-oriented design and the practices of professional developers. If you have not read PPP, it continues the story told by this book; if you have, you will find its sentiments echoed here at the level of code.</p>
  <p>The chapter notes that the book makes sporadic references to design principles such as the <strong>Single Responsibility Principle (SRP)</strong>, the <strong>Open Closed Principle (OCP)</strong> and the <strong>Dependency Inversion Principle (DIP)</strong>, all described in depth in PPP.</p>
</section>

<section class="card" id="conclusion">
  <h2><span class="num">Section 13</span>Conclusion</h2>
  <p>Books on art don't promise to make you an artist. All they can do is give you some of the tools, techniques and thought processes other artists have used. So too this book cannot promise to make you a good programmer, or give you "code-sense" — it can only show you the thought processes of good programmers and the tricks, techniques and tools they use.</p>
  <p>Like a book on art, it will be full of details: lots of code, good code and bad code, bad code transformed into good code, lists of heuristics, disciplines and techniques, example after example. After that, it's up to you. Which recalls the old joke of the concert violinist who got lost on his way to a performance and asked an old man how to get to Carnegie Hall:</p>
  <div class="pull">"Practice, son. Practice!"</div>
</section>

<section class="card" id="takeaways">
 <h2><span class="num">Wrap-up</span>Key Takeaways</h2>
  <ul class="takeaways">
    <li><strong>Code is forever.</strong> Code is the precise language in which requirements are ultimately expressed — higher-level and domain-specific languages are code too.</li>
    <li><strong>Bad code is expensive.</strong> It slows teams asymptotically toward zero productivity, and has killed whole products and companies.</li>
    <li><strong>The only way to go fast is to keep the code as clean as possible at all times.</strong> Messes don't save time; they steal it instantly.</li>
    <li><strong>The fault is ours.</strong> Rotting code is a professionalism problem, not an excuse to blame schedules, managers or requirements.</li>
    <li><strong>Clean code, per the masters:</strong> elegant, efficient, one thing well, prose-like, decisive, tested, meaningful, minimal, literate, caring, expected — and beautiful when it makes the language look made for the problem.</li>
    <li><strong>We are authors.</strong> Reading vs. writing is over 10:1 — make code easy to read and it becomes easier to write.</li>
    <li><strong>The Boy Scout Rule.</strong> Leave every module a little cleaner than you found it, always.</li>
    <li><strong>Practice.</strong> No book can give you code-sense — only show you how to acquire it.</li>
  </ul>
  <p style="margin-top:14px">
    <span class="badge">good code matters</span>
    <span class="badge">later equals never</span>
    <span class="badge">go fast by staying clean</span>
    <span class="badge">code-sense</span>
    <span class="badge">10:1 read/write</span>
    <span class="badge">leave it cleaner</span>
    <span class="badge">practice</span>
  </p>
</section>

<section class="card" id="code">
  <h2><span class="num">A note on code in Chapter 1</span>From Bad to Clean — an Illustration</h2>
  <p><strong>Chapter 1 of the book contains no code listings</strong> — it is the philosophical foundation, and the code begins in Chapter 2 ("Meaningful Names"). So, to honor the chapter's message, here is a small <em>illustrative</em> before/after (not from the book) showing what its lessons look like in practice: intention-revealing names, one thing per function, no clever tricks — code that reads like prose and does one thing well.</p>

  <div class="code-label bad">✗ Before — what does this even do?</div>
<pre><span class="kw">public</span> String[] m(String s) {
    String[] p = s.split(<span class="st">","</span>);
    String r = <span class="st">""</span>;
    <span class="kw">for</span> (<span class="kw">int</span> i = <span class="st">0</span>; i &lt; p.length; i++) {
        <span class="kw">if</span> (p[i].length() &gt; <span class="st">3</span>) {
            r += p[i].trim().toUpperCase() + <span class="st">";"</span>;
        }
    }
    <span class="kw">return</span> r.split(<span class="st">";"</span>);
}</pre>

  <div class="code-label good">✓ After — obvious, single-purpose, easy to read</div>
<pre><span class="kw">public</span> List&lt;String&gt; extractLongNames(String commaSeparatedNames) {
    List&lt;String&gt; longNames = <span class="kw">new</span> ArrayList&lt;&gt;();
    <span class="kw">for</span> (String name : commaSeparatedNames.split(<span class="st">","</span>)) {
        String trimmed = name.trim();
        <span class="kw">if</span> (trimmed.length() &gt; MIN_NAME_LENGTH) {
            longNames.add(trimmed.toUpperCase());
        }
    }
    <span class="kw">return</span> longNames;
}</pre>
  <p style="font-size:14px;color:var(--muted)">Apply the Boy Scout Rule in miniature: rename, extract, remove duplication, simplify the condition — check the code in a little cleaner than you checked it out.</p>
</section>

<div class="part-divider">
  <div class="kicker">Book 2 · The Clean Coder — A Code of Conduct for Professional Programmers</div>
  <h2 class="part-title">Chapter 4 — Coding</h2>
  <div class="sub">The next chapter in this collection's PDF — the personal rules and principles behind professional coding</div>
  <img class="chapter-art" src="__CHAPTER4_ART__" alt="Chapter 4 'Coding' opener artwork from The Clean Coder">
</div>

<section class="card" id="c-intro">
  <p class="lead">This chapter describes Uncle Bob's personal set of rules and principles for coding. They are not about the code itself — they are about his <em>behavior, mood, and attitude</em> while writing code: his mental, moral, and emotional context. These are the roots of his confidence and "error-sense".</p>
  <p>He opens with a story from age 18, learning to type blind on an 029 keypunch. By the end of one long night he was typing nearly perfectly: typing blind turned out to be all about <em>confidence</em>, and confidence came from being able to <em>feel</em> an error the instant he made it. That error-sense — rapidly closing the feedback loop — is the key to mastery in every discipline he has studied. He cautions that these are one man's approach, not absolute truths; but perhaps by contemplating his coding milieu, you can "snatch the pebble from my hand".</p>
</section>

<section class="card" id="c-preparedness">
  <h2><span class="num">Preparedness</span>The Four Concerns You Must Juggle</h2>
  <p>Coding is intellectually exhausting because you must juggle four competing concerns at once:</p>
  <ul>
    <li><strong>Your code must work.</strong> You must understand the problem, how to solve it, and keep the code a faithful representation of that solution — consistent with the language, platform, architecture and the current system's warts.</li>
    <li><strong>It must solve the customer's real problem.</strong> Requirements often don't; seeing that and negotiating with the customer is up to you.</li>
    <li><strong>It must fit the existing system</strong> — without increasing its rigidity, fragility or opacity; dependencies must be well managed.</li>
    <li><strong>It must be readable by other programmers.</strong> Not just nice comments: the code must reveal your intent. "This may be the most difficult thing a programmer can master."</li>
  </ul>
  <p>Maintaining that focus is physiologically hard, and the opportunity for distraction is high. When you cannot concentrate, the code will be wrong — bugs, wrong structure, opacity — and will have to be reworked. Working while distracted creates waste.</p>
  <div class="pull">If you are tired or distracted, do not code. You'll only wind up redoing what you did. Instead, eliminate the distractions and settle your mind.</div>
</section>

<section class="card" id="c-3am">
  <h2><span class="num">Preparedness</span>3 AM Code</h2>
  <p>The worst code Uncle Bob ever wrote was at 3 AM in 1988, at a telecommunications start-up. After 18-hour days (and 60–70 hour weeks), he solved a timing problem by having his code send a message to itself through the event dispatch system — "sending mail". It was the wrong solution, but at 3 AM it looked pretty damned good, and he felt <em>dedicated</em>.</p>
  <p>That code bit them over and over: a faulty design everyone used and worked around, strange timing errors, infinite mail loops. They never had time to rewrite it but always had time to add another wart. Years later it was a team joke: "Look out! Bob's about to send mail to himself!"</p>
  <div class="pull">Don't write code when you are tired. Dedication and professionalism are more about discipline than hours. Tune your sleep, health and lifestyle so you can put in eight <em>good</em> hours per day.</div>
</section>

<section class="card" id="c-worry">
  <h2><span class="num">Preparedness</span>Worry Code</h2>
  <p>A big argument with a spouse, a customer crisis, a sick child — a background emotional process starts running in your mind, and concentration wavers. You stare at the screen, catatonic, churning on the worry instead of the code. Any code produced now will be trash.</p>
  <p>The trick is to <em>partition your time</em>: instead of brute-forcing code, spend a dedicated block (perhaps an hour) on the issue creating the worry — call home and check in, talk through the argument, think through the finances. You may not solve it, but you reduce the anxiety and quiet the background process. Ideally you settle anxieties at home so office time stays productive; if you're already at the office, an hour spent quieting the worry beats an hour of code you'll throw away (or worse, live with).</p>
</section>

<section class="card" id="c-zone">
  <h2><span class="num">Flow</span>The Flow Zone (a.k.a. "the Zone")</h2>
  <p>Every programmer knows the hyper-focused, tunnel-vision state called <em>flow</em> — or "the Zone". It feels productive and infallible, so programmers chase it and measure their self-worth by it. Uncle Bob's advice:</p>
  <div class="pull">Avoid the Zone.</div>
  <p>It is not really hyper-productive and it is certainly not infallible — it is a mild meditative state in which rational faculties are diminished in favor of a sense of speed. You <em>will</em> write more code, and go around the red/green/refactor loop faster, with a mild euphoria. But you lose the big picture and make decisions you will later reverse. Code written in the Zone comes out faster, but you'll revisit it more.</p>
  <p>When he feels himself slipping into the Zone, he walks away for a few minutes (email, tweets, lunch) or finds a pair partner. <strong>Pair programming makes the Zone virtually impossible</strong> — it is an uncommunicative state, while pairing demands constant communication; one of the most common complaints about pairing is that it blocks the Zone. Good! The exception: the Zone is exactly where you want to be when <em>practicing</em>.</p>
</section>

<section class="card" id="c-music">
  <h2><span class="num">Flow</span>Music &amp; Interruptions</h2>
  <p><strong>Music.</strong> At Teradyne in the late '70s he cranked Led Zeppelin and Pink Floyd while coding, thinking it helped concentration. Then he reopened a module he'd edited during <em>The Wall</em> and found the comments full of lyrics and editorial notations about dive bombers and crying babies. As a reader, he learned more about the author's music collection than about the problem. Music consumes a vital resource the mind needs for clean, well-designed code. (Maybe it helps others — but he suspects it mostly helps them enter the Zone.)</p>
  <p><strong>Interruptions.</strong> Are you rude when someone asks a question? The rude response often comes from the Zone. Two disciplines help: <em>pairing</em> (your partner holds the context while you take the call, and reconstructs it when you return) and <em>TDD</em> (a failing test holds the context of where you are). And some interruptions are simply unavoidable — the professional attitude is a polite willingness to help, because next time you may be the one who needs to interrupt someone else.</p>
</section>

<section class="card" id="c-block">
  <h2><span class="num">Flow</span>Writer's Block &amp; Creative Input</h2>
  <p>Sometimes the code just doesn't come. You read email, tweets, books, schedules; you call meetings; you do anything to avoid facing the workstation. Causes include too little sleep, worry, fear and depression.</p>
  <div class="pull">The simple solution that works almost every time: find a pair partner. There is a physiological change when you work with someone — the issues that were blocking you melt away and momentum returns. (Not perfect: sometimes it is followed by exhaustion, but it is the most reliable remedy he knows.)</div>
  <p>He also prevents blockage with <strong>creative input</strong>: creative output depends on creative input. He reads widely — software, politics, biology, astronomy, physics, chemistry, mathematics — but the best primer for his creative pump is science fiction ("nothing works better for me than good old space opera"). Creativity breeds creativity, and escapism helps: hours away from his problems while being stimulated by challenging ideas create an almost irresistible pressure to create. TV doesn't help him create; movies only a little; music helps him create <em>presentations</em>, not code.</p>
</section>

<section class="card" id="c-debugging">
  <h2><span class="num">Debugging</span>The 1972 Terminal Freeze (a war story)</h2>
  <p>One of the worst debugging sessions of his career: in 1972, terminals on the Teamsters' accounting system froze once or twice a day, unpredictably. There were no logs, counters or debuggers — only lights and toggle switches on the front panel, and five minutes at a time to peek at memory. The team built a real-time inspector on an ASR-33 teletype, wrote it in assembler, and added in-memory counters and state history.</p>
  <p>The terminals were interrupt-driven, with characters held in circular buffers. A freeze meant the three variables managing the buffer were out of sync — and the root cause was a <strong>concurrency bug</strong>: interrupt heads run in a different "thread" than application code, so shared variables must be protected (interrupts disabled around updates). Finding the one place that updated a variable with interrupts enabled took days of poring over an inches-thick listing — the variables were used <em>everywhere</em>, and in that assembler there was no way to tell a read-only reference from a write without following the logic.</p>
  <div class="pull">The vulnerability was about two microseconds long; a dozen terminals at 30 characters per second meant an interrupt every ~3 ms, so they'd expect a freeze-up one or two times a day. Bingo!</div>
  <p>Lesson: shared state touched by both "interrupt" and ordinary code must be protected from concurrent update — and tooling that shows every place a variable is touched turns days of study into minutes.</p>
</section>

<section class="card" id="c-debugging-time">
  <h2><span class="num">Debugging</span>Debugging Time Is Coding Time</h2>
  <p>Developers often treat debugging as a call of nature, but it is just as expensive to the business as coding — so anything that diminishes it is good. Uncle Bob estimates he now spends <strong>about ten times less</strong> time debugging than ten years earlier, chiefly by adopting Test Driven Development (red/green/refactor). Whether or not you adopt TDD, a professional must push debugging time as close to zero as possible — an asymptotic goal, but the goal nonetheless.</p>
  <div class="pull">Doctors don't like to reopen patients to fix something they did wrong; lawyers don't retry cases they flubbed. A developer who creates many bugs is acting unprofessionally.</div>
</section>

<section class="card" id="c-pacing">
  <h2><span class="num">Pacing</span>Pacing Yourself · Know When to Walk Away</h2>
  <p>Software development is a <strong>marathon, not a sprint</strong>. You win by conserving resources and pacing yourself, the way a marathon runner cares for her body before and during the race. Learn your own patterns of creativity and brilliance and take advantage of them rather than working against them.</p>
  <p>Can't go home till you solve this problem? Oh yes you can — and you probably should. Creativity and intelligence are fleeting; pounding a tired brain until the early hours just makes you more tired and less likely to see the solution. Disengage and let your creative subconscious work.</p>
  <div class="pull">Two of his most productive places: the car ride home (driving consumes noncreative mental resources, and that disengagement lets the mind hunt differently) and the shower (the spray wakes him to review what his brain solved overnight). Sometimes the best way to solve a problem is to go home, eat dinner, watch TV, go to bed, and wake up and shower.</div>
</section>

<section class="card" id="c-late">
  <h2><span class="num">Estimates</span>Being Late · Hope · Rushing · Overtime</h2>
  <p><strong>You will be late.</strong> It happens to the best and most dedicated of us. The trick is <em>early detection and transparency</em>: measure progress against the goal and maintain <strong>three fact-based end dates — best case, nominal case, and worst case</strong>. Be honest; do not incorporate hope into your estimates. Present all three numbers to the team and stakeholders, and update them daily. The worst case is telling everyone you'll be on time, up to the very end, and then letting them down.</p>
  <div class="pull">Hope is the project killer. If the trade show is in ten days and your three-number estimate is 8/12/20, you are not going to make it. Make sure the team and stakeholders understand, and don't let up until there is a fall-back plan. Don't let anyone else have hope.</div>
  <p><strong>Rushing.</strong> If your manager insists you "do what it takes" to make the deadline, <em>hold to your estimates</em> — they are more accurate than any changes made under confrontation. The only way to improve the schedule is to <strong>reduce scope</strong>. Do not be tempted to rush: shortcuts and extra hours in vain hope of a miracle give everyone false hope, delay the tough decisions, and slow everyone down. There is no way to rush.</p>
  <p><strong>Overtime.</strong> It can work and is sometimes necessary, but it is very risky: you will not get 20% more done by working 20% more hours, and it certainly fails beyond two or three weeks. Agree only if <strong>(1)</strong> you can personally afford it, <strong>(2)</strong> it is short term (two weeks or less), and <strong>(3)</strong> your boss has a fall-back plan if it fails — that last one is a deal breaker.</p>
</section>

<section class="card" id="c-false-delivery">
  <h2><span class="num">Professionalism</span>False Delivery · Define "Done"</h2>
  <p>Of all the unprofessional behaviors a programmer can indulge in, perhaps the worst is <strong>saying you are done when you know you aren't</strong>. Worse still is the insidious version: rationalizing a new definition of "done" — "done enough" — and moving on. It is contagious (one client defined "done" as "checked-in"; the code didn't even have to compile), and managers then hear that everything is fine until the freight train of unfinished work hits.</p>
  <p>The cure is an <strong>independent definition of "done"</strong>: business analysts and testers create <em>automated acceptance tests</em> (FitNesse, Selenium, RobotFX, Cucumber, …) that must pass before you may say you're done — written in a language stakeholders understand, and run frequently.</p>
</section>

<section class="card" id="c-help">
  <h2><span class="num">Professionalism</span>Help · Mentoring</h2>
  <p>Programming is <strong>hard</strong> — so hard it is beyond the capability of one person to do it well. So helping each other is a professional responsibility, not a favor:</p>
  <ul>
    <li><strong>Helping others.</strong> Don't sequester yourself and refuse queries; be fair and polite about your alone time (e.g. "don't bother me 10 AM–noon, door open 1–3 PM"). Watch for teammates in trouble and offer help — a fresh perspective is a profound catalyst. Sit down and write code together for the better part of an hour; you'll likely learn more than you give.</li>
    <li><strong>Being helped.</strong> Accept help graciously; don't protect your turf or push it away because you're under the gun. Give it thirty minutes; if it isn't helping, politely excuse yourself with thanks.</li>
    <li><strong>Asking for help.</strong> When stuck, befuddled, or unable to wrap your mind around a problem, call for help — it is unprofessional to remain stuck when help is easily accessible.</li>
    <li><strong>Mentoring.</strong> Training courses and books don't cut it: training less-experienced programmers is the responsibility of those with more experience, and juniors have a professional duty to seek out that mentoring.</li>
  </ul>
  <div class="pull">Programmers tend to be arrogant, self-absorbed introverts — collaboration is not instinctive for many of us, and yet it is critical to effective programming. So we require disciplines that drive us to collaborate.</div>
</section>

<section class="card" id="c-takeaways">
  <h2><span class="num">Wrap-up</span>Key Takeaways — Chapter 4: Coding</h2>
  <ul class="takeaways">
    <li><strong>Don't code when tired or distracted</strong> — 3 AM code becomes a team joke and a design wart. Eight good hours beat eighteen bad ones.</li>
    <li><strong>Avoid the Zone.</strong> It feels infallible but costs you the big picture; pairing is the best defense (and fine when practicing).</li>
    <li><strong>Quiet your worries</strong> by partitioning time; don't brute-force code you'll throw away.</li>
    <li><strong>Writer's block?</strong> Pair up; feed the pump with creative input (for him, science fiction).</li>
    <li><strong>Debugging time is coding time</strong> — drive it toward zero with TDD and good tooling.</li>
    <li><strong>Pace yourself</strong>; when stuck, walk away — the car and the shower are legitimate tools.</li>
    <li><strong>Never hope.</strong> Three fact-based end dates (best/nominal/worst), updated daily; reduce scope instead of rushing.</li>
    <li><strong>Overtime</strong> only if affordable, ≤ 2 weeks, and backed by a real fall-back plan.</li>
    <li><strong>Never falsely deliver.</strong> Define "done" with automated acceptance tests everyone understands.</li>
    <li><strong>Help, accept help, ask for help</strong> — and mentor; it's professional ethics, not kindness.</li>
  </ul>
  <p style="margin-top:14px">
    <span class="badge">error-sense</span>
    <span class="badge">no 3 AM code</span>
    <span class="badge">avoid the Zone</span>
    <span class="badge">pair programming</span>
    <span class="badge">TDD</span>
    <span class="badge">kill hope</span>
    <span class="badge">reduce scope</span>
    <span class="badge">definition of done</span>
  </p>
</section>

<section class="card" id="c-code">
  <h2><span class="num">A note on code in Chapter 4</span>Protecting Shared State — an Illustration</h2>
  <p><strong>Chapter 4 (like Chapter 1) contains no code listings</strong> — it's about the professional's mindset. Its one technical war story is the 1972 terminal freeze, a classic concurrency bug: three circular-buffer variables were manipulated by both "interrupt heads" and application code, and one update happened with interrupts enabled. Here is a small <em>illustrative</em> before/after (not from the book) of that lesson.</p>

  <div class="code-label bad">✗ Before — shared state updated without protection (the 1972 bug)</div>
<pre><span class="kw">private int</span> head;   <span class="cm">// read/written by "interrupt" code AND application code</span>

<span class="cm">// application thread — races with the interrupt handler:</span>
head = (head + <span class="st">1</span>) % BUFFER_SIZE;   <span class="cm">// two-microsecond vulnerability!</span></pre>

  <div class="code-label good">✓ After — one protected operation keeps the invariant</div>
<pre><span class="kw">private int</span> head;

<span class="kw">private synchronized void</span> advanceHead() {
    head = (head + <span class="st">1</span>) % BUFFER_SIZE;   <span class="cm">// interrupts disabled / atomic</span>
}</pre>
  <p style="font-size:14px;color:var(--muted)">Today we'd reach for <code>AtomicInteger</code>, a lock, or a concurrent queue — and a tool that shows every line touching the variable, turning days of reading into minutes.</p>
</section>

<footer>
  Summaries from <em>The Robert C. Martin Clean Code Collection</em>, Robert C. Martin, Pearson / Prentice Hall, 2011:
  Book 1 <em>Clean Code</em> — Chapter 1, and Book 2 <em>The Clean Coder</em> — Chapter 4 ("Coding").<br>
  Note: this PDF is a partial collection — it contains Clean Code Ch. 1 (plus front matter and the full index) and The Clean Coder's front matter + Ch. 4 (plus index). Chapters 2–3 of <em>Clean Code</em> are not present in the PDF, so the next chapter available in the book was summarized.<br>
  Chapter artwork, Figure 1-1 and the author portraits are embedded from the book's PDF. Quotes are short excerpts used for commentary.
</footer>

</div>

<button id="top" title="Back to top">↑</button>

<script>
  // scrollspy for the sticky nav
  const links = [...document.querySelectorAll('nav.toc a')];
  const sections = links
    .map(a => document.querySelector(a.getAttribute('href')))
    .filter(Boolean);
  const spy = () => {
    let current = null;
    for (const sec of sections) {
      if (sec.getBoundingClientRect().top <= 90) current = sec.id;
    }
    links.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + current));
  };
  window.addEventListener('scroll', spy, { passive: true });
  spy();

  // back-to-top button
  const btn = document.getElementById('top');
  window.addEventListener('scroll', () => {
    btn.classList.toggle('show', window.scrollY > 600);
  }, { passive: true });
  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
</script>

</body>
</html>
"""


def main():
    mapping = {
        "__CHAPTER_ART__": data_uri("chapter-art.png"),
        "__FIGURE_1_1__": data_uri("figure-1-1.jpeg"),
        "__KENT_BECK__": data_uri("kent-beck.png"),
        "__BJARNE__": data_uri("bjarne-stroustrup.png"),
        "__GRADY__": data_uri("grady-booch.png"),
        "__DAVE__": data_uri("dave-thomas.png"),
        "__FEATHERS__": data_uri("michael-feathers.png"),
        "__JEFFRIES__": data_uri("ron-jeffries.png"),
        "__WARD__": data_uri("ward-cunningham.png"),
        "__UNCLE_BOB__": data_uri("uncle-bob.png"),
        "__CHAPTER4_ART__": data_uri_ch4("chapter4-art.png"),
    }
    html = TEMPLATE
    for key, uri in mapping.items():
        html = html.replace(key, uri)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clean-code-chapter-1.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {out} ({os.path.getsize(out):,} bytes)")


if __name__ == "__main__":
    main()
