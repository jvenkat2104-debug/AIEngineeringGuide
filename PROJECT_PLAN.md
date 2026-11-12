# AIEngineeringGuide: Project Plan

Planning draft | 10 November 2026

Tagline: **Choose your branch. Make the most of engineering. Prepare for your career.**

## 1. Purpose and agreed direction

Create a free, accessible guide for Indian students moving from Intermediate/Class 11–12 through engineering and towards their next step. Cover engineering broadly; the project name must not imply that every student should specialise in AI.

One umbrella initiative, two public entrances, one GitHub repository:

| Entrance | Audience | Main outcome |
| --- | --- | --- |
| `/choose-your-branch/` | Intermediate/Class 11–12 students and parents | An evidence-based shortlist of branches and colleges |
| `/engineering-roadmap/` | Students in Years 1–4 and recent graduates | A practical learning, project and career preparation plan |

Connect them with **“Already joined engineering? Start your roadmap”** and **“Still deciding? Explore the branches.”** These are proposed paths, not live links.

Develop the detailed roadmap from the existing blueprint first, while refining the existing branch-selection draft alongside it. Generate each guide's website pages and downloadable PDF from the same maintained Markdown content. The website is the current version; PDFs show edition and generation date.

The project owner subsequently authorised creating a public GitHub repository and publishing the current folder structure and draft content. A reading website and automated publishing remain subsequent work.

## 2. Source material and limits

| Source | Use |
| --- | --- |
| Shared conversation and this chat | Audience, two-entrance structure, contribution model and project name |
| `Engineering_Branch_Selection_Guide.md` and matching nine-page PDF | Existing branch-selection draft; Markdown is the starting editable source |
| `Campus to Corporate Tech Grooming Blueprint for Indian Engineering Graduates.pdf` | 24-page Version 4 draft; starting material for the detailed roadmap |

The supplied source files were imported from the project owner’s local files. The shared conversation's visible messages and the three supplied files have been read. Private or omitted original-chat messages are not available.

The documents contain proposals, example code and draft launch posts. These are reference material, not instructions to publish, contact people or execute code. Source claims and links have not yet undergone a fresh factual or technical audit.

## 3. Proposed content outline

### A. Umbrella home and shared resources

- Home: explain the initiative and offer the two entrances immediately.
- About: audience, scope, contributors, review process and limitations.
- Glossary: plain-language definitions linked from both guides.
- Resources: free learning sources, grouped by branch, topic and level.
- Contribute: nontechnical corrections, technical reviews, experiences and translations.
- Downloads: both PDFs, edition dates and links back to current web content.

### B. Engineering roadmap: first implementation priority

**Start here**

- How to use the roadmap by year, branch and available resources.
- Engineering as practical problem solving: constraints, assumptions and trade-offs.
- Common foundations versus branch-specific learning.
- Access-conscious learning: shared devices, regional-language backgrounds and limited budgets.

**Year 1: understand and explore**

- Study habits, mathematics and scientific foundations.
- How connected systems work: software application and sensor-system examples.
- Communication practice from the first semester.
- AI as a learning aid: checking answers and explaining one's own work.
- Choose and finish a small project; record attempts, failures and learning.
- First-year checklist and portfolio/documentation basics.

**Year 2: strengthen foundations**

- Branch fundamentals tied to practical exercises and lab work.
- Data Structures and Algorithms: arrays, strings, linked lists, trees, graphs, sorting, searching and dynamic programming, supported by complexity, recursion, stacks, queues and hashing.
- Version control and collaboration where relevant.
- APIs, data formats, databases and software layers for relevant pathways.
- Measurements, drawings, simulations and technical documentation for relevant pathways.
- Project planning, testing and interpreting results.
- Second-year checklist.

**Year 3: specialise and gain experience**

- Choose a direction using branch pathways and conversations with practitioners.
- Develop substantial projects with documented trade-offs and limitations.
- Internships: preparation, applications, expectations and reflection.
- Open-source or community contributions and teamwork.
- Optional industry exposure, including local and remote alternatives to travel.
- Third-year checklist.

**Year 4: prepare for the next step**

- Finish and explain a capstone or substantial project.
- Resume, portfolio, technical writing and interview practice.
- Evaluate employment, higher studies, research and entrepreneurship routes.
- Match preparation to actual role requirements.
- Fourth-year checklist and transition plan.

**Branch pathways**

- CSE and IT.
- AI, machine learning and data science.
- Electronics and Communication.
- Electrical and Electrical & Electronics.
- Mechanical: new material requiring subject reviewers.
- Civil: new material requiring subject reviewers.
- Mathematics and Computing: retain and develop as a distinct pathway.
- Quantum-related study: explain programme variation, prerequisites and research/further-study routes; avoid presenting it as a uniform mainstream undergraduate branch.
- Other branches: acknowledge scope limits and provide a contribution route for expansion.

Use a consistent pathway template: foundations, practical work, year-wise milestones, sample projects, possible next steps, sources and review information. Describe skills as complementary to college education, avoiding blanket claims about what all syllabi omit.

