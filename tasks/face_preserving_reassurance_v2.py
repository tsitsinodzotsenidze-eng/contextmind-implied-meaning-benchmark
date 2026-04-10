import textwrap
import re
import kaggle_benchmarks as kbench


def extract_choice(response: str):
    if not response:
        return None

    text = response.strip()

    # 1) Boxed answer
    m = re.search(r"\\boxed\{([A-D])\}", text, re.IGNORECASE)
    if m:
        return m.group(1).upper()

    # 2) Very explicit answer phrases
    explicit_patterns = [
        r"the main communicative function(?: of this statement)?\s+is\s+([A-D])\b",
        r"the communicative function(?: of this statement)?\s+is\s+([A-D])\b",
        r"(?:final answer|correct answer|the answer|answer)\s*[:\-]?\s*([A-D])\b",
        r"(?:the best answer|best answer)\s*[:\-]?\s*([A-D])\b",
    ]

    for p in explicit_patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1).upper()

    # 3) Letter followed by the full option text
    option_patterns = [
        r"\b([A-D])\s*[\.\):-]\s*face-preserving reassurance\b",
        r"\b([A-D])\s*[\.\):-]\s*genuine reassurance\b",
        r"\b([A-D])\s*[\.\):-]\s*strategic warning\b",
        r"\b([A-D])\s*[\.\):-]\s*neutral procedural clarification\b",
    ]

    for p in option_patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1).upper()

    # 4) Conservative fallback: last answer-like line only
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    tail = "\n".join(lines[-5:])

    m = re.search(
        r"(?:answer|final answer|correct answer|best answer)[^\n]{0,20}\b([A-D])\b",
        tail,
        re.IGNORECASE,
    )
    if m:
        return m.group(1).upper()

    return None


