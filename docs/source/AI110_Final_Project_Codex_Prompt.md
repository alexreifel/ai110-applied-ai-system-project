# Codex handoff: CodePath AI110 Project 4 — Applied AI System

You are helping me, Alex Reifel, build my CodePath AI110 final project on my Mac. Read this entire prompt, including both source appendices, before working. The appendices contain the full supplied project description and grading rubric. Do not replace them with assumptions from the starter repository or another CodePath assignment.

## My objective and working context

I want a complete, understandable implementation that meets every required feature, with real validation and clear documentation. I want to review the result and iterate. Do not add optional extensions unless I explicitly request them. Their complete rubric is included for reference, not as authorization to implement them.

I study economics, data science, and computer science/math at NYU. I can work with Python, but I am learning LLM integration, RAG, agent workflows, and reliability engineering. Explain meaningful architectural choices in concrete language and keep the code approachable. Avoid unnecessary frameworks, infrastructure, and unrelated features.

This chat is a handoff from ChatGPT, which could inspect the course and GitHub but could not access my Mac. You are running in my local Codex workspace and should inspect the actual selected directory rather than guessing a path. My course projects are in a folder for CodePath AI 110, but the exact path is not provided. Do not recursively search my whole home directory or unrelated personal files. Follow applicable AGENTS.md instructions and preserve all existing uncommitted work.

## First response: inspect and propose, then let me choose

The final project's base and feature have NOT been selected. A previous assistant recommended extending the Music Recommender, but that was a suggestion, not my decision. Do not silently select it or begin implementing a new idea.

1. Inspect the selected workspace, relevant README, source files, tests, Git status, branches, remotes, and applicable AGENTS.md files. If this is not the relevant course directory, ask me for the course folder path.
2. Identify which eligible Modules 1–3 projects are available and what they currently do. Inspect actual current files; do not assume an earlier assistant's claims are still true.
3. Give me 2–3 concrete extension options grounded in the available projects. For each, explain the original behavior, the new user-facing behavior, the substantial AI feature, how reliability will work, API needs, scope, and why it satisfies the required rubric. Recommend one manageable option.
4. Show a short implementation plan and the proposed dedicated final-project folder/repository. Ask me to choose the base and extension, then pause before implementing. Continue read-only inspection if useful while awaiting that choice.
5. Once I choose and authorize implementation, carry it through coding, testing, documentation, commits, and publication as described below. Do not repeatedly ask permission for routine implementation decisions within that chosen scope.

## Known prior repositories and caveats

These are discovery pointers, not proof of current completion:

- Module 1 Game Glitch Investigator: https://github.com/alexreifel/ai110-module1show-gameglitchinvestigator-starter
- Module 2 PawPal+: https://github.com/alexreifel/ai110-module2show-pawpal-starter
- Module 3 Music Recommender Simulation: https://github.com/alexreifel/ai110-module3show-musicrecommendersimulation-starter
- Module 4 DocuBot Tinker: https://github.com/alexreifel/ai110-module4tinker-docubot-starter
- Module 5 BugHound Tinker: https://github.com/alexreifel/ai110-module5tinker-bughound-starter

The final instructions explicitly require a base from Modules 1–3. DocuBot and BugHound are useful learning references, but do not use either as the base without my obtaining instructor approval.

The Music Recommender was previously implemented as a deterministic, content-based weighted ranking system over 20 synthetic songs. Prior work reportedly included explanations, three profiles, weight experiments, pytest tests, and CI. Verify all of that. It was not an LLM or RAG application. Do not relabel existing ranking logic or existing tests as a substantial NEW AI feature.

I recently discovered that my local BugHound clone might point at CodePath's official repository rather than my fork. I subsequently created my fork. ChatGPT supplied remote-reconfiguration commands, but has not verified whether I ran them. Never assume local remotes are correct. Do not repair unrelated repositories as part of the final project.

Gemini access was previously problematic, including a 403 error. A working API key, billing, model access, and available quota are NOT established. Inspect configuration names without printing secret values. Never commit .env files or credentials. Use .env.example with placeholders. Do not enable billing, incur unapproved charges, or assume a quota quoted in course material is current.

## Deadline and course sources