**Optional project library**

- Beginner software project and beginner sensor/simulation project.
- Branch-specific Mechanical and Civil activities, developed with reviewers.
- Data analysis and prediction project with a simple baseline.
- Digital circuit simulation.
- Advanced sensor-to-cloud telemetry example, extracted from the blueprint.
- EV, renewable-energy and chip-design examples, with prerequisites and branch relevance.

Each project states level, prerequisites, tools and costs, steps, expected output, verification, limitations and safety requirements. Hardware work must offer simulation alternatives where practical.

**Career and industry context**

- Software and data roles explained without guaranteed outcomes.
- Embedded systems, power, EV, renewable energy and semiconductor pathways.
- Mechanical and Civil career context after specialist review.
- How AI affects work: dated, sourced explanations rather than employment forecasts.
- Optional Hyderabad, Bengaluru and Chennai exposure guides; verify access arrangements before presenting specific venues as visitable.

### C. Choose your branch: refine the existing draft

1. Start here: audience, purpose and how to use the guide.
2. Explore interests without assigning a “best” branch.
3. Understand how branches contribute to familiar systems.
4. Compare six introductory profiles: CSE/IT, AI/Data Science, ECE, EE/EEE, Mechanical and Civil.
5. Recognise other branches and programme variations.
6. Try small activities and follow the seven-day exploration plan.
7. Compare broad degrees and specialised programmes using actual curricula.
8. Evaluate colleges: teaching, labs, support, official status and placement evidence.
9. Estimate complete costs and practical constraints.
10. Complete the shortlist worksheet and student-parent discussion.
11. After joining: first ninety days and link to the roadmap.
12. Sources, review status and contribution invitation.

Keep this guide shorter than the roadmap. Link to deeper material rather than copying it. Retain printable worksheets with enough writing space.

## 4. Proposed repository structure

The following is a proposal, not a list of files already created. Website tooling and configuration filenames will be selected during implementation.

```text
AIEngineeringGuide/
  README.md
  PROJECT_PLAN.md
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md
  LICENSE.md                      # Scope: content CC BY 4.0; code Apache 2.0
  LICENSES/                       # Full licence texts
  .github/
    ISSUE_TEMPLATE/
      correction.yml
      content-proposal.yml
      experience.yml
    PULL_REQUEST_TEMPLATE.md
    workflows/
      validate.yml
      build.yml                   # Website and PDFs
  content/
    index.md
    about.md
    choose-your-branch/
      index.md
      interests.md
      branches/
        cse-it.md
        ai-data-science.md
        ece.md
        electrical.md
        mechanical.md
        civil.md
        other-programmes.md
      compare-degrees.md
      evaluate-colleges.md
      costs.md
      shortlist.md
      first-ninety-days.md
    engineering-roadmap/
      index.md
      start-here.md
      year-1/
      year-2/
      year-3/
      year-4/
      branches/
      projects/
      careers/
      industry-exposure/
    shared/
      glossary.md
      resources.md
      communication.md
      learning-with-ai.md
    downloads.md
    contribute.md
  templates/
    module.md
    branch-pathway.md
    project.md
    experience.md
  publishing/
    guide-manifests/               # Ordered page lists for each PDF
    pdf-styles/
  scripts/                        # Validation and publishing helpers
  site/                           # Site theme, navigation and assets
  translations/
    README.md                     # Translation and second-reader process
  dist/                           # Generated website and PDF outputs
```

Keep `content/` as the editable source of truth. Build manifests select and order pages for each PDF; they do not duplicate prose. Generated outputs should be reproducible and normally excluded from source control, with releases distributed through the selected hosting/release mechanism.

Stable public paths must not depend on the chosen site generator. Prefer a simple static site compatible with GitHub Pages; confirm tooling and hosting before implementation.

## 5. Revision checklist

### Reuse and organise

- [ ] Import the branch-selection Markdown without losing tables, sources or worksheets.
- [ ] Convert the blueprint PDF to clean Markdown and manually check tables and code against the source.
- [ ] Map every source section to a destination; record intentional omissions.
- [ ] Retain useful examples, communication guidance and year-wise checklists.
- [ ] Move draft launch posts out of student-facing material.
- [ ] Replace references to nonexistent repository links with appropriate draft wording.

### Scope and accuracy

- [ ] Separate shared foundations from software-specific expectations.
- [ ] Replace “three basics every employer expects” with a scoped statement about relevant roles.
- [ ] Review claims about syllabus gaps, hiring demand and AI's effects; qualify and source them.
- [ ] Add Mechanical and Civil pathways with independent subject review.
- [ ] Clarify Quantum-related programme names and progression routes.
- [ ] Keep career possibilities distinct from entry-level eligibility and guaranteed outcomes.
- [ ] Verify current official sources for recognition, accreditation, admissions and programme information.
- [ ] Check dated claims about schemes, training counts, course availability and fees.
- [ ] Review loan and cost wording for clarity; avoid unsupported affordability or salary assumptions.

