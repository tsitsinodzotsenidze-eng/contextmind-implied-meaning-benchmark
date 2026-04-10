import textwrap
import re
import kaggle_benchmarks as kbench


def extract_choice(response: str):
    if not response:
        return None

    # 1) Prefer boxed answers
    m = re.search(r"\\boxed\{([A-D])\}", response, re.IGNORECASE)
    if m:
        return m.group(1).upper()

    # 2) Explicit final-answer phrases
    patterns = [
        r"(?:final answer|correct answer|the answer is|best answer is)\s*[:\-]?\s*([A-D])\b",
        r"(?:I choose|I select|I'd choose|my answer is)\s*[:\-]?\s*([A-D])\b",
    ]
    for p in patterns:
        m = re.search(p, response, re.IGNORECASE)
        if m:
            return m.group(1).upper()

    # 3) Fallback: last standalone A-D near the end
    tail = response[-250:]
    matches = re.findall(r"\b([A-D])\b", tail, re.IGNORECASE)
    if matches:
        return matches[-1].upper()

    return None


@kbench.task(
    name="implicit_strategic_warning",
    description="Identify softly expressed geoeconomic warnings that are framed as advice or caution rather than direct threat."
)
def implicit_strategic_warning(llm) -> None:
    cases = [
        {
            "prompt": textwrap.dedent("""
                Context: Sanctions

                Statement:
                "In the current environment, partners may wish to review their cross-border exposure with particular care."

                Question:
                What concern is being indirectly signaled here?

                A. Partners that maintain current ties will face immediate penalties.
                B. Partners are being gently advised to reconsider ties before regulatory consequences widen.
                C. Partners are mainly being cautioned about reputational discomfort from public association.
                D. The statement is simply offering routine, neutral advice about prudent international operations.

                Answer with only A, B, C, or D.
            """),
            "answer": "B",
        },
        {
            "prompt": textwrap.dedent("""
                Context: Export controls

                Statement:
                "Member firms may benefit from renewed due diligence when evaluating transactions in sensitive categories."

                Question:
                What concern is being indirectly signaled here?

                A. Member firms are being warned that transactions in these categories may soon invite immediate formal restrictions.
                B. Member firms are being cautioned that public association with such transactions may become reputationally uncomfortable.
                C. Member firms are being warned that scrutiny around sensitive transactions is increasing.
                D. Member firms are being encouraged to strengthen internal review practices as a matter of prudent governance, not because the external scrutiny environment is materially changing.
                Answer with only A, B, C, or D.
            """),
            "answer": "C",
        },
        {
            "prompt": textwrap.dedent("""
                Context: Semiconductor restrictions

                Statement:
                "Companies planning multi-year production cycles may wish to avoid assuming uninterrupted availability of advanced-node inputs."

                Question:
                What concern is being indirectly signaled here?

                A. Companies are being warned that access to advanced-node inputs may become less predictable, so long-term planning should not rely on continuity.
                B. Companies are being warned that purchases of advanced-node inputs will soon be completely prohibited.
                C. Companies are mainly being cautioned that involvement with advanced-node supply chains could become politically embarrassing.
                D. Companies are being encouraged to build sourcing flexibility simply as a matter of prudent planning in a volatile but otherwise normal environment.

                Answer with only A, B, C, or D.
            """),
            "answer": "A",
        },
        {
            "prompt": textwrap.dedent("""
                Context: Shipping / maritime corridor

                Statement:
                "Exporters with time-sensitive deliveries may wish to avoid building near-term planning assumptions around uninterrupted corridor reliability."

                Question:
                What concern is being indirectly signaled here?

                A. Exporters are being warned that transit disruptions across the corridor are now certain and immediate.
                B. Exporters are being cautioned that visible use of the corridor may create reputational discomfort with foreign partners.
                C. Exporters are being advised to add modest contingency buffers as a matter of prudent logistics, even though route dependability remains broadly stable.
                D. Exporters are being warned that corridor dependability may no longer be stable enough to anchor planning with confidence, so continuity should not be assumed.

                Answer with only A, B, C, or D.
            """),
            "answer": "D",
        },
        {
            "prompt": textwrap.dedent("""
                Context: Energy dependency

                Statement:
                "Large industrial users may want to revisit procurement plans that assume uninterrupted external energy supply through the coming season."

                Question:
                What concern is being indirectly signaled here?

                A. The message points to an imminent and formally announced cutoff in external energy supply.
                B. The statement quietly warns that continued access to external energy supply may be less secure than current planning assumptions suggest, so stability should not be taken for granted.
                C. The real concern is mostly reputational: firms that rely heavily on external energy could appear politically exposed.
                D. This is mainly a reminder to diversify procurement for efficiency reasons, while the broader supply framework is still expected to remain dependable.

                Answer with only A, B, C, or D.
            """),
            "answer": "B",
        },
        {
            "prompt": textwrap.dedent("""
                Context: Investment screening

                Statement:
                "Cross-border investors looking at acquisitions in sensitive sectors would do well to build extra time and uncertainty into transaction planning."

                Question:
                What concern is being indirectly signaled here?

                A. The message indicates that acquisitions in sensitive sectors are already destined to be rejected.
                B. The main concern is reputational: investors may appear politically exposed if they pursue these deals.
                C. The statement is quietly warning that approval in sensitive sectors may no longer be routine, so transactions should not be planned as if clearance were automatic.
                D. This is mostly a practical reminder about paperwork and scheduling, while the review outcome itself is still expected to follow the usual path.

                Answer with only A, B, C, or D.
            """),
            "answer": "C",
        },
        {
            "prompt": textwrap.dedent("""
                Context: Dual-use technology transfer

                Statement:
                "Institutions engaged in technical cooperation may wish to revisit the end-use assumptions behind existing transfer arrangements before extending them further."

                Question:
                What concern is being indirectly signaled here?

                A. The statement quietly warns that earlier assumptions about how transferred technology will ultimately be used may no longer be reliable enough, so end-use needs closer rechecking.
                B. The message indicates that dual-use technical cooperation is about to be broadly and formally prohibited.
                C. The real concern is mainly reputational: institutions involved in such cooperation could appear politically compromised.
                D. This is mostly a routine governance reminder to review documentation, while the underlying end-use assumptions themselves are still broadly sound.

                Answer with only A, B, C, or D.
            """),
            "answer": "A",
        },
        {
            "prompt": textwrap.dedent("""
                Context: Sovereign debt / lender pressure

                Statement:
                "Borrowers approaching refinancing windows may want to allow for a less accommodating external funding environment when setting near-term expectations."

                Question:
                What concern is being indirectly signaled here?

                A. The statement indicates that external lenders are about to suspend support altogether.
                B. The real concern is mostly reputational: borrowers may look politically vulnerable if they seek outside funding.
                C. This is mainly a reminder to update financing models, while still assuming lenders will remain available on broadly familiar terms.
                D. The statement quietly warns that refinancing conditions may no longer be as accommodating as borrowers expect, so future funding should not be planned as if lenient terms were assured.

                Answer with only A, B, C, or D.
            """),
            "answer": "D",
        },
        {
            "prompt": textwrap.dedent("""
                Context: Critical minerals

                Statement:
                "Producers dependent on critical mineral inputs may find it prudent to re-examine sourcing plans that assume replacement suppliers can be secured without significant delay."

                Question:
                What concern is being indirectly signaled here?

                A. The message indicates that replacement supplies of critical minerals are about to disappear altogether.
                B. The statement quietly warns that substitute sources for critical minerals may be harder and slower to secure than current planning assumes, so supply flexibility should not be treated as assured.
                C. The main issue is reputational: firms tied to critical mineral sourcing may appear politically exposed.
                D. This is mostly a routine reminder to improve procurement efficiency, while the broader assumption of easy supplier substitution still remains sound.

                Answer with only A, B, C, or D.
            """),
            "answer": "B",
        },
        {
            "prompt": textwrap.dedent("""
                Context: Supply-chain relocation

                Statement:
                "Firms pursuing rapid supply-chain relocation may want to be cautious about treating resilience gains as something that can be secured on a near-term timetable."

                Question:
                What concern is being indirectly signaled here?

                A. The statement implies that supply-chain relocation is about to fail outright and should be abandoned.
                B. The deeper issue is mainly reputational: firms that relocate too quickly may appear politically exposed.
                C. The statement quietly warns that relocation may involve more friction, delay, and adjustment costs than current planning assumes, so resilience should not be treated as quickly achievable.
                D. This is mostly a general reminder to manage transition carefully, while the expected benefits of relocation are still likely to arrive on roughly the planned schedule.

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