CASES = [
    {
        "prompt": textwrap.dedent("""
        A larger financial institution delays a joint implementation with Meridian Bank after speculation begins to focus on Meridian’s internal controls.

        It states:

        "We continue to regard Meridian Bank as a valued and credible partner. The current adjustment to the implementation timeline should not be read as singling out Meridian, but as a responsible governance step taken while internal alignment processes continue on both sides. Our intention is to avoid encouraging speculation that would attach disproportionate meaning to a routine implementation pause."

        What is the main communicative function of this statement?

        A. Neutral procedural clarification
        B. Face-preserving reassurance
        C. Genuine reassurance
        D. Strategic warning
        """).strip(),
        "answer": "B",
    },
    {
        "prompt": textwrap.dedent("""
        During a border-coordination process, unforeseen verification steps trigger domestic commentary suggesting that the visiting delegation was not properly prepared.

        Officials say:

        "We appreciate the professionalism demonstrated by all parties throughout the border coordination process. The additional verification steps arose from our own standard sequencing requirements and should not be taken to reflect on the delegation’s preparedness. We recognize that such speculation can be unhelpful, and a brief administrative pause is the most appropriate way to avoid drawing external counterparts into a domestic discussion not of their making."

        What is the main communicative function of this statement?

        A. Strategic warning
        B. Neutral procedural clarification
        C. Face-preserving reassurance
        D. Genuine reassurance
        """).strip(),
        "answer": "C",
    },
    {
        "prompt": textwrap.dedent("""
        A donor institution reviews disbursement conditions after parliamentary scrutiny creates pressure on the recipient country’s implementing authorities.

        Its message reads:

        "We recognize the considerable efforts made by the implementing authorities under challenging structural conditions. The current review of disbursement conditions forms part of our routine portfolio management process and is intended to provide space for the existing questions to be addressed without casting the ministry in the position of being publicly corrected by an external partner. We remain committed to working constructively with your team on a mutually agreed path forward."

        What is the main communicative function of this statement?

        A. Face-preserving reassurance
        B. Neutral procedural clarification
        C. Strategic warning
        D. Genuine reassurance
        """).strip(),
        "answer": "A",
    },
    {
        "prompt": textwrap.dedent("""
        A university pauses a joint academic program after controversy over governance leaves the partner institution exposed to awkward public commentary.

        The statement says:

        "We wish to reaffirm our deep respect for the partner university’s academic standing and the quality of its faculty. The present pause is not intended to cast doubt on the institution’s credibility, but to ensure that the partnership does not become a vehicle for reputational judgments while internal questions are being settled. Our aim is to avoid placing the institution in an unfairly exposed position during a period of heightened scrutiny."

        What is the main communicative function of this statement?

        A. Genuine reassurance
        B. Strategic warning
        C. Neutral procedural clarification
        D. Face-preserving reassurance
        """).strip(),
        "answer": "D",
    },
    {
        "prompt": textwrap.dedent("""
        A firm hears rumors that an upcoming compliance review means it has been singled out for unusual scrutiny.

        The regulator responds:

        "We wish to assure Cascade Holdings that the forthcoming review of its operational compliance frameworks forms part of a sector-wide assessment initiative and should not be interpreted as a sign that the company has been marked out for any particular concern. The purpose is to preserve consistency across the review process while avoiding unnecessary conclusions about the standing of any individual participant. We value your continued cooperation."

        What is the main communicative function of this statement?

        A. Neutral procedural clarification
        B. Genuine reassurance
        C. Face-preserving reassurance
        D. Strategic warning
        """).strip(),
        "answer": "C",
    },
    {
        "prompt": textwrap.dedent("""
        A ministry postpones contract renewal with a supplier after journalists begin implying that the supplier’s recent performance has been unsatisfactory.

        The ministry states:

        "We wish to thank Vantage Supplies for their continued dedication throughout our partnership. The postponement of contract renewal reflects internal budgetary realignment and should be understood as a temporary administrative measure, rather than any assessment of Vantage Supplies’ performance or standing as a valued partner. Our aim is to avoid attaching undue significance to what is, in substance, a routine timing adjustment."

        What is the main communicative function of this statement?

        A. Strategic warning
        B. Face-preserving reassurance
        C. Neutral procedural clarification
        D. Genuine reassurance
        """).strip(),
        "answer": "B",
    },
    {
        "prompt": textwrap.dedent("""
        Two delegations complete a difficult round of trade talks in which visible disagreement emerges during the discussions and is quickly amplified in domestic commentary.

        The communiqué reads:

        "Both delegations reaffirm their shared commitment to a deepened and mutually beneficial trade relationship. While differences of emphasis naturally arose during the talks, neither side sees value in allowing those exchanges to harden into narratives of diminished confidence or diplomatic imbalance. Both sides remain focused on the practical areas of convergence established during the round."

        What is the main communicative function of this statement?

        A. Face-preserving reassurance
        B. Genuine reassurance
        C. Neutral procedural clarification
        D. Strategic warning
        """).strip(),
        "answer": "A",
    },
    {
        "prompt": textwrap.dedent("""
        A multinational reduces the role of a smaller supplier while trying not to humiliate it in front of other regional partners.

        It writes:

        "This volume adjustment should not be understood as a judgment on your broader reliability. Under current conditions, a modest rebalancing helps us maintain continuity while avoiding the kind of visibility that can unfairly attach disproportionate meaning to a temporary operational issue. Our intention is to prevent a limited adjustment from being read by others as a broader signal about your standing in the network."

        What is the main communicative function of this statement?

        A. Genuine reassurance
        B. Face-preserving reassurance
        C. Strategic warning
        D. Neutral procedural clarification
        """).strip(),
        "answer": "B",
    },
    {
        "prompt": textwrap.dedent("""
        A company moves a senior manager out of a visible negotiating role after a difficult public episode and announces the change internally in carefully positive language.

        The memo says:

        "We are pleased to announce that David will be transitioning to the newly created position of Senior Advisor for Strategic Initiatives, a role that will allow him to bring his extensive institutional knowledge to bear across a broader range of organizational priorities. We are grateful for David’s exceptional contributions and look forward to the value he will bring in this expanded capacity. The change is intended to prevent a situationally difficult episode from being given a personal interpretation that would not reflect his standing in the organization."

        What is the main communicative function of this statement?

        A. Genuine reassurance
        B. Face-preserving reassurance
        C. Neutral procedural clarification
        D. Strategic warning
        """).strip(),
        "answer": "B",
    },
    {
        "prompt": textwrap.dedent("""
        At a multilateral economic forum, a visible disagreement during a panel risks making one or more delegations appear diminished within the forum.

        Organizers later say:

        "Participants acknowledged the diversity of perspectives represented at the forum and expressed appreciation for the open and substantive exchange of views during the session. All parties reaffirmed their commitment to continued dialogue and to the shared objectives that form the foundation of this multilateral framework. The intention is to ensure that differences of emphasis are not taken as reflections on any delegation’s standing within the forum."

        What is the main communicative function of this statement?

        A. Strategic warning
        B. Neutral procedural clarification
        C. Face-preserving reassurance
        D. Genuine reassurance
        """).strip(),
        "answer": "C",
    },
]


@kbench.task(
    name="face_preserving_reassurance_v2",
    description="Identify when a statement presented as reassurance is actually designed to preserve face, soften tension, or manage concern without offering full direct clarity."
)
def face_preserving_reassurance_v2(llm):
    for i, case in enumerate(CASES, start=1):
        response = llm.prompt(case["prompt"])
        pred = extract_choice(response)
        assert pred == case["answer"], (
            f"Case {i} failed. Expected {case['answer']}, got {pred}. "
            f"Raw response: {response}"
        )
