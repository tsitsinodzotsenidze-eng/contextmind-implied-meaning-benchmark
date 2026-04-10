import textwrap
import re
import kaggle_benchmarks as kbench


def extract_choice(response: str) -> str:
    response = response.strip()

    # 1) Prefer boxed answers if present
    m = re.search(r"\\boxed\{([A-D])\}", response)
    if m:
        return m.group(1)

    # 2) Explicit final-answer phrasings
    patterns = [
        r"(?:final answer|answer)\s*[:\-]?\s*([A-D])\b",
        r"(?:the correct answer is|the answer is)\s*([A-D])\b",
        r"(?:I choose|I pick|I select)\s*([A-D])\b",
    ]
    for pat in patterns:
        m = re.search(pat, response, flags=re.IGNORECASE)
        if m:
            return m.group(1).upper()

    # 3) Last standalone A-D near the end
    tail = response[-200:]
    matches = re.findall(r"\b([A-D])\b", tail)
    if matches:
        return matches[-1]

    # 4) Fallback: anywhere in response
    matches = re.findall(r"\b([A-D])\b", response)
    if matches:
        return matches[-1]

    raise AssertionError(f"Could not extract answer choice from response: {response}")


@kbench.task(
    name="procedural_distancing",
    description="Identify when institutional or regulatory language uses procedure, sequencing, or review processes to avoid taking a direct substantive position."
)
def procedural_distancing(llm) -> None:
    cases = [
        {
            "prompt": textwrap.dedent("""
                Context:
                A ministry spokesperson is asked whether the government will reverse a recently announced customs measure that has drawn criticism from importers.

                Statement:
                "At this stage, the matter remains under interagency review, and any adjustment would need to follow the established consultative process."

                Question:
                What is the most likely implied function of this statement?

                A. It indicates that the government is preserving a formal pathway for revision rather than ruling it out outright.
                B. It shifts attention to procedure in order to avoid giving a direct commitment or taking immediate responsibility for the decision.
                C. It suggests that comment is being deferred until technical agencies complete a substantive evaluation of the measure's economic effects.
                D. It reassures importers that their concerns are being actively addressed within the proper institutional framework.

                Answer with only A, B, C, or D.
            """),
            "answer": "B",
        },
        {
            "prompt": textwrap.dedent("""
                Context:
                A central bank official is asked whether recent exchange-rate volatility will trigger an emergency market intervention.

                Statement:
                "Any response would need to be assessed within the Bank's established analytical framework and in light of its medium-term price stability mandate."

                Question:
                What is the most likely implied function of this statement?

                A. It indicates that any intervention would have to be justified as consistent with the Bank's formal policy framework.
                B. It suggests that the Bank wants to ensure that any intervention is technically well-calibrated before acting.
                C. It implies that current exchange-rate volatility is not yet serious enough to merit intervention.
                D. It shifts the discussion into procedural and institutional terms in order to avoid a direct commitment to near-term action.

                Answer with only A, B, C, or D.
            """),
            "answer": "D",
        },
        {
            "prompt": textwrap.dedent("""
                Context:
                A trade authority official is asked whether a politically sensitive import license will be approved after weeks of public pressure from business groups.

                Statement:
                "The application will be considered in accordance with standard licensing procedures once the full interdepartmental review has been completed."

                Question:
                What is the most likely implied function of this statement?

                A. It shifts the discussion into procedural terms in order to avoid taking a direct position on whether the license will be approved.
                B. It indicates that approval remains possible, but only after the required procedural steps are completed.
                C. It suggests that the authority is waiting for the review process to establish whether the application satisfies the relevant administrative and regulatory criteria.
                D. It reassures business groups that the application is moving normally through the system and is likely to receive a fair outcome.

                Answer with only A, B, C, or D.
            """),
            "answer": "A",
        },
        {
            "prompt": textwrap.dedent("""
                Context:
                A procurement agency spokesperson is asked whether a controversial public tender will be suspended after allegations of favoritism from opposition lawmakers.

                Statement:
                "The matter will be addressed through the established oversight and review channels, in accordance with the procurement framework currently in force."

                Question:
                What is the most likely implied function of this statement?

                A. It indicates that the tender is still legally valid unless a formal violation is identified.
                B. It reassures critics that the allegations are already being resolved through the proper institutional process.
                C. It shifts the discussion into procedural and oversight terms in order to avoid taking a direct position on whether the tender will be suspended.
                D. It suggests that the agency's main concern is to preserve the credibility of procurement rules during politically sensitive disputes.

                Answer with only A, B, C, or D.
            """),
            "answer": "C",
        },
        {
            "prompt": textwrap.dedent("""
                Context:
                A competition authority official is asked whether a proposed merger between two large distributors will be blocked after criticism that it could reduce consumer choice.

                Statement:
                "The transaction is being examined under the Authority's standard assessment framework, and any determination will follow the completion of the formal review process."

                Question:
                What is the most likely implied function of this statement?

                A. It indicates that the merger could still be approved if the parties satisfy the Authority's usual review criteria.
                B. It shifts the discussion into procedural and evaluative terms in order to avoid taking a direct position on whether the merger will be blocked.
                C. It suggests that the Authority's main concern is to ensure that the merger is judged according to consistent technical standards rather than political pressure.
                D. It reassures consumers that the review process is already working to protect market choice and competition.

                Answer with only A, B, C, or D.
            """),
            "answer": "B",
        },
        {
            "prompt": textwrap.dedent("""
                Context:
                An energy regulator is asked whether a proposed electricity tariff revision will be postponed after criticism from consumer groups about rising household costs.

                Statement:
                "Any decision on timing will be taken in line with the Commission's established review calendar and the completion of its scheduled technical consultations."

                Question:
                What is the most likely implied function of this statement?

                A. It shifts the discussion into procedural and scheduling terms in order to avoid taking a direct position on whether the tariff revision will be postponed.
                B. It indicates that the tariff revision could still be delayed if the consultation process reveals sufficient concern about household affordability.
                C. It suggests that the Commission's main concern is to ensure that the final timing reflects a technically orderly consultation process.
                D. It reassures consumer groups that the existing review calendar is already designed to protect household interests.

                Answer with only A, B, C, or D.
            """),
            "answer": "A",
        },
        {
            "prompt": textwrap.dedent("""
                Context:
                A pharmaceutical regulator is asked whether approval of a high-profile imported medicine will be accelerated after public pressure from patient groups.

                Statement:
                "The application will continue to be processed under the Authority's established evaluation timetable and according to the sequencing requirements of the current review protocol."

                Question:
                What is the most likely implied function of this statement?

                A. It indicates that accelerated approval remains possible if the medicine performs strongly under the existing review criteria.
                B. It suggests that the Authority's main concern is to ensure that the medicine is assessed in the correct technical sequence before any decision is made.
                C. It reassures patient groups that the application is progressing appropriately within a system designed to protect fairness and safety.
                D. It shifts the discussion into procedural and sequencing terms in order to avoid taking a direct position on whether approval will be accelerated.

                Answer with only A, B, C, or D.
            """),
            "answer": "D",
        },
        {
            "prompt": textwrap.dedent("""
                Context:
                A telecommunications regulator is asked whether a disputed spectrum allocation decision will be reopened after complaints from smaller operators that the process favored larger firms.

                Statement:
                "Any further action would need to proceed through the Authority's established reconsideration mechanism and in accordance with the sequencing rules governing spectrum review."

                Question:
                What is the most likely implied function of this statement?

                A. It indicates that the decision could still be reopened if the complaining operators satisfy the requirements for formal reconsideration.
                B. It suggests that the Authority's main concern is to ensure that any reconsideration follows the proper technical order required in spectrum administration.
                C. It shifts the discussion into procedural and sequencing terms in order to avoid taking a direct position on whether the allocation decision will be reopened.
                D. It reassures smaller operators that the current framework already provides a fair route for addressing their concerns.

                Answer with only A, B, C, or D.
            """),
            "answer": "C",
        },
        {
            "prompt": textwrap.dedent("""
                Context:
                A financial regulator is asked whether a controversial banking license application will be rejected after reports that the applicant has strong political connections.

                Statement:
                "The file is being handled under the Authority's standard fit-and-proper assessment procedures, and any conclusion will follow the completion of the prescribed review stages."

                Question:
                What is the most likely implied function of this statement?

                A. It indicates that the application could still succeed if the applicant satisfies the regulator's established licensing criteria.
                B. It shifts the discussion into procedural and evaluative terms in order to avoid taking a direct position on whether the application will be rejected.
                C. It suggests that the regulator's main concern is to ensure that political controversy does not interfere with the technical integrity of the review.
                D. It reassures the public that the existing licensing process is already sufficient to protect the system from improper influence.

                Answer with only A, B, C, or D.
            """),
            "answer": "B",
        },
        {
            "prompt": textwrap.dedent("""
                Context:
                An environmental regulator is asked whether an operating permit for a large industrial project will be suspended after local groups raise concerns about compliance failures.

                Statement:
                "Any determination on the permit's status will be made through the Authority's established compliance review process and in line with the sequencing requirements governing enforcement action."

                Question:
                What is the most likely implied function of this statement?

                A. It shifts the discussion into procedural and enforcement terms in order to avoid taking a direct position on whether the permit will be suspended.
                B. It indicates that suspension remains possible if the compliance review establishes sufficient grounds for enforcement.
                C. It suggests that the Authority's main concern is to ensure that any enforcement action follows the correct administrative sequence.
                D. It reassures local groups that the current compliance framework is already capable of protecting their interests.

                Answer with only A, B, C, or D.
            """),
            "answer": "A",
        },
    ]

    for i, case in enumerate(cases, start=1):
        response = llm.prompt(case["prompt"])
        pred = extract_choice(response)

        assert pred == case["answer"], (
            f"Item {i} failed. Expected {case['answer']}, got {pred}. "
            f"Raw response: {response}"
        )
