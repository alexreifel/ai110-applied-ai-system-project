# Portfolio draft — requires Alex review

Repository: [ai110-applied-ai-system-project](https://github.com/alexreifel/ai110-applied-ai-system-project). Its identity and public visibility were verified during this work. The final local audit and evidence are in docs/final_audit.md; publication and actual remote CI results are recorded at delivery. Do not publish this draft elsewhere automatically.

## Project summary

Music Discovery Assistant extends my CodePath music recommender into a Python and Streamlit application over 1,200 real independent tracks. It combines an implemented Gemini preference-interpreter adapter with editable preference review, deterministic ranking, source-backed explanations, and checks for unsupported conditions. A reproducible evaluation harness exercises 12 predefined requests, and 174 automated tests pass in two local environments. The browser workflow and offline tests are verified; live Gemini behavior and the generic-versus-specialized prompt comparison still need validation with usable access.

## Reflection paragraph for Alex's review

I wanted the AI to add something useful: translating how someone describes music into preferences the recommender can evaluate. I rejected the guessing-game coach because binary search doesn't need repeated LLM calls, and I pushed to expand the music data before putting an assistant over it. That decision shaped the project. A flexible interface means little if the catalog can't support the request or if the system quietly ignores an exclusion. I used Codex to help implement and test the system, with a focus on making its assumptions and limits visible.

This paragraph draws on Alex's actual decisions in the chat. Alex should confirm the wording. His actual observation during final review was that the recommendations were diverse and most songs were unfamiliar, which he associated with expanding the dataset. It does not claim independent authorship, a successful live model run, listening satisfaction, delivered presentation, or an awarded grade. Update the status sentence only when the corresponding live/publication evidence exists.