- Final project page: https://courses.codepath.org/courses/ai110/unit/9#!projects
- Rubric: https://courses.codepath.org/courses/ai110/pages/grading#heading-project-4-applied-ai-system
- Demo Day overview: https://courses.codepath.org/courses/ai110/unit/10#!overview

Previously observed deadline: Monday, November 16, 2026, 2:59 a.m. America/New_York, equivalent to Sunday, November 15, 11:59 p.m. Pacific. The browser displayed Monday November 16, 5:29 p.m. GMT+9:30. Previously observed Demo Day: Wednesday November 18, 2026, 8 p.m. New York time. These dates are prior observations, not included in the attached description. Verify current course timing if accessible; otherwise flag them as unverified. Do not invent an extension or claim a late submission is on time. Prioritize core completion if time is short.

The appendices below are the supplied requirements. If you find a material contradiction in a newer official page, explain it and ask only the focused question needed to resolve scope. Do not silently drop requirements.

## Repository setup after I select the project

- Preserve my original submission and all its uncommitted changes. Create a dedicated copy in a new final-project directory and a separate new public GitHub repository, retaining original commit history as the assignment requests. Do not initialize a conflicting README in the empty GitHub repository.
- Inspect Git authentication and the actual target owner/name. Before any push, check fetch and push URLs, branch tracking, remote.pushDefault, and branch-specific push settings. Ensure all push destinations are the selected new alexreifel repository, never CodePath or the original submission. If retaining an upstream remote, make it fetch-only with pushing disabled. Never force-push or rewrite existing history.
- My authorization to implement the chosen plan includes creating and pushing to its dedicated new public repository. Inspect staged content for secrets or unrelated personal material before publishing. Do not change visibility of an existing private repository to satisfy this instruction.
- Use a project-local virtual environment and an appropriate supported Python version. Document the actual interpreter and dependency setup. Include assets/ and diagrams/ as requested; retain otherwise-empty required directories with a small explanatory file if needed.
- Preserve the base behavior unless the selected extension intentionally changes it, and explain the change.

## Implementation standards

- Implement one substantial new AI capability integrated into the real application workflow. Show the full path from user input through the new feature, validation, core processing, and output. A disconnected demonstration or decorative LLM call is insufficient.
- If choosing RAG, generated answers must use retrieved content, with traceable source references and meaningful handling of insufficient context. Retrieval alone is not generation.
- If choosing an agent, make its steps and allowed actions explicit and bounded. Log observable actions, tool inputs/outputs where appropriate, and brief decision summaries. Do not request or save hidden model chain-of-thought as evidence.
- If choosing specialization, show the actual prompting/model configuration and how behavior differs from baseline. Do not claim fine-tuning when you only used prompts.
- If choosing reliability as the main new feature, it must materially change the application's behavior through integrated validation, evaluation, or self-checking. Merely adding ordinary unit tests or CI to an otherwise unchanged app is not sufficient.
- Prefer deterministic validation around nondeterministic model output. Handle empty/malformed inputs, unsupported requests, invalid output structure, provider errors, and timeouts as appropriate to the chosen system. Use bounded retries only when justified.
- Include user-facing fallback/error messages and useful logs without secrets. Distinguish missing credentials, provider failure, invalid output, and legitimate no-result cases.
- Mock clients and offline modes are useful for repeatable tests, but label them clearly. Never call a mock result a successful live AI run. If live access is unavailable, complete everything independently possible and report the specific remaining gap. Do not claim full end-to-end live verification.
- Keep optional stretch work out of scope. If a necessary core implementation incidentally satisfies a bonus item, document that honestly without expanding the build to chase bonuses.

## Validation and evidence

