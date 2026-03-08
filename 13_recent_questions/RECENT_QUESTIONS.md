# Recently Reported Amazon Interview Questions

Questions that people have reported seeing in recent Amazon coding interviews (Jan–Mar 2026). Data sourced from 1point3acres, Glassdoor, and programhelp. Use this to prioritize your prep.

---

## BREAKING: Amazon Changed Their OA Format (Jan 22, 2026)

Amazon SDEs now use Gen AI tools like Amazon Q, Cline, and Kiro daily for writing/documenting code, debugging, refactoring, and testing. Amazon has reimagined its technical assessments to mirror how engineers actually work. **Candidates can now work with an interactive AI assistant on the coding platform during the assessment**, while still being evaluated on their distinct skills.

- 87% of candidates reported that the new coding questions effectively relate to the role they're pursuing.
- Amazon also uses AI-powered real-time transcription during interviews, with 83% of candidates reporting more engaging interactions.
- **The OA is changing — you may be given an AI assistant to use during coding, and they're watching how you use it, not just if you can code.**

---

## Coding Questions — Last 3 Weeks (Jan–Mar 2026, 1point3acres verified)

| Problem | LC # | Pattern | Difficulty | Source | How Recent |
|---------|------|---------|------------|--------|------------|
| Analyzing One-Time Visitors | — | HashMap / Frequency | Easy–Med | 1p3a Phone Screen | ~5 days ago |
| Word Break II | 140 | DP / Backtracking | Hard | 1p3a VO | ~10 days ago |
| Morse Code variant | 804 (variant) | String / HashMap | Easy–Med | 1p3a VO | ~10 days ago |
| Merge Sorted Arrays | — | Two Pointer | Easy | 1p3a VO | ~10 days ago |
| EC2 Instance Allocation Cost | — | Greedy / Sorting | Medium | 1p3a OA | ~12 days ago |
| Frequent Item Pair | — | HashMap / Nested Counting | Easy–Med | 1p3a OA | ~12 days ago |
| Refactoring Modules / Min Days Scheduling | — | BFS / Binary Search | Med–Hard | 1p3a OA | ~12 days ago |
| Deep Copy Linked List w/ Random Pointer | 138 | Linked List | Medium | 1p3a | ~19 days ago |
| Next Greater Element / Monotonic Stack | — | Stack | Medium | 1p3a | ~19 days ago |
| Merge K Sorted Lists | 23 | Heap / Divide & Conquer | Hard | 1p3a | Yes |
| Server Security Level Grouping | — | Greedy / Frequency | Medium | programhelp OA | Dec 2025 |
| Max Bandwidth w/ Primary-Secondary Pairing | — | Greedy | Medium | programhelp OA | Dec 2025 |

*Note: A candidate reported getting "Merge 3 Lists" which is a variant of Merge K Sorted Lists (LC 23) with k=3.*

### Details on Specific Interviews

**~5 days ago — SWE Intern Tech Phone Screen**
- "Analyzing One-Time Visitors" — given user visit logs, find users who visited only once, then figure out how to target them with promotional offers. Classic HashMap/frequency counting problem with follow-up requirements.

**~10 days ago — SDE Intern VO (Video Interview)**
- Morse Code — likely a variant of Unique Morse Code Words (LC #804) or a harder encoding/decoding problem
- Word Break II (LC #140) — given a string and a dictionary, return all ways to break the string into valid dictionary words. Hard DP/backtracking problem.

**~12 days ago — SDE Intern OA**
- EC2 allocation = greedy/sorting problem (minimize cost to allocate server instances to tasks)
- Frequent item pair = find the most common pair of items that appear together (HashMap + nested counting)

**~12 days ago — OA Coding Questions**
- Module refactoring and release schedules — find the minimum number of days to complete all releases under given constraints. Scheduling/BFS or binary search on answer problem.

**~19 days ago — SDE Intern Interview**
- Deep Copy of a Linked List with Random Pointer (LC #138) and a Next Greater Element / Monotonic Stack problem, with optimization discussion.

---

## GenAI Interview Questions (NEW in 2026)

There is now reportedly a **dedicated Gen AI round** appearing in some SDE 1 interviews (confirmed by 1p3a post tagged "SDE 1 Interview Experience 2026 with DSA and Gen AI Rounds", posted ~1 day ago).

65% of employers now ask about AI tools and adaptability skills when evaluating candidates in 2026.

### Questions Being Asked

| Question | Context |
|----------|---------|
| How do you use generative AI? | Multiple reports, very common |
| What's your favorite prompt when you get stuck? | Reported across tech interviews |
| What have you built using AI tools recently? | Reported across tech interviews |
| How have you used AI tools (Copilot, ChatGPT, etc.) in a project? | SDE interviews |
| Describe a time AI helped you debug or write code faster — what did you verify yourself? | SDE interviews |
| What are the risks of using AI-generated code in production? | SDE interviews |
| How would you use Amazon Q or Bedrock to solve [X problem]? | Amazon-specific |

### How to Prep

- Have a real, specific example of using AI tools in your workflow
- Highlight continuous learning and your methodology for adopting new tools
- You don't need to be an ML expert, but you need AI literacy
- Amazon is actively building GenAI into both their assessments and their culture

---

## Behavioral / LP Questions — Reported Recently (Last 2–3 Weeks)

### Ownership
| Question |
|----------|
| Tell me about a time you took on a project outside your normal responsibilities |
| Tell me about a time you saw a problem and fixed it without being asked |

### Bias for Action
| Question |
|----------|
| Tell me about a time you had to make a decision without having all the information you needed |
| Describe a time you had to choose between moving forward vs. waiting to finish something perfectly |
| *Behavioral questions on decision-making and deadlines — specifically around what you do when a deadline is at risk* |

### Deliver Results
| Question |
|----------|
| Tell me about a time you failed to meet a deadline. What happened and what did you do? |
| Give an example of when you set a goal and had to overcome obstacles to achieve it |

### Customer Obsession
| Question |
|----------|
| Tell me about a time you went out of your way for a user/customer/teammate |
| Describe a project where you had to understand your end user deeply |

### Learn and Be Curious (maps directly to GenAI questions)
| Question |
|----------|
| What's a new technology or tool you've recently taught yourself? How did you apply it? |
| How do you stay current with changes in the industry? *(GenAI use is a perfect answer here)* |

### Earn Trust / Disagree and Commit
| Question |
|----------|
| Tell me about a time you disagreed with a teammate or manager. How did you handle it? |

### Dive Deep
| Question |
|----------|
| Walk me through a complex technical problem you solved. How did you debug it step by step? |

---

*Add new entries as you hear about them. Keep this list updated to focus on high-probability questions.*
