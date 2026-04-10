import re
import textwrap
import kaggle_benchmarks as kbench


def extract_choice(response: str) -> str:
    """
    Robustly extract a multiple-choice answer (A/B/C/D) from model output.
    Priority:
    1) \\boxed{A-D}
    2) explicit final-answer phrases
    3) last standalone A-D near the end
    """
    if response is None:
        return ""

    text = response.strip()

    patterns = [
        r"\\boxed\{\s*([A-D])\s*\}",
        r"(?i)(?:final answer|answer|correct answer|best answer)\s*[:\-]?\s*([A-D])\b",
        r"(?i)\boption\s*([A-D])\b",
        r"\b([A-D])\b(?=[^A-D]*$)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).upper()

    return ""


@kbench.task(
    name="strategic_ambiguity",
    description="Identify the strategic function served by ambiguity in geoeconomic and policy statements."
)
def strategic_ambiguity(llm) -> None:
    cases = [
        {
            "prompt": textwrap.dedent("""
                Task: Strategic ambiguity in geoeconomic and policy statements.
                Identify the strategic function served by the ambiguity in the statement below.

                Context: Foreign investment screening

                Statement:
                "We regularly review whether the current framework provides adequate protection for long-term national capabilities."

                Question:
                What strategic function does the ambiguity in this statement primarily serve?

                A. To reassure foreign investors that the existing framework is unlikely to change in substance
                B. To frame the issue as one of protecting national capabilities while leaving open the possibility of tighter screening later
                C. To suggest that the current framework may face closer scrutiny because of emerging strategic vulnerabilities
                D. To imply that any future tightening would likely be targeted at especially sensitive sectors rather than applied broadly

                Answer with only A, B, C, or D.
            """),
            "answer": "B",
        },
        {
            "prompt": textwrap.dedent("""
                Task: Strategic ambiguity in geoeconomic and policy statements.
                Identify the strategic function served by the ambiguity in the statement below.

                Context: Tariff retaliation

                Statement:
                "We will take whatever steps are necessary to defend our economic position under current conditions."

                Question:
                What strategic function does the ambiguity in this statement primarily serve?

                A. To project resolve while preserving flexibility over the form and timing of any response
                B. To portray any eventual response as protective of national interests rather than openly punitive
                C. To suggest that retaliation has now become more likely than continued negotiation
                D. To imply that specific sector-based countermeasures have already been chosen internally

                Answer with only A, B, C, or D.
            """),
            "answer": "A",
        },
        {
            "prompt": textwrap.dedent("""
                Task: Strategic ambiguity in geoeconomic and policy statements.
                Identify the strategic function served by the ambiguity in the statement below.

                Context: Energy dependency

                Statement:
                "Energy security requires a balanced approach that takes account of resilience, affordability, and existing partnerships."

                Question:
                What strategic function does the ambiguity in this statement primarily serve?

                A. To make any future diversification appear compatible with preserving workable ties to the current supplier
                B. To keep resilience, affordability, and existing partnerships all in play without revealing which priority will ultimately drive supplier policy
                C. To justify continued dependence on the current supplier mainly on affordability grounds
                D. To suggest that a timetable for replacing the supplier already exists but has not yet been disclosed

                Answer with only A, B, C, or D.
            """),
            "answer": "B",
        },
        {
            "prompt": textwrap.dedent("""
                Task: Strategic ambiguity in geoeconomic and policy statements.
                Identify the strategic function served by the ambiguity in the statement below.

                Context: Emergency industrial support

                Statement:
                "We remain attentive to the needs of strategically significant sectors as market conditions continue to evolve."

                Question:
                What strategic function does the ambiguity in this statement primarily serve?

                A. To signal that the government is monitoring pressure on strategically important sectors without promising any immediate support
                B. To leave open the possibility that targeted assistance could be considered later if import pressure worsens significantly
                C. To imply that ordinary policy tools may still be viewed as sufficient for the moment
                D. To shift the discussion from a direct yes-or-no answer on emergency aid toward broad evolving market conditions, thereby avoiding a concrete commitment

                Answer with only A, B, C, or D.
            """),
            "answer": "D",
        },
        {
            "prompt": textwrap.dedent("""
                Task: Strategic ambiguity in geoeconomic and policy statements.
                Identify the strategic function served by the ambiguity in the statement below.

                Context: Regional trade bloc

                Statement:
                "Any future engagement will be assessed in light of our broader economic priorities and long-term strategic interests."

                Question:
                What strategic function does the ambiguity in this statement primarily serve?

                A. To signal that participation remains under consideration, but only if it can be aligned with domestic economic priorities
                B. To preserve room across competing economic alignments by avoiding a commitment that could alienate either current or potential partners
                C. To suggest that participation is unlikely unless the bloc offers substantially more favorable terms
                D. To imply that the government has already moved the issue into an advanced internal decision phase without saying so directly

                Answer with only A, B, C, or D.
            """),
            "answer": "B",
        },
        {
            "prompt": textwrap.dedent("""
                Task: Strategic ambiguity in geoeconomic and policy statements.
                Identify the strategic function served by the ambiguity in the statement below.

                Context: Logistics infrastructure access

                Statement:
                "Infrastructure policy must reflect both openness to commerce and the protection of essential national capacities."

                Question:
                What strategic function does the ambiguity in this statement primarily serve?

                A. To suggest that openness to commerce will remain the default position unless specific security concerns justify narrower restrictions
                B. To reassure commercial actors that any safeguards under consideration would be limited rather than broadly exclusionary
                C. To shift the discussion to broad governing principles while leaving any specific future restrictions undefined
                D. To imply that the government is already moving toward a more selective screening approach for certain operators without specifying who they are

                Answer with only A, B, C, or D.
            """),
            "answer": "C",
        },
        {
            "prompt": textwrap.dedent("""
                Task: Strategic ambiguity in geoeconomic and policy statements.
                Identify the strategic function served by the ambiguity in the statement below.

                Context: Semiconductor export licensing

                Statement:
                "Licensing decisions will continue to reflect the broader security environment and the need to protect critical technological ecosystems."

                Question:
                What strategic function does the ambiguity in this statement primarily serve?

                A. To suggest that any near-term licensing changes would likely be gradual rather than immediate or sweeping
                B. To frame possible future tightening as a security-based policy choice without specifying which products, firms, or thresholds could trigger it
                C. To imply that any future licensing adjustments would be calibrated in coordination with trusted partners rather than driven by unilateral commercial considerations
                D. To indicate that future licensing decisions may rely more heavily on case-by-case scrutiny of selected actors without committing to a defined control mechanism

                Answer with only A, B, C, or D.
            """),
            "answer": "B",
        },
        {
            "prompt": textwrap.dedent("""
                Task: Strategic ambiguity in geoeconomic and policy statements.
                Identify the strategic function served by the ambiguity in the statement below.

                Context: Telecom infrastructure tenders

                Statement:
                "Participation decisions will be guided by resilience, reliability, and the long-term integrity of nationally significant networks."

                Question:
                What strategic function does the ambiguity in this statement primarily serve?

                A. To suggest that vendor eligibility will continue to depend mainly on technical performance rather than geopolitical considerations
                B. To imply that a confidential list of disfavored vendors has already been prepared for the next tender round
                C. To recast a potentially geopolitical exclusion decision as a standards-based evaluation without specifying which firms or criteria might trigger exclusion
                D. To reassure market participants that any future restrictions would likely be limited to the most security-sensitive contracts rather than applied broadly

                Answer with only A, B, C, or D.
            """),
            "answer": "C",
        },
        {
            "prompt": textwrap.dedent("""
                Task: Strategic ambiguity in geoeconomic and policy statements.
                Identify the strategic function served by the ambiguity in the statement below.

                Context: Cross-border settlement alternatives

                Statement:
                "Financial continuity requires settlement architecture that can remain adaptable under changing external conditions."

                Question:
                What strategic function does the ambiguity in this statement primarily serve?

                A. To hint at contingency planning for alternative settlement channels without openly declaring a shift away from the current route
                B. To signal that financial continuity is the government’s primary concern rather than any deliberate shift in geopolitical alignment
                C. To suggest that any adaptation would be pursued through multilateral coordination rather than a unilateral departure from the current settlement route
                D. To avoid publicly assigning responsibility for the vulnerability to any specific external actor while keeping the discussion at a general institutional level

                Answer with only A, B, C, or D.
            """),
            "answer": "A",
        },
        {
            "prompt": textwrap.dedent("""
                Task: Strategic ambiguity in geoeconomic and policy statements.
                Identify the strategic function served by the ambiguity in the statement below.

                Context: Grain import diversification

                Statement:
                "Food security is best protected by maintaining diversified sourcing options consistent with long-term national stability."

                Question:
                What strategic function does the ambiguity in this statement primarily serve?

                A. To reassure domestic markets that any adjustment in grain sourcing would be guided by supply stability rather than abrupt political retaliation
                B. To justify possible diversification away from the supplier without openly committing to an immediate reduction in imports
                C. To signal that the government is already in advanced talks with alternative suppliers to replace the current import arrangement
                D. To imply that import volumes will be reduced gradually rather than through any immediate or publicly announced policy shift

                Answer with only A, B, C, or D.
            """),
            "answer": "B",
        },
    ]

    for i, case in enumerate(cases, start=1):
        response = llm.prompt(case["prompt"])
        pred = extract_choice(response)

        assert pred == case["answer"], (
            f"Item {i} failed. Expected {case['answer']}, got {pred}. "
            f"Raw response: {response}"
        )
