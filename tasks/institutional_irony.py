import textwrap
import re
import kaggle_benchmarks as kbench

def extract_choice(response):
    response = response.strip()

    boxed = re.findall(r"\\boxed\{([A-D])\}", response)
    if boxed:
        return boxed[-1]

    explicit_patterns = [
        r"(?:final answer|answer is|correct answer is)\s*[:\-]?\s*([A-D])\b",
        r"^\s*([A-D])\s*$",
    ]
    for pattern in explicit_patterns:
        matches = re.findall(pattern, response, flags=re.IGNORECASE | re.MULTILINE)
        if matches:
            return matches[-1].upper()

    tail = response[-200:]
    matches = re.findall(r"\b([A-D])\b", tail)
    if matches:
        return matches[-1].upper()

    return None


@kbench.task(
    name="institutional_irony",
    description="Detect when formally approving economic or policy language actually conveys criticism through institutional irony rather than sincere praise, neutral reporting, or direct accusation."
)
def institutional_irony(llm) -> None:
    cases = [
        {
            "prompt": textwrap.dedent("""
                Context: Tariff predictability

                Statement:
                "The ministry has again demonstrated its commitment to tariff predictability; by implementation week, importers had become remarkably efficient at updating their assumptions about the final rate."

                Question:
                What is the speaker most likely implying?

                A. The speaker sincerely praises the ministry for communicating tariffs in a stable and predictable way.
                B. The speaker ironically criticizes the ministry for instability that repeatedly forces firms to revise expectations.
                C. The speaker warns that the ministry is preparing a punitive tariff shock for importers.
                D. The speaker neutrally observes that firms are becoming better at scenario planning during reform.

                Answer with only A, B, C, or D.
            """),
            "answer": "B",
        },
        {
            "prompt": textwrap.dedent("""
                Context: Procurement transparency

                Statement:
                "It is reassuring to see the procurement portal continue setting high transparency standards by publishing contract data several months after the goods have already been delivered."

                Question:
                What is the speaker most likely implying?

                A. The speaker acknowledges that publication timing is imperfect but sees the portal as genuinely improving institutional transparency over time.
                B. The speaker is making a technical point that contract data publication cycles are constrained by administrative processing requirements rather than by any lack of commitment to openness.
                C. The speaker ironically criticizes an institution for calling delayed disclosure transparency.
                D. The speaker implies that delayed disclosure has become normalized to the point where procurement actors no longer treat timely publication as a meaningful standard.

                Answer with only A, B, C, or D.
            """),
            "answer": "C",
        },
        {
            "prompt": textwrap.dedent("""
                Context: Customs streamlining

                Statement:
                "The customs authority deserves credit for streamlining border procedures; traders now know exactly which additional form will appear after the previous one has been resubmitted."

                Question:
                What is the speaker most likely implying?

                A. The speaker ironically suggests that the process remains bureaucratic and inefficient despite being presented as streamlined reform.
                B. The speaker sincerely credits the authority for making border procedures more predictable and easier for traders to navigate.
                C. The speaker implies that the sequencing of forms reflects a deliberate administrative logic that traders are gradually learning to work with efficiently.
                D. The speaker acknowledges that the reform has not eliminated complexity but sees the increased predictability of requirements as a genuine operational improvement for traders.

                Answer with only A, B, C, or D.
            """),
            "answer": "A",
        },
        {
            "prompt": textwrap.dedent("""
                Context: Subsidy review process

                Statement:
                "The subsidy review process has clearly protected market neutrality: only firms with long-standing access to the ministry seem to understand how to apply correctly."

                Question:
                What is the speaker most likely implying?

                A. The speaker suggests that experienced firms are naturally better positioned to navigate complex application systems, which can still be consistent with a neutral process.
                B. The speaker is making a practical observation that repeated participation tends to improve administrative accuracy, without necessarily implying unfairness.
                C. The speaker ironically criticizes a supposedly neutral process that appears institutionally biased.
                D. The speaker implies that firms outside the network are likely to remain disadvantaged even when the process is formally described as neutral.

                Answer with only A, B, C, or D.
            """),
            "answer": "C",
        },
        {
            "prompt": textwrap.dedent("""
                Context: Regulatory clarification

                Statement:
                "Investors will no doubt welcome the regulator's latest clarification, especially those still working through the previous clarification issued last week."

                Question:
                What is the speaker most likely implying?

                A. The speaker suggests that repeated clarification can still be a genuine sign of regulatory responsiveness when markets are adjusting quickly.
                B. The speaker ironically criticizes the regulator for generating confusion instead of clarity.
                C. The speaker is making a neutral observation that investors who engaged with earlier guidance are now better positioned to interpret the latest regulatory update.
                D. The speaker is making a technical observation that frequent clarifications are a normal feature of complex regulatory implementation.

                Answer with only A, B, C, or D.
            """),
            "answer": "B",
        },
        {
            "prompt": textwrap.dedent("""
                Context: Port modernization

                Statement:
                "The port modernization plan appears to be moving with admirable urgency; even the temporary detours have now acquired a semi-permanent character."

                Question:
                What is the speaker most likely implying?

                A. The speaker suggests that the authorities deserve credit for adapting flexibly to project delays through durable contingency arrangements.
                B. The speaker is making a neutral observation that temporary infrastructure adjustments often last longer than initially expected in projects of this scale.
                C. The speaker ironically criticizes slow or stalled implementation being framed as urgent reform.
                D. The speaker implies that the detours have created a new long-term transport pattern that may ultimately prove more efficient than the original plan.

                Answer with only A, B, C, or D.
            """),
            "answer": "C",
        },
        {
            "prompt": textwrap.dedent("""
                Context: Competition authority

                Statement:
                "The competition authority has again demonstrated its independence by discovering, after extensive review, that the market leader's dominance remains entirely coincidental."

                Question:
                What is the speaker most likely implying?

                A. The speaker suggests that the authority's lengthy review lends credibility to its conclusion, even if the result remains controversial.
                B. The speaker ironically questions the credibility and independence of the authority's finding.
                C. The speaker implies that the authority's analysis may be technically narrow, but not necessarily politically compromised.
                D. The speaker suggests that stronger intervention may still become necessary if market conditions worsen.

                Answer with only A, B, C, or D.
            """),
            "answer": "B",
        },
        {
            "prompt": textwrap.dedent("""
                Context: Emergency liquidity facility

                Statement:
                "The emergency liquidity facility has been a model of equal access, with support arriving fastest for institutions that somehow seemed prepared for the announcement in advance."

                Question:
                What is the speaker most likely implying?

                A. The speaker ironically suggests that access may not have been equally fair in practice.
                B. The speaker implies that some institutions were operationally better prepared, but without necessarily questioning the fairness of the facility itself.
                C. The speaker is making a technical observation that unequal processing speed can occur even in formally equal emergency mechanisms.
                D. The speaker suggests that the facility's announcement may have been communicated unevenly, creating the appearance of preferential readiness.

                Answer with only A, B, C, or D.
            """),
            "answer": "A",
        },
        {
            "prompt": textwrap.dedent("""
                Context: Export licensing platform

                Statement:
                "It is encouraging that the export licensing platform now gives applicants a single dashboard from which they may monitor, with admirable precision, the continued movement of their requests between pending categories."

                Question:
                What is the speaker most likely implying?

                A. The speaker suggests that applicants now benefit from clearer digital visibility into an otherwise complex but functioning licensing workflow.
                B. The speaker ironically criticizes a system that is technologically polished in form but still unresponsive in substance.
                C. The speaker implies that licensing officials are intentionally keeping requests in motionless categories to delay approvals without formal rejection.
                D. The speaker is making a technical point that better dashboard design has improved category tracking even where underlying case complexity remains high.

                Answer with only A, B, C, or D.
            """),
            "answer": "B",
        },
        {
            "prompt": textwrap.dedent("""
                Context: Fiscal accountability report

                Statement:
                "The fiscal council's latest report should finally settle concerns about accountability, particularly since the missing annexes leave so much room for public trust."

                Question:
                What is the speaker most likely implying?

                A. The speaker suggests that the report still represents a meaningful step toward accountability, even if some supporting material has not yet been included.
                B. The speaker is making a narrow observation that incomplete annex publication can occur without undermining the report’s broader institutional value.
                C. The speaker ironically criticizes the gap between accountability claims and incomplete disclosure.
                D. The speaker implies that the omitted annexes are likely to contain politically damaging material that authorities are intentionally concealing.

                Answer with only A, B, C, or D.
            """),
            "answer": "C",
        },
    ]

    for i, case in enumerate(cases, start=1):
        response = llm.prompt(case["prompt"])
        pred = extract_choice(response)

        assert pred == case["answer"], (
            f"Item {i} failed. Expected {case['answer']}, got {pred}. "
            f"Raw response: {response}"
        )
