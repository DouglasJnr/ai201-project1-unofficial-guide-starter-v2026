# The Unofficial Guide

# Douglas Tanyanyiwa Corpus: City_Guides
---

# Unit 1

## What This Does

For this Aassignment I picked the City_Guides corpus which covers information about towns in a region. My sytstem answersa range of practical, location-specific questions such as public transit, restaurant operating hours, accessibility of local towns and regional lookups spanning multiple locations.Rather than relyin on general knowledge, it retrieves relevant passages from the corpus and answers strictly based on that grounded context. If the syste cannot retrieve any or enough relevant information to answer the questions  it states so, meaning questions outside of the city context will not have answers provided.. 

## Chunking Strategy

**Chunk size: 325**

**Overlap: 1 sentence(final sentence of each chunk is repeatd as the opening of the next), rather than a fixed character count.**

My documents are long sectioned guides as opposed to short posts.Therefore I decided to implement a target range for my chunk size (250-400 characters) for my chunk size with a hard ceiling of 700 characters which only triggers if a single paragraph/sentence exceeds this because I'm using paragraph/sentence split as opposed to a hard-cut character count. This then led me to use the last sentence of the previous chunk as overlap as opposed to n characters of overlap.
My decision to use these metrics is because of the criteria I used and the nature of the documents. Most answers may be found in a thought window of approximately 2-3 sentences, but to ensure my criteria would be met and without the trade-off of potentially sacrificing a complete thought, or not getting an answer from the pre-determined document to satisy criteria 5.


## Sample Chunks


**Chunk 1** — source: guide_accessibility.md#0 `` — produced by: chunker.py::split_documents ``

```
# Getting around the region with limited mobility An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance. ## Straightforward **Thornby Wells** is the easiest town in the region. It is flat, compact, and
everything is within three minutes of everything else. Parking is free for two
hours anywhere in town and the station is central.
```

**Chunk 2** — source: guide_corry_vale.md#5 `` — produced by: chunker.py::split_documents ``

```
## Where to stay Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else. ## When to go May to September.
```

**Chunk 3** — source: guide_givens_mill.md#2 `` — produced by: chunker.py::split_documents ``

```
## Eat and drink A tearoom attached to the mill, open 10 to 4 daily except Tuesdays, which sells bread made from the flour ground twenty metres away and is the reason most people come. One pub, food served lunchtimes and Thursday to Saturday evenings.
```

**Chunk 4** — source: guide_marchwood.md#0 `` — produced by: chunker.py::split_documents ``

```
# Marchwood Marchwood is the regional hub — 180,000 people, the junction everyone changes trains at, and a city most visitors pass through rather than stop in. That is a mistake, though an understandable one, since almost nothing of interest is near the station.
```

**Chunk 5** — source: guide_regional_transport.md#4 `` — produced by: chunker.py::split_documents ``

```
The Kestrelford approach is single-track with passing places
for the final eight minutes. The Halden Bay coast road is cut into the cliff
and is slow rather than difficult. Parking is the constraint rather than driving. Both Halden Bay lots fill by
10am on summer weekends. Kestrelford's lower car park is free and involves a
steep walk up.
```

## Sample Answer

**Question: Answer using only the information in the documents below. If they don't cover it, say you don't have enough information.What are the business operation hours where I can buy food to eat outside Matchwood?**

**Answer: Based on the provided documents, food options and their hours outside of Marchwood include:

* **Elder Ness:** One pub serves food from 12 to 2 and 6 to 8, and is closed on Mondays. A shop sells basics and closes at 5pm and all day Sunday. (*guide_elder_ness.md*)
* **Corry Vale:** One pub in the largest village serves food seven days a week, and a second pub opens Thursday to Sunday. A farm shop closes at 4pm. (*guide_corry_vale.md*)
* **Kestrelford:** Pubs serve food between 12 and 2 and again between 6 and 8:30 (there is nowhere to eat outside these windows). A bakery sells out by 11am. (*guide_kestrelford.md* and *guide_eating.md*)
* **General Region:** Outside Marchwood, kitchens across the region stop serving at 9pm and often earlier. (*guide_eating.md*)** 

```
Sources retrieved: guide_corry_vale.md, guide_eating.md, guide_elder_ness.md, guide_kestrelford.md, guide_marchwood.md
```

**My relevance cutoff: 0.6**

| Question | In corpus? | Best distance |
|---|---|---|
|What is the bus service like in Kestrelford throughout the week? | YES | 0.372 | 
|What are the business operation hours where I can buy food to eat outside Matchwood? | YES | 0.431 |
|What is the accessibility of Thornby Wells? | YES | 0.389 |
|When is it cheapest to book tickets when traveling by railway| YES  | 0.592 |
|Which town(s) in the region has a hospital? | YES  | 0.429 |
|What bus terminals are there in Silicon Valley | NO | 0.665 |
|How do I change the oil in a diesel engine?| NO | 0.876 |
|Who won the 1994 World Cup?| NO | 0.997 |
|What is the recommended dosage of ibuprofen for a headache?| NO | 0.841 |
|How do I write a for loop in Rust?    | NO   | 0.861 |

## How I Used AI

**1. I asked Claude to write help me implement a chunking function that split the documents by paragraphs using a designated character window, including the 1 sentence overlap. It produced a chunk character window that was too wide and I had to correct it.**

**2. I used Claude to analyze and deliberate my chunk size and overlap for the chunker. It lost context for my criterion and I had to adjust the feedback it gave me to ensure that my chunking function would meet my criteria.  **

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
