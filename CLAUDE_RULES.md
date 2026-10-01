# NeuroLearn Permanent Development Rules

These rules apply to all future NeuroLearn work unless the user explicitly changes them.

## Scope and Workflow

1. Build NeuroLearn incrementally. Complete and verify one phase before starting another.
2. Do not build the entire application in one step.
3. Before modifying an important file, inspect the current workspace and the file's existing contents.
4. Preserve working code. Make focused, minimal changes.
5. Never delete existing files without explicit approval.
6. Never rewrite the whole project unnecessarily.
7. Do not create duplicate components, routes, services, or configuration files unless there is a clear reason.
8. Do not continue to a later development phase automatically. Wait for the user's next command.

## Technology and Cost

9. Prefer free, open-source, and local technologies.
10. Do not add paid APIs or paid services.
11. Do not require OpenAI, Gemini, or any other external AI API.
12. Do not add cloud infrastructure unless the user explicitly requests it and the decision is reviewed first.
13. Keep the first version runnable on the local computer.
14. Do not install packages that are not needed for the current approved phase.

## Code Quality and Beginner Friendliness

15. Use clear names and straightforward code.
16. Match the style and conventions of the surrounding code.
17. Explain unfamiliar React, JavaScript, Python, FastAPI, database, API, and computer-vision concepts in beginner-friendly language.
18. Avoid over-engineering. Choose the simplest design that works and can be tested.
19. Keep frontend, backend, database, computer-vision, and scheduling responsibilities separated without adding unnecessary abstraction.
20. Add tests and documentation as features are introduced.
21. Report verification results honestly, including failures and skipped checks.

## Privacy and Security

22. Keep secrets, passwords, tokens, and API keys out of source code and version control.
23. Use environment/configuration files only for local values, and provide safe examples rather than real secrets.
24. Do not store raw webcam video.
25. Request webcam permission explicitly and process frames locally whenever possible.
26. Discard camera frames after extracting the needed signals whenever practical.
27. Handle camera denial, unavailable hardware, and missing computer-vision data gracefully.
28. Store only the minimum data needed for the product and explain what is stored.
29. Do not describe NeuroLearn as a medical diagnostic system.
30. Present fatigue results as approximate study-productivity signals, with limitations clearly communicated.

## Collaboration and Change Safety

31. Inspect before editing and verify after each meaningful change.
32. Do not overwrite user work.
33. Do not assume that an installed package, service, or tool is available without checking it.
34. Use Git when the repository is initialized; do not commit secrets, local databases, webcam data, virtual environments, or build output.
35. Update `NEUROLEARN_DEVELOPMENT_PLAN.md` when the approved architecture, status, or development phases change.
36. If requirements are ambiguous or a choice could significantly affect the project, explain the choice and ask before proceeding.
