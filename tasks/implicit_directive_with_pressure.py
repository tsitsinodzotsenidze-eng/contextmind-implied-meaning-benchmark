import textwrap
import re
import kaggle_benchmarks as kbench


def extract_choice(response):
    if not response:
        return None

    text = str(response).strip()

    # 1) boxed answers like \boxed{B}
    m = re.search(r'\\boxed\{([A-D])\}', text, flags=re.IGNORECASE)
    if m:
        return m.group(1).upper()

    # 2) explicit answer phrases
    patterns = [
        r'final answer\s*[:\-]?\s*([A-D])\b',
        r'answer\s*[:\-]?\s*([A-D])\b',
        r'the correct answer is\s*([A-D])\b',
        r'i choose\s*([A-D])\b',
        r'i pick\s*([A-D])\b',
        r'my answer is\s*([A-D])\b',
    ]
    for pattern in patterns:
        m = re.search(pattern, text, flags=re.IGNORECASE)
        if m:
            return m.group(1).upper()

    # 3) fallback: last standalone A-D near the end
    tail = text[-200:]
    matches = re.findall(r'\b([A-D])\b', tail, flags=re.IGNORECASE)
    if matches:
        return matches[-1].upper()

    return None


@kbench.task(
    name="implicit_directive_with_pressure",
    description="Identify when a seemingly neutral or cooperative geoeconomic statement functions as an implicit directive backed by pressure to comply."
)
def implicit_directive_with_pressure(llm) -> None:
    cases = [
        {
            "prompt": textwrap.dedent("""
                Read the context and statement carefully. Then choose the option (A, B, C, or D)
                that best captures the statement's pragmatic force.

                Context:
                A regional trade official is speaking to firms that rely on imported industrial components.

                Statement:
                "Companies may wish to align their sourcing plans with the ministry's resilience framework
                if they expect licensing discussions to proceed without unnecessary delay."

                Question:
                What is the most accurate reading of this statement?

                A. A neutral reminder about routine licensing timelines
                B. A softened instruction backed by procedural pressure
                C. A diplomatic warning about future consequences without telling firms what to do
                D. A reassurance that different sourcing plans will be treated the same

                Answer with only A, B, C, or D.
            """),
            "answer": "B",
        },
        {
            "prompt": textwrap.dedent("""
                Read the context and statement carefully. Then choose the option (A, B, C, or D)
                that best captures the statement's pragmatic force.

                Context:
                A customs authority comments on a new compliance procedure for exporters.

                Statement:
                "Exporters are, of course, free to organize documentation as they see fit.
                Those who follow the recommended filing sequence, however, are unlikely to encounter review complications."

                Question:
                What is the most accurate reading of this statement?

                A. A friendly reassurance meant only to reduce exporter anxiety
                B. A purely descriptive note about how documents are processed
                C. A vague statement with no real push toward any behavior
                D. A pressure-backed nudge toward the recommended procedure

                Answer with only A, B, C, or D.
            """),
            "answer": "D",
        },
        {
            "prompt": textwrap.dedent("""
                Read the context and statement carefully. Then choose the option (A, B, C, or D)
                that best captures the statement's pragmatic force.

                Context:
                A ministry spokesperson announces a timeline for updating industrial certification forms.

                Statement:
                "The revised certification portal will open on Monday, and firms will receive the updated template by email."

                Question:
                What is the most accurate reading of this statement?

                A. A straightforward administrative communication
                B. A softened effort to steer firms toward compliance
                C. A diplomatic signal that firms may face sanctions
                D. A cooperative message masking an unstated competitive threat

                Answer with only A, B, C, or D.
            """),
            "answer": "A",
        },
        {
            "prompt": textwrap.dedent("""
                Read the context and statement carefully. Then choose the option (A, B, C, or D)
                that best captures the statement's pragmatic force.

                Context:
                A transport regulator addresses firms seeking priority access to a logistics corridor.

                Statement:
                "Applicants who want their corridor requests considered favorably should take care
                to reflect national continuity priorities in their revised submissions."

                Question:
                What is the most accurate reading of this statement?

                A. A reassurance that corridor access decisions are fully neutral
                B. A clarification of how the corridor system is geographically organized
                C. A softened directive tied to favorable review
                D. A warning about retaliation without a suggested course of action

                Answer with only A, B, C, or D.
            """),
            "answer": "C",
        },
        {
            "prompt": textwrap.dedent("""
                Read the context and statement carefully. Then choose the option (A, B, C, or D)
                that best captures the statement's pragmatic force.

                Context:
                A deputy industry minister is addressing firms applying to join a strategic supplier program.

                Statement:
                "Firms seeking expedited entry into the supplier program may wish to ensure that their
                upcoming partnership disclosures are fully aligned with the ministry's resilience priorities."

                Question:
                What is the most accurate reading of this statement?

                A. A routine clarification about how partnership disclosures are filed
                B. A softened instruction tied to process advantage
                C. A diplomatic warning about future penalties without directing conduct
                D. A reassurance that current partnership disclosures are already satisfactory

                Answer with only A, B, C, or D.
            """),
            "answer": "B",
        },
        {
            "prompt": textwrap.dedent("""
                Read the context and statement carefully. Then choose the option (A, B, C, or D)
                that best captures the statement's pragmatic force.

                Context:
                A development agency is speaking to contractors bidding for public infrastructure projects.

                Statement:
                "Bidders may structure proposals as they choose, though submissions that closely follow
                the agency's preferred localization model will naturally move more efficiently through review."

                Question:
                What is the most accurate reading of this statement?

                A. A neutral note about how the review software sorts files
                B. A reassurance that all proposal formats are equally welcome
                C. A vague formulation that avoids signaling any real preference
                D. A softened push toward compliance backed by review pressure

                Answer with only A, B, C, or D.
            """),
            "answer": "D",
        },
        {
            "prompt": textwrap.dedent("""
                Read the context and statement carefully. Then choose the option (A, B, C, or D)
                that best captures the statement's pragmatic force.

                Context:
                A regional coordinator concludes a meeting on cross-border industrial cooperation.

                Statement:
                "We appreciate today's constructive exchange and remain committed to continued practical
                cooperation through regular technical consultations in the months ahead."

                Question:
                What is the most accurate reading of this statement?

                A. Genuine cooperative reassurance
                B. A subtle attempt to push counterparts toward policy alignment
                C. A warning that relations may worsen without concessions
                D. A notice about upcoming implementation deadlines

                Answer with only A, B, C, or D.
            """),
            "answer": "A",
        },
        {
            "prompt": textwrap.dedent("""
                Read the context and statement carefully. Then choose the option (A, B, C, or D)
                that best captures the statement's pragmatic force.

                Context:
                A national procurement office addresses suppliers seeking long-term framework contracts.

                Statement:
                "Suppliers interested in remaining under active consideration would be well advised
                to revise sourcing plans in line with the resilience guidance circulated last quarter."

                Question:
                What is the most accurate reading of this statement?

                A. A historical reference to last quarter's guidance memo
                B. A reassurance that current sourcing plans are already acceptable
                C. A softened instruction reinforced by selection pressure
                D. A vague signal with no real behavioral push

                Answer with only A, B, C, or D.
            """),
            "answer": "C",
        },
        {
            "prompt": textwrap.dedent("""
                Read the context and statement carefully. Then choose the option (A, B, C, or D)
                that best captures the statement's pragmatic force.

                Context:
                A port administration publishes a notice about maintenance work.

                Statement:
                "Berths 3 and 4 will be unavailable from Tuesday to Thursday due to scheduled maintenance."

                Question:
                What is the most accurate reading of this statement?

                A. A pressure-backed attempt to redirect operator behavior
                B. A diplomatic warning aimed at foreign shipping firms
                C. A cooperative reassurance meant to soften hidden pressure
                D. A straightforward operational notice

                Answer with only A, B, C, or D.
            """),
            "answer": "D",
        },
        {
            "prompt": textwrap.dedent("""
                Read the context and statement carefully. Then choose the option (A, B, C, or D)
                that best captures the statement's pragmatic force.

                Context:
                A senior industry official comments on applications for semiconductor-equipment partnerships.

                Statement:
                "Firms seeking a smooth authorization process may find it useful to demonstrate, early on,
                that their partnerships reflect the strategic orientation set out in the ministry's latest guidance."

                Question:
                What is the most accurate reading of this statement?

                A. A reassurance that authorization will proceed automatically
                B. A softened instruction tied to a smoother approval process
                C. A note about where the ministry's guidance can be found
                D. A warning about punishment that offers no behavioral nudge

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