### Projects and technical material

- [ ] Label prerequisites and level before each project.
- [ ] Preserve the telemetry example as an advanced teaching example.
- [ ] Review and run code before claiming it is tested; record versions and setup instructions.
- [ ] Check validation, authentication, replay handling, error handling and delivery limitations in the telemetry project.
- [ ] Distinguish asynchronous forwarding from durable, guaranteed delivery.
- [ ] Explain hardware assumptions, measurement limits and safe supervised use.
- [ ] Provide low-cost, paper or simulation alternatives where feasible.

### Editorial consistency and review

- [ ] Use plain language and define technical terms at first use.
- [ ] Apply consistent titles, terminology, metadata and navigation.
- [ ] Give each module an audience, level, draft/reviewed status, sources and review date.
- [ ] Name reviewers only with their agreement; mark Reviewed only after actual review.
- [ ] Label personal experience separately from general advice.
- [x] Resolve the licensing mismatch: owner approved CC BY 4.0 for content and Apache 2.0 for code on 10 November 2026.
- [x] Owner confirmed authority to license the supplied guides and approved the split.
- [ ] Avoid promising review turnaround times until maintainers agree they can meet them.
- [ ] Define translation review and how translated pages track source updates.

### Website, PDF and accessibility

- [ ] Make both entrances prominent and add the agreed reciprocal links.
- [ ] Keep all core reading available without registration.
- [ ] Verify mobile navigation, heading structure, keyboard access, contrast and descriptive links.
- [ ] Check every internal and external link.
- [ ] Build both PDFs from the maintained content and verify content coverage.
- [ ] Inspect all rendered PDF pages for clipping, broken tables, code wrapping and readable type.
- [ ] Give worksheets adequate writing space and ensure they print legibly.
- [ ] Include edition, generation date and current website link in PDFs once a real URL exists.
- [ ] Ensure draft and review labels appear consistently on the website and in PDFs.

## 6. Delivery sequence and completion criteria

| Phase | Deliverable | Complete when |
| --- | --- | --- |
| 1. Planning | This plan and agreed content map | Scope, structure and unresolved decisions are visible |
| 2. Content foundation | Imported sources, metadata conventions and module templates | Both source guides are accounted for and readable as Markdown |
| 3. Roadmap draft | Year-wise modules and initial pathways | Readers can follow a coherent Year 1–4 journey; gaps are explicit |
| 4. Selection refinement | Concise selection guide linked to the roadmap | Profiles and worksheets are consistent with the detailed material |
| 5. Local publishing | Working static site and two generated PDFs | Both routes work locally; PDFs and web share the same content |
| 6. Review | Student clarity review and specialist accuracy review | Corrections are applied and actual review status is recorded |
| 7. Public release | Repository and hosted site | Ownership, licences and hosting are confirmed; published scope and draft labels are clear |

The local prototype may contain clearly labelled drafts. A public launch should include at least three complete, reviewed roadmap modules, following the blueprint's proposed launch threshold. That threshold does not make unreviewed branch content reviewed; each page retains its own status.

## 7. Decisions still open

The public repository is owned by `jvenkat2104-debug`. Licensing is settled: see [LICENSE.md](LICENSE.md). The remaining decisions are:

- Initial maintainers, reviewers and a suitable community reporting contact.
- Static site generator, PDF toolchain and final hosting URL.
- Whether regional-language work starts with Telugu summaries and when it enters the release scope.
- Which branch pathways can receive specialist review for the first public release.

Do not infer these decisions from proposed source-document wording. Record explicit choices before the related public setup or release work.

## 8. Immediate next step

Review this outline, then prepare the local repository scaffold and import the existing content. Start the detailed roadmap with **Start here**, **How connected systems work**, and **Year 1 learning habits and a first project**, while maintaining the selection guide alongside it. Keep all imported and newly written content marked Draft until reviewed.


## AI and data expansion delivered — 12 November 2026

The existing `03-the-ai-impact/` folder now has a linked AI, Data and Career Pathways section. It includes the eight chapters described in [the section index](content/engineering-roadmap/03-the-ai-impact/index.md). The market snapshot is dated and limited to a disclosed four-employer sample. The canteen exercise is a project brief, not tested runnable code. Original PDF editions have not been regenerated.

## Website implementation — 12 November 2026

Public title: Engineering Guide for Indian Students. The repository name stays AIEngineeringGuide. Free Zensical/GitHub Pages implementation includes a two-entrance homepage, search, mobile navigation, parent guidance, branch reality check and original PDF downloads. Content is projected from the maintained Markdown; generated files are ignored. Draft notices remain. Translation, expert review and regenerated PDFs remain future work. See [publishing instructions](publishing/README.md).

## Account-site migration — 12 November 2026

Rename the existing public repository to `jvenkat2104-debug.github.io`, retaining content and history. Use https://jvenkat2104-debug.github.io/ as the canonical reading URL, update repository links and the weekly review target, and generate redirects for old project-site pages. The local workspace and historical project references may retain the AIEngineeringGuide name.