- Establish the existing baseline by running relevant tests before changes. Record pre-existing failures separately.
- Run pytest after implementation, along with applicable existing checks. Add meaningful tests for new behavior and regressions. Include at least one test proving a chosen guardrail rejects/changes an unsafe or invalid case; when feasible demonstrate it fails without the guardrail and passes with it.
- Run the documented application commands from a clean setup or otherwise verify that setup reproducibly. Test the actual user entry point, not only helper functions.
- Demonstrate at least THREE end-to-end example inputs and outputs. Include representative normal requests and separate reliability/error examples. Use actual captured results, commands, mode, and model details as appropriate. Never invent execution logs or paste hypothetical outputs as observed evidence.
- Include a before/after comparison showing that the new feature meaningfully changes the base application. Make comparisons fair and explain what they do and do not establish. Scores are not probabilities of correctness unless genuinely calibrated.
- Keep validation results parseable: Markdown tables, fenced code blocks, or committed .txt/JSON logs. Screenshots and video cannot replace this evidence.
- Retain existing CI and update it for the final repository. If absent, add a small GitHub Actions pytest workflow as an engineering safeguard, not a claim that CI is required by the rubric. CI must use mock/offline tests without embedded API secrets, so ordinary pushes can run it reproducibly. Separate live smoke tests when needed.
- Once pushed, inspect the workflow run and report its real status. If actions are disabled or unavailable, describe the blocker accurately rather than claiming CI passed. Do not change account-wide security settings.

## Required documentation and presentation preparation

1. README.md: original project named explicitly with its original scope; new goal and feature; architecture explanation; design tradeoffs; exact install/run/test steps; prerequisites and configuration; THREE real end-to-end input/output examples; reliability results; limitations and any live-access gap. Make the difference between old and new behavior clear.
2. diagrams/architecture.mmd or a Markdown Mermaid source file: actual components and input → processing → output flow, including checks and any human review. Link it from README. A PNG alone is insufficient.
3. model_card.md: clearly labeled sections answering ALL reflection and ethics prompts in Appendix A and the reflection criteria in Appendix B. Include biases, limitations, misuse and mitigations, testing observations, AI collaboration, accepted suggestion, rejected/revised suggestion, and future improvements. Reflection only in README does not earn these points.
4. Honest authorship: record actual AI assistance and actual decisions as we work. Do not fabricate my experiences, surprise, human evaluation, or accepted/rejected suggestions. Agent-selected revisions can be described as agent choices, not attributed to me. Draft factual technical sections from evidence; identify any personal reflection requiring my review before submission. Ask a focused question if a required personal decision cannot be grounded in the session.
5. docs/presentation_outline.md: a concise 5–7 minute outline with the problem, base vs extension, architecture, demo commands, reliability evidence, limitations, and reflection. This prepares the required presentation; it does not claim I have delivered it. A polished slide deck or Loom recording is not requested.
6. Portfolio text: draft a short project summary and reflection paragraph with the verified GitHub link, clearly marked for my review where personal wording is involved. Do not publish it elsewhere.
7. docs/requirements_checklist.md: map EACH of the 21 one-point required rubric rows to specific code, documentation, and observed evidence. Also track non-rubric instructions such as presentation preparation and repository setup. Use Complete / Partial / Blocked / Requires Alex review as appropriate. Report gaps honestly and do not assign an official grade.

## Commits, publishing, and final report

- Make 2–3 meaningful NEW commits on top of the inherited history. Aim for three: core feature; reliability/tests/CI; documentation/evidence/presentation outline. Adjust grouping to keep commits coherent and verified. Do not manufacture empty commits or include unrelated changes.
- Push only to the new final-project repository after verifying the destination and staged content. Do not push to the original base submission or CodePath.
- Do not submit to CodePath, send messages, record/upload a video, or publish elsewhere. I want to review the implementation first.
- Finish with the local project path, repository URL, commit hashes and purposes, exact run/test commands, test results, CI run URL/status, a concise rubric-completion assessment, and any outstanding live-access or personal-review items. Explain how the new feature works and what I should review first.
- Persist through ordinary implementation issues. Stop only for a real missing decision, unavailable credential/access, a destructive action beyond scope, or a specific blocker you cannot resolve. Do all independent work before reporting a blocker.

---

# Appendix A — Full project description supplied by Alex

The following text is preserved from Alex's attachment. Its Example Extensions table arrived empty; no missing rows have been invented. The requirements and later examples remain intact.

## Show What You Know: Applied AI System

### ℹ️ Project Overview

**⏰ \~4 hours**

This final project is your opportunity to bring everything together, from debugging and design (Module 1-2) to reasoning and retrieval (Module 3-4), and finally agentic workflows and reliability testing (Module 5).

