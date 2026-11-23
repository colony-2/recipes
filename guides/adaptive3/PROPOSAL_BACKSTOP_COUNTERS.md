# Proposed Adaptive3 retry rules

## 1. Phase attempts reset on reentry

Count work attempts, consultations, child-job rounds, and package retries within the current phase visit. Retries during that visit continue the count. Every entry from another phase starts the destination’s counters at zero. For example, if Direction uses all four attempts and Backstop sends it back to revise the plan, Direction gets four fresh attempts and retains its earlier work.

## 2. A new human instruction resets all retry counters

Wherever the instruction arrives, reset phase and merge retry counts to zero and restore both Backstop returns **before the next decision**. Apply this once per instruction. A reviewer saying “put the switcher in the About menu” during Preparation triggers the reset there. Passing those same words on to Direction carries the instruction forward without triggering a second reset.

## 3. Confirmed progress restores both Backstop returns

Backstop starts with two automatic returns. Spend one when it sends work to a phase with an instruction. Considering several destinations costs nothing. On the next visit, Backstop keeps the remaining allowance unless the job has made confirmed progress or received a new human instruction. If another return is needed with zero left, Backstop asks the human for guidance.

A **progress checkpoint** records evidence that the job has newly satisfied a requirement, such as approval of a revised plan or a previously failing acceptance check passing. Each new checkpoint restores both Backstop returns. A phase transition or a new commit alone earns no reset. Count each checkpoint once per human instruction, even if the job repeats a check. Show the evidence and the allowance change together in the chapter trace.

**Example.** Verification finds checks A and B failing. Backstop sends the job to Implementation, leaving one return. If A now passes and B still fails, the trace records “Check A passed on verification. Backstop returns increased from one to two.” If both still fail, one return remains. Backstop can use it to try another correction without involving the reviewer.