You'll **choose one of your previous projects** from Modules 1-3 and **extend it into a full applied AI system** that solves a meaningful problem or automates a reasoning task. This is your chance to evolve an earlier prototype into a polished, professional artifact.

Your system should demonstrate **responsible design**, **technical creativity**, and **clear explanation** of how the AI works and why it's trustworthy.



#### 🎯 Goals

By completing this project, you will be able to...

- Extend and redesign a prior mini-project into a cohesive, end-to-end AI integrated system.
- Implement modular components (retrieval, logic, or agentic planning) using Python.
- Test and evaluate system reliability and guardrails through structured experiments.
- Document and explain the AI's decision-making process clearly and responsibly.
- Communicate results through a professional presentation and portfolio entry.

**Key terms**

By the end of the module, practice your technical communication; attempt to use these words in a sentence aloud.

- agent
- guardrail
- human-in-the-loop
- orchestration
- RAG (retrieval-augmented generation)
- reliability testing
- verification

---

📊 Before you start, review the [**Grading Rubric**](https://courses.codepath.org/courses/ai110/pages/grading#heading-project-4-applied-ai-system "Grading Rubric") to understand exactly how your project will be evaluated, including required features and optional stretch challenges worth extra points.



### ⚙️ Project Requirements

Your final project is about taking what you've already built and making it stronger, smarter, and more reliable. You'll extend one of your previous projects (from Modules 1-3) into a complete applied AI system.

**💡 Example Extensions**

|   |   |
| - | - |
|   |   |
|   |   |
|   |   |
|   |   |



**0. Preparing Your Project Environment**

Because this project is an evolution of your earlier work, you should create a dedicated copy of your chosen repo. This allows you to experiment freely without altering your original Module 1-3 submission.

- Go to GitHub and create a new, public repo.
  - Name it something professional, like `applied-ai-system-project`.
  - Do **not** initialize it with a README, license, or `.gitignore`. Keep it completely empty.
  - Copy the URL of this new repo (e.g., `https://github.com/username/applied-ai-system-final.git`)
- Clone your original repo into a new folder on your computer:
  - `git clone https://github.com/username/your-original-repo.git applied-ai-system-final`
  - Enter the folder: `cd applied-ai-system-final`
- Update the remote to point to your new repo:
  - `git remote set-url origin https://github.com/username/applied-ai-system-final.git`
- Push everything to your new repo:
  - `git push -u origin main`
  **Note:** If your default branch is named `master` instead of `main`, use `git push -u origin master`.
- Verify the connection: go to your new repo on GitHub and confirm your code and commit history are there.

Before you begin coding, set up a professional folder structure in your new repo.

- Create a folder in your project called `assets`. This will be your dedicated directory for your system architecture images.
- Create a folder called `diagrams`. Your architecture diagram **must** be saved as a Mermaid source file (e.g., `diagrams/architecture.mmd`) — a `.mmd` file or a `.md` file containing a Mermaid code block. A PNG image alone is not sufficient.
- If you are using the Mermaid Live Editor to preview your diagram, copy the source text into your `.mmd` file before exporting. You may also export a PNG for embedding in the README, but **the source file is required.**

After you clone down and navigate to your new cloned repo, remember to create and initialize your project venv. See the [Tool Setup page](https://courses.codepath.org/courses/ai110/pages/ide_setup.md) for the full environment guide.

#### Create a virtual environment if you don't already have one

Navigate to your new cloned repo:

`python3 -m venv .venv`

- Activate the virtual environment:

**BASH/ZSH commands for MacOS, Git Bash on Windows, or WSL**

`source .venv/bin/activate`

**Windows PowerShell** (note the backslashes, not forward slashes)

`.\.venv\Scripts\Activate.ps1`

#### Install dependencies

```
python -m pip install --upgrade pip
pip install -r requirements.txt

```



**1. Functionality: What Your System Should Do**

Your project should **do something useful with AI**. For example:

- Summarize text or documents
- Retrieve information or data from a source
- Plan and complete a step-by-step task
- Help debug, classify, or explain something

To make your project more advanced, it must include **at least one** of the following AI features:

| **Feature**                              | **What It Means**                                                    | **Example**                                                               |
| ---------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **Retrieval-Augmented Generation (RAG)** | Your AI looks up or retrieves information before answering.          | A study bot that searches notes before generating a quiz question.        |
| **Agentic Workflow**                     | Your AI can plan, act, and check its own work.                       | A coding assistant that writes, tests, and then fixes code automatically. |
| **Fine-Tuned or Specialized Model**      | You use a model that’s been trained or adjusted for a specific task. | A chatbot tuned to respond in a company’s tone of voice.                  |
| **Reliability or Testing System**        | You include ways to measure or test how well your AI performs.       | A script that checks if your AI gives consistent answers.                 |

The feature should be fully integrated into the main application logic. It is not enough to have standalone script; the feature must meaningfully change how the system behaves or processes information. For example, if you add RAG, your AI should actively use the retrieved data to formulate its response rather than just printing the data alongside a standard answer.

Also, make sure your project:

- **Runs correctly and reproducibly:** If someone follows your instructions, it should work.
- **Includes logging or guardrails:** Your code should track what it does and handle errors safely.
- **Has clear setup steps:** Someone else should be able to run it without guessing what to install.



**2. Design and Architecture: How Your System Fits Together**

Show how your project is organized by creating a short **system diagram**. Your diagram should include:

- The **main components** (like retriever, agent, evaluator, or tester).
- How **data flows** through the system (input, then process, then output).
- Where **humans or testing** are involved in checking AI results.

Submit your diagram as a Mermaid source file (`.mmd`) or a Markdown (`.md`) file containing Mermaid syntax — do not submit it only as a screenshot or image. This lets the diagram's structure be read directly from the source.



**3. Documentation: How You Explain Your Work**

You'll write a **README file** that clearly explains your project. It should include:

- Explicitly name your original project (from Modules 1-3) and provide a 2-3 sentence summary of its original goals and capabilities.
- **Title and Summary:** What your project does and why it matters.
- **Architecture Overview:** A short explanation of your system diagram.
- **Setup Instructions:** Step-by-step directions to run your code.
- **Sample Interactions:** Include at least 2-3 examples of inputs and the resulting AI outputs to demonstrate the system is functional.
- **Design Decisions:** Why you built it this way, and what trade-offs you made.
- **Testing Summary:** What worked, what didn't, and what you learned.
- **Reflection:** A brief note on what this project taught you about AI and problem-solving. Your **graded** responsible-AI reflection — how you collaborated with AI, one suggestion you accepted and one you rejected or revised, and your system's limitations — goes in `model_card.md` (see Step 5), **not** here. Reflection content placed only in the README does not earn the reflection points.

Write this for a future employer who might look at your GitHub portfolio! Clarity and completeness matter more than perfection.



**4. Reliability and Evaluation: How You Test and Improve Your AI**

Your AI should **prove that it works**, not just seem like it does. Include **at least one way** to test or measure its reliability, such as:

- Automated tests (e.g., unit tests or simple checks for key functions).
- Confidence scoring (the AI rates how sure it is).
- Logging and error handling (your code records what failed and why).
- Human evaluation (you or a peer review the AI's output).

Summarize your testing in a few lines, like:

> 5 out of 6 tests passed; the AI struggled when context was missing. Confidence scores averaged 0.8; accuracy improved after adding validation rules.

**If you use human evaluation,** document it in a parseable format such as a markdown table or structured text/JSON so your results can be read without watching a demo. For example:

| **Test Input**           | **Evaluation Criteria**   | **Result**     |
| ------------------------ | ------------------------- | -------------- |
| "Summarize this article" | Accurate, under 100 words | Pass           |
| Empty input              | Handles gracefully        | Fail — crashed |

Put evaluation tables or structured test logs in `README.md` or `model_card.md`; keep them text-based and parseable, not screenshots



**5. Reflection and Ethics: Thinking Critically About Your AI**

AI isn't just about what works -- it's about what's responsible. Document your reflection in `model_card.md` under clearly labeled section headers, answering the following questions:

- What are the limitations or biases in your system?
- Could your AI be misused, and how would you prevent that?
- What surprised you while testing your AI's reliability?
- describe your collaboration with AI during this project. Identify one suggestion you accepted and one you did not accept as written, and say why you rejected or changed it. It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for your system all count. If nothing the AI suggested was outright wrong, look for one you still changed: shortened, simplified, renamed, or scoped down. That counts.



**🚀 Optional: Stretch Features for Extra Points**

These features are **completely optional** and go beyond the required 21 points. Completing them can earn up to **+8 additional points**, allowing your score to exceed 100%. See the [**Grading Rubric**](https://courses.codepath.org/courses/ai110/pages/grading#heading-project-4-applied-ai-system "Grading Rubric") for how each is evaluated.

| **Feature**                           | **What To Build**                                                                                                                                                                                                                             | **Points** |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| **RAG Enhancement**                   | Extend your retrieval system to use custom documents or multiple data sources. Document the improvement in your `README.md` or `model_card.md` — a before/after example or a short written description of how retrieval improved your output. | +2         |
| **Agentic Workflow Enhancement**      | Implement multi-step reasoning with tool-calls, planning steps, or a decision-making chain. Save the intermediate reasoning traces to `ai_interactions.md` (embed them, or link a committed log file from it).                                | +2         |
| **Fine-Tuning or Specialization**     | Demonstrate specialized model behavior using few-shot patterns, synthetic datasets, or constrained tone/style. Show that output measurably differs from the baseline.                                                                         | +2         |
| **Test Harness or Evaluation Script** | Build a script that runs your system on a set of predefined inputs and prints a summary (pass/fail scores, confidence ratings, or similar).                                                                                                   | +2         |

**Note:** These stretch features build directly on the required AI feature you chose in Step 1. For example, if you added RAG as your required feature, the RAG Enhancement stretch would extend that same component further.



**6. Presentation and Portfolio: Sharing Your Work Professionally**

You'll wrap up by sharing your final project.

- Prepare a 5-7 minute presentation showing your system, demo, and what you learned.
- Add a portfolio artifact:
  - A GitHub link to your code
  - A short reflection paragraph: *What this project says about me as an AI engineer.*
- **Include reproducible execution evidence in your README (required):** So your system can be graded without watching a video, your `README.md` must include, in markdown (code blocks or generated `.txt` logs):
  - Sample command executions
  - Example inputs
  - Example outputs
  - Reliability/guardrail results
- **Record a Loom video walkthrough (optional, for human reviewers):** A short walkthrough showing your system running end-to-end is encouraged for human reviewers. To record, we recommend using [Loom](https://www.loom.com/). Include the link in your README. Grading is based on the text-based evidence above, not the video.

**[IMPORTANT]**

To receive an accurate grade, make sure your **text-based execution evidence** in the README clearly demonstrates:

- ✅ End-to-end system run (2–3 inputs)
- ✅ AI feature behavior (RAG, agent, etc.)
- ✅ Reliability/guardrail or evaluation behavior
- ✅ Clear outputs for each case

If you include a Loom video, it does **not** need to show code setup, file structure, or installation steps.

If you are unsure about including something, consult the [Grading Rubric](https://courses.codepath.org/courses/ai110/pages/grading#heading-project-4-applied-ai-system "Grading Rubric").



### 📬 Submitting Your Project

Once you've completed all the required features for your project, use the following checklist to prepare your work for submission.

1. Code is pushed to the correct GitHub repository
2. Repo is public
3. **Required files are present:** You must include your runnable functional code, a comprehensive `README.md`, a `model_card.md` for reflections, and a System Architecture Diagram saved as a Mermaid source file (`.mmd` or `.md` with Mermaid code block) in a `diagrams/` folder.
4. **Reproducible Execution Evidence:** Instead of demo screenshots, include reproducible command outputs or interaction logs in markdown or `.txt` files. Your diagram source file and any optional supplementary images should be stored in dedicated `/assets` or `/diagrams` folders.
5. Commit history shows multiple meaningful commits
6. **Standardized Documentation:** Your `README.md` must identify your base project, and your `model_card.md` must answer all reflection prompts regarding AI collaboration, biases, and testing results.
7. **Demo evidence is included:** Your `README.md` contains at least 2-3 example inputs with their outputs pasted as fenced code blocks that demonstrate your system's behavior without relying on a video. A Loom walkthrough is optional but helpful for human reviewers; if you include one, add the link to your README.
8. Final changes are committed and pushed before the deadline

---

# Appendix B — Full grading rubric supplied by Alex

### Project 4: Applied AI System

Total Points: **21pts** + 8pts bonus

**Required Features**

| **3pts** | **Clear Identification of the Base Project and Its Original Scope** |
| -------- | ------------------------------------------------------------------ |
| 1 | Student identifies the original project they are extending. |
| 1 | Student provides a short description of the original system's goal and capabilities. |
| 1 | Description is accurate and sets clear context for extensions. |

| **3pts** | **Substantial New AI Feature Added (RAG, Agent, Specialization, or Reliability Mechanism)** |
| -------- | --------------------------------------------------------------------------------------- |
| 1 | Student adds at least one substantial AI feature such as RAG, a multi-step agent or planning workflow, specialized behavior (mini fine-tune or structured prompting), or a reliability harness (evaluation loop, guardrails, self-checking). |
| 1 | Feature is integrated into the working system (not an isolated demo). |
| 1 | Feature is functional and produces meaningful changes in system behavior. |

| **3pts** | **System Architecture Diagram** |
| -------- | ------------------------------- |
| 1 | Architecture diagram is submitted as a Mermaid source file (.mmd or embedded in a .md file); a PNG image alone is not sufficient. |
| 1 | Diagram clearly illustrates data flow (input, then processing steps, then output). |
| 1 | Diagram matches actual project implementation (not theoretical). |

| **3pts** | **Functional End-to-End System Demonstration** |
| -------- | -------------------------------------------- |
| 1 | Student provides a working script or UI that demonstrates full system workflow. |
| 1 | README includes example commands and sample outputs in code blocks showing the system running end-to-end. |
| 1 | System responds consistently to at least 2-3 example inputs. |

| **3pts** | **Reliability, Evaluation, or Guardrail Component** |
| -------- | ------------------------------------------------- |
| 1 | System includes a reliability mechanism such as input validation, output guardrails, self-critique or multi-model agreement, or an evaluation script that tests sample inputs. |
| 1 | Mechanism is functional and meaningfully improves reliability. |
| 1 | Student provides examples in markdown format (showing input, behavior, and result) demonstrating how the guardrail or evaluator behaves. |

| **3pts** | **Documentation: README and Setup Instructions** |
| -------- | ----------------------------------------------- |
| 1 | README clearly explains project goals and new features. |
| 1 | README contains step-by-step instructions to install, run, and test the system. |
| 1 | README includes sample input/output illustrating system behavior. |

| **3pts** | **Reflection on AI Collaboration and System Design** |
| -------- | --------------------------------------------------- |
| 1 | Student explains how they used AI during development (prompting, debugging, design). |
| 1 | Student identifies at least one AI suggestion they accepted and at least one they rejected or revised. |
| 1 | Student reflects on system limitations and future improvements. |

**Stretch Features**

| **+2pts** | **RAG Enhancement: Custom Indexing or Multi-Source Retrieval** |
| --------- | ------------------------------------------------------------ |
| | Retrieval is extended to include custom documents, sections, or multi-source retrieval. |
| | `README.md` or `model_card.md` documents the impact on output quality (a before/after example or a written description of how retrieval improved the results). |

| **+2pts** | **Agentic Workflow Enhancement** |
| --------- | -------------------------------- |
| | Multi-step reasoning with tool-calls, planning steps, or a decision-making chain is implemented. |
| | The agent's intermediate reasoning traces are saved in `ai_interactions.md` (embedded, or via a committed log file linked from it), not just printed to terminal. |

| **+2pts** | **Fine-Tuning or Specialization Behavior** |
| --------- | ----------------------------------------- |
| | Specialized model behavior (few-shot patterns, synthetic datasets, or constrained tone/style) is demonstrated. |
| | `model_card.md` includes a comparison of baseline vs. specialized output showing measurable differences. |

| **+2pts** | **Test Harness or Evaluation Script** |
| --------- | ------------------------------------ |
| | A script that evaluates the system on multiple predefined inputs is built and runs successfully. |
| | The script prints a summary of results (pass/fail score, confidence, or similar). |

---

End of source appendices. Start with the read-only inspection and project-option discussion specified above. Do not implement an unselected project or automatically pursue stretch features.
